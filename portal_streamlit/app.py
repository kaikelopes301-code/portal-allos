"""
Portal Performance - Entry Point
=================================
Aplicação principal do portal de faturamento Atlas.
Design System v2.0 - Professional Edition
"""

import os
import sys
import warnings

import streamlit as st

# Suppress non-critical warnings
warnings.filterwarnings("ignore", message=".*Data Validation extension is not supported.*")
warnings.filterwarnings("ignore", message=".*Unknown extension is not supported.*")

# Ensure project root is in path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

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
except Exception:
    # Fallback: show loading screen with branding
    from portal_streamlit.utils.ui import COLORS
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .loading-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 80vh;
        text-align: center;
        background-color: {COLORS['background']};
    }}
    
    .loading-logo {{
        width: 80px;
        height: 80px;
        background: {COLORS['primary']};
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        color: white;
        margin-bottom: 1.5rem;
        animation: pulse 2s infinite;
    }}
    
    .loading-title {{
        font-family: 'Inter', sans-serif;
        font-size: 1.75rem;
        font-weight: 700;
        color: {COLORS['text_primary']};
        margin-bottom: 0.5rem;
    }}
    
    .loading-subtitle {{
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: {COLORS['text_secondary']};
        margin-bottom: 2rem;
    }}
    
    .loading-spinner {{
        width: 40px;
        height: 40px;
        border: 3px solid {COLORS['divider']};
        border-top: 3px solid {COLORS['primary']};
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); opacity: 1; }}
        50% {{ transform: scale(1.05); opacity: 0.8; }}
    }}
    </style>
    
    <div class="loading-container">
        <div class="loading-logo">📊</div>
        <h1 class="loading-title">Portal Performance</h1>
        <p class="loading-subtitle">Carregando sistema...</p>
        <div class="loading-spinner"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Force page reload after brief delay
    import time
    time.sleep(1)
    st.rerun()
