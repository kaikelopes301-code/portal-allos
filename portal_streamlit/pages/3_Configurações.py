"""
Página de Configurações - Versão Refatorada
Usa arquitetura de serviços e componentes reutilizáveis.
"""
import streamlit as st
from portal_streamlit.pages import init_page
from portal_streamlit.services import ConfigService, ColumnManager
from portal_streamlit.utils.pipeline import get_regions, list_units_for_region
from portal_streamlit.utils.validators import ConfigValidator
from portal_streamlit.utils.ui import (
    render_preset_selector,
    render_scope_selector,
    render_config_summary,
    render_copy_config_selector
)
from portal_streamlit.constants import PRESETS

# ============================================================================
# Inicialização
# ============================================================================

config = init_page("Configurações", "🛠️")

# Instancia serviços
config_service = ConfigService()
column_manager = ColumnManager()

st.title("⚙️ Configurações")
st.caption("Configure colunas de relatórios e mês de referência por unidade, região ou globalmente")

# ============================================================================
# Seleção de Contexto
# ============================================================================

st.markdown("### 📋 Seleção de Contexto")

col1, col2 = st.columns(2)

with col1:
    regioes = get_regions()
    default_regiao = config.get("default_regiao", "SP1")
    regiao_index = regioes.index(default_regiao) if default_regiao in regioes else 0
    
    regiao = st.selectbox(
        "Região",
        options=regioes,
        index=regiao_index,
        key="cfg_regiao"
    )

with col2:
    xlsx_dir = config.get("xlsx_dir", "c:/backpperformance/planilhas")
    unidades = list_units_for_region(xlsx_dir, regiao)
    
    if unidades:
        unidade = st.selectbox(
            "Unidade",
            options=unidades,
            key="cfg_unidade"
        )
    else:
        unidade = None
        st.warning("⚠️ Nenhuma unidade encontrada para esta região")

st.divider()

# ============================================================================
# Processamento Principal (quando unidade está selecionada)
# ============================================================================

