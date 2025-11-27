"""
Portal Performance - Entry Point
=================================
Aplicação principal do portal de faturamento Atlas.
Design System v2.0 - Professional Edition
"""

import warnings
import streamlit as st

# Inicialização do pacote (configura sys.path automaticamente)
import portal_streamlit

# Suppress non-critical warnings
warnings.filterwarnings("ignore", message=".*Data Validation extension is not supported.*")
warnings.filterwarnings("ignore", message=".*Unknown extension is not supported.*")

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="Portal Performance | Atlas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:Kaike.costa@atlasinovacoes.com.br',
        'Report a bug': 'mailto:Kaike.costa@atlasinovacoes.com.br',
        'About': '''
        ## Portal Performance v2.0
        
        Sistema de gestão de relatórios de faturamento.
        
        **Desenvolvido por:** Atlas Inovações
        '''
    }
)

# Redirect to main page for better UX
try:
    st.switch_page("pages/1_Execução.py")
except Exception as e:
    # Fallback simples caso redirecionamento falhe
    st.error("❌ Erro ao carregar página inicial")
    st.info("Por favor, navegue manualmente para a página 'Execução' no menu lateral.")
    st.caption(f"Detalhes: {str(e)}")
