"""
Portal Streamlit - Páginas - Funções Comuns
==========================================
Utilitários compartilhados para inicialização de páginas.
"""

import streamlit as st
from portal_streamlit.utils.ui import inject_global_styles, render_sidebar_branding
from portal_streamlit.utils.config_manager import get_config


def init_page(title: str, icon: str, layout: str = "wide"):
    """
    Inicializa configuração padrão de uma página Streamlit.
    
    Esta função centraliza a inicialização repetitiva de páginas,
    aplicando estilos globais, sidebar branding e retornando a configuração.
    
    Args:
        title: Título da página (aparece na aba do navegador)
        icon: Emoji ou ícone da página
        layout: Layout da página ("wide" ou "centered")
        
    Returns:
        dict: Configuração global do portal carregada de config.json
        
    Example:
        ```python
        from portal_streamlit.pages import init_page
        
        config = init_page("Execução do Pipeline", "⚙️")
        st.title("Minha Página")
        ```
    """
    st.set_page_config(page_title=title, page_icon=icon, layout=layout)
    inject_global_styles()
    render_sidebar_branding()
    return get_config()