if unidade:
    # Obtém configuração atual da unidade (se existir)
    current_config = config_service.get_unit_config(unidade) or {}
    current_columns = current_config.get("columns", column_manager.get_default_columns())
    current_month = current_config.get("month_reference", config.get("default_mes", "2025-08"))
    
    # ========================================================================
    # TABS para organizar melhor a interface
    # ========================================================================
    
    tab1, tab2, tab3 = st.tabs(["🎨 Templates & Presets", "📊 Configuração Manual", "📋 Copiar Configuração"])
    
    # ------------------------------------------------------------------------
    # TAB 1: Templates & Presets
    # ------------------------------------------------------------------------
    with tab1:
        st.markdown("### 🎨 Selecione um Template")
        st.caption("Use um template predefinido para configurar rapidamente as colunas")
        
        # Renderiza seletor de presets
        preset_name, preset_data = render_preset_selector(PRESETS)
        
        if preset_name:
            # Usuário selecionou um preset
            if st.button(f"✓ Aplicar Template '{preset_name}'", key="apply_preset"):
                selected_columns = preset_data["columns"].copy()
                st.session_state["selected_columns"] = selected_columns
                st.success(f"✅ Template '{preset_name}' aplicado! ({len(selected_columns)} colunas)")
                st.rerun()
        else:
            st.info("ℹ️ Selecione um template acima ou configure manualmente na aba 'Configuração Manual'")
    
    # ------------------------------------------------------------------------
    # TAB 2: Configuração Manual
    # ------------------------------------------------------------------------
    with tab2:
        st.markdown("### 📊 Configuração Manual de Colunas")
        
        # Busca de colunas
        search_term = st.text_input(
            "🔍 Buscar coluna",
            placeholder="Digite para filtrar colunas...",
            key="column_search"
        )
        
        # Inicializa seleção se não existir
        if "selected_columns" not in st.session_state:
            st.session_state["selected_columns"] = current_columns.copy()
        
        # Filtra colunas por busca
        all_columns = column_manager.get_all_columns()
        if search_term:
            filtered_columns = column_manager.filter_columns(search_term)
        else:
            filtered_columns = all_columns
        
        # Botões de seleção em massa
        col_actions1, col_actions2 = st.columns(2)
        
        with col_actions1:
            if st.button("✓ Selecionar Todas", key="select_all_cols", use_container_width=True):
                st.session_state["selected_columns"] = filtered_columns.copy()
                st.rerun()
        
        with col_actions2:
            if st.button("✗ Desmarcar Todas", key="deselect_all_cols", use_container_width=True):
                st.session_state["selected_columns"] = []
                st.rerun()
        
        st.divider()
        
        # Lista simples de checkboxes
        for col in filtered_columns:
            is_selected = col in st.session_state["selected_columns"]
            checked = st.checkbox(
                col,
                value=is_selected,
                key=f"col_{col}"
            )
            
            if checked and not is_selected:
                st.session_state["selected_columns"].append(col)
            elif not checked and is_selected:
                st.session_state["selected_columns"].remove(col)
        
        # Resumo das colunas selecionadas
        st.divider()
        stats = column_manager.get_column_stats(st.session_state["selected_columns"])
        st.info(f"📊 **{stats['total']} colunas selecionadas** ({stats['defaults']} padrão + {stats['extras']} extras)")
    
    # ------------------------------------------------------------------------
    # TAB 3: Copiar de Outra Unidade
    # ------------------------------------------------------------------------
    with tab3:
        st.markdown("### 📋 Copiar Configuração")
        st.caption("Copie todas as configurações (colunas + mês) de outra unidade")
        
        # Obtém unidades configuradas
        units_with_config = config_service.get_units_with_config()
        
        source_unit = render_copy_config_selector(units_with_config, unidade)
        
        if source_unit:
            source_config = config_service.get_unit_config(source_unit)
            
            if source_config:
                # Mostra preview da configuração
                st.markdown("#### Preview da Configuração:")
                render_config_summary(source_config, column_manager)
                
                if st.button(f"✓ Copiar de '{source_unit}'", key="copy_config_btn"):
                    st.session_state["selected_columns"] = source_config.get("columns", []).copy()
                    st.session_state["copied_month"] = source_config.get("month_reference")
                    st.success(f"✅ Configuração copiada de '{source_unit}'!")
                    st.rerun()
    
    # ========================================================================
    # Configuração de Mês (fora das tabs)
    # ========================================================================
    
    st.divider()
    st.markdown("### 📅 Mês de Referência")
    
    # Verifica se há mês copiado
    if "copied_month" in st.session_state:
        default_month = st.session_state["copied_month"]
        del st.session_state["copied_month"]
    else:
        default_month = current_month
    
    mes = st.text_input(
        "Mês (AAAA-MM)",
        value=default_month,
        help="Formato: AAAA-MM (ex: 2025-10)",
        key="mes_input"
    )
    
    # Validação em tempo real
    if mes and not ConfigValidator.validate_month_format(mes):
        st.error("❌ Formato inválido! Use AAAA-MM (ex: 2025-10)")
    elif mes:
        st.success(f"✅ Mês válido: {mes}")
    
    # ========================================================================
    # Escopo de Aplicação
    # ========================================================================
    
    st.divider()
    apply_scope, scope_desc = render_scope_selector(unidade, regiao, regioes)
    
    # ========================================================================
    # Preview da Configuração
    # ========================================================================
    
    st.divider()
    st.markdown("### 👁️ Preview da Configuração")
    
    # Monta configuração para preview
    preview_config = {
        "columns": st.session_state.get("selected_columns", []),
        "month_reference": mes
    }
    
    render_config_summary(preview_config, column_manager)
    
    # ========================================================================
    # Botão de Salvar
    # ========================================================================
    
    st.divider()
    
    col_save1, col_save2 = st.columns([3, 1])
    
    with col_save1:
        if st.button("💾 Salvar Configurações", type="primary", use_container_width=True):
            # Valida configuração
            config_data = {
                "columns": st.session_state.get("selected_columns", []),
                "month_reference": mes
            }
            
            is_valid, errors = config_service.validate_config(config_data)
            
            if not is_valid:
                st.error(f"❌ Erro de validação: {'; '.join(errors)}")
            else:
                # Determina unidades alvo
                if apply_scope == "Somente esta unidade":
                    targets = [unidade]
                elif apply_scope == "Todas as unidades desta região":
                    targets = list_units_for_region(xlsx_dir, regiao) or []
                else:  # Todas as unidades
                    targets = []
                    for r in get_regions():
                        units_r = list_units_for_region(xlsx_dir, r) or []
                        targets.extend(units_r)
                
                # Remove duplicatas
                targets = list(dict.fromkeys(targets))
                
                # Aplica configuração
                success, message = config_service.apply_config_to_units(
                    config_data,
                    targets,
                    user="streamlit_user"
                )
                
                if success:
                    # Atualiza config global
                    config["default_regiao"] = regiao
                    if ConfigValidator.validate_month_format(mes):
                        config["default_mes"] = mes.strip()
                    
                    from portal_streamlit.utils.config_manager import save_config
                    save_config(config)
                    
                    st.success(f"✅ {message}")
                    
                    # Limpa session state
                    if "selected_columns" in st.session_state:
                        del st.session_state["selected_columns"]
                else:
                    st.error(f"❌ {message}")
    
    with col_save2:
        if st.button("🔄 Resetar", use_container_width=True):
            if "selected_columns" in st.session_state:
                del st.session_state["selected_columns"]
            st.rerun()
    
    # ========================================================================
    # Estatísticas (opcional, no final)
    # ========================================================================
    
    with st.expander("📈 Estatísticas de Configuração"):
        stats = config_service.get_config_stats()
        
        metrics_cols = st.columns(3)
        
        with metrics_cols[0]:
            st.metric("Total de Unidades Configuradas", stats["total_configured_units"])
        
        with metrics_cols[1]:
            st.metric("Com Mês Personalizado", stats["units_with_custom_month"])
        
        with metrics_cols[2]:
            st.metric("Com Colunas Personalizadas", stats["units_with_custom_columns"])

else:
    st.info("ℹ️ Selecione uma região e uma unidade para começar a configurar")
