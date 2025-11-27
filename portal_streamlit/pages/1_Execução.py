import re
import subprocess
import time

import streamlit as st
from portal_streamlit.pages import init_page
from portal_streamlit.utils.pipeline import list_units_for_region, get_regions

# Inicialização da página (substitui código duplicado)
config = init_page("Execução do Pipeline", "⚙️")

# Interface
st.title("⚙️ Execução do Pipeline")

regioes = get_regions()
idx_default = regioes.index(config.get("default_regiao", "SP1")) if config.get("default_regiao", "SP1") in regioes else 0
regiao = st.selectbox("🗺️ Região", options=regioes, index=max(0, idx_default))

unidades_da_regiao = list_units_for_region(config.get("xlsx_dir", "c:/backpperformance/planilhas"), regiao)
unidades_selecionadas = st.multiselect("🏢 Unidades", options=unidades_da_regiao, default=unidades_da_regiao)

col1, col2 = st.columns(2)
with col1:
    envio_real = st.toggle("📧 Envio real via SendGrid", value=False, help="Habilita o envio de e-mails.")
with col2:
    permitir_reenvio = st.checkbox("🔄 Forçar reenvio", value=False, help="Ignora histórico de envios anteriores.")

if not envio_real:
    st.info("**Modo Dry-Run:** Geração de HTML e simulação de envio.")

st.divider()

# Botão e Métricas
c_btn, c_tot, c_mode = st.columns([2, 1, 1])    
iniciar = c_btn.button("Executar Pipeline", type="primary", use_container_width=True)
c_tot.metric("Total Unidades", len(unidades_selecionadas))
c_mode.metric("Modo", "Produção" if envio_real else "Dry-Run", delta="SendGrid" if envio_real else "Simulação", delta_color="normal" if envio_real else "off")

# --- LÓGICA DE EXECUÇÃO ---
if iniciar:
    if not unidades_selecionadas:
        st.error("❌ Selecione pelo menos uma unidade!")
        st.stop()

    total_units = len(unidades_selecionadas)
    
    # Montagem do Comando (forçando modo unbuffered com -u)
    cmd = [
        config.get("python_path", "python"),
        "-u",
        config.get("main_py_path", "c:/backpperformance/main.py"),
        "--regiao", regiao,
        "--mes", config.get("default_mes", "2025-08"),
        "--xlsx-dir", config.get("xlsx_dir", "c:/backpperformance/planilhas"),
        "--non-interactive",
    ]
    
    if not envio_real:
        cmd.append("--dry-run")
    if permitir_reenvio:
        cmd.append("--allow-resend")
    
    # Adiciona unidades separadas por vírgula
    if unidades_selecionadas:
        cmd.extend(["--units", ",".join(unidades_selecionadas)])

    st.subheader("📊 Status da execução")

    # Container de Status Imersivo (Streamlit 1.28+)
    with st.status("🚀 Inicializando pipeline...", expanded=True) as status_container:
        
        # Layout interno do status
        header_placeholder = st.empty()
        progress_placeholder = st.empty()
        
        # Variáveis de controle aprimoradas
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            encoding='utf-8',  # Garante leitura correta de acentos
            errors='replace'
        )

        processed_count = 0
        processed_units = set()  # ✨ Rastreia unidades únicas processadas
        errors_count = 0
        warnings_count = 0
        current_unit = "Iniciando..."
        
        full_logs = []

        # Regex otimizados
        re_unit_start = re.compile(r"Processando unidade:?\s*(.+)", re.IGNORECASE)
        re_error = re.compile(r"\[(ERROR|ERRO)\]", re.IGNORECASE)
        re_warn = re.compile(r"\[WARN\]", re.IGNORECASE)

        start_time = time.time()

        def update_ui():
            """Atualiza UI com progresso atual."""
            # Garante que contador nunca excede total
            display_count = min(processed_count, total_units)
            progress_pct = min(processed_count / total_units, 1.0) if total_units > 0 else 0
            
            # Cabeçalho com unidade atual
            header_placeholder.markdown(
                f"""
                <div style="margin-bottom:0.5rem;">
                    <strong>Unidade atual:</strong> {current_unit}<br>
                    <span style="color:#A1A1AA;font-size:0.85rem;">
                        Concluídas: {display_count}/{total_units}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            # Progress bar simples (só porcentagem)
            progress_placeholder.progress(progress_pct)

        update_ui()

        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            
            if line:
                clean_line = line.strip()
                full_logs.append(clean_line)
                
                # Conta erros e warnings
                if re_error.search(clean_line):
                    errors_count += 1
                elif re_warn.search(clean_line):
                    warnings_count += 1

                # ✅ CORRIGIDO: Detecta mudança de unidade e marca anterior como concluída
                match_unit = re_unit_start.search(clean_line)
                if match_unit:
                    new_unit = match_unit.group(1).strip()
                    
                    # Se mudou de unidade, marca anterior como concluída
                    if new_unit != current_unit:
                        # Adiciona unidade anterior ao set (se não for a primeira)
                        if current_unit != "Iniciando...":
                            processed_units.add(current_unit)
                            processed_count = len(processed_units)
                        
                        # Atualiza para nova unidade
                        current_unit = new_unit
                        
                        # Atualiza UI
                        update_ui()
                        
                        # Atualiza status container
                        status_container.update(
                            label=f"🚀 Executando pipeline... ({processed_count}/{total_units})",
                            state="running",
                            expanded=True,
                        )

        # ✅ Marca última unidade como concluída
        if current_unit and current_unit != "Iniciando...":
            processed_units.add(current_unit)
            processed_count = len(processed_units)
        
        # Captura stderr final se houver falha catastrófica
        stderr_output = process.stderr.read()
        returncode = process.wait()
        end_time = time.time()
        duration = end_time - start_time

        # Atualiza estado final do container
        if returncode == 0 and errors_count == 0:
            status_container.update(label=f"✅ Pipeline concluído em {duration:.1f}s!", state="complete", expanded=False)
        elif errors_count > 0:
            status_container.update(label="⚠️ Pipeline concluído com erros.", state="error", expanded=True)
        else:
            status_container.update(label="❌ Falha na execução.", state="error", expanded=True)

    # --- LOGS COMPLETOS ---
    if stderr_output:
        st.error("Erro crítico no processo Python:")
        st.code(stderr_output)

    with st.expander("📄 Ver Logs Completos (Texto Puro)"):
        st.text("\n".join(full_logs))
