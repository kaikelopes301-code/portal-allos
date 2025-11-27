"""
Portal Performance - Design System Profissional
================================================
Sistema de design unificado com componentes reutilizáveis,
tokens de design e estilização avançada.
"""

import os
import streamlit as st
from typing import Optional, Literal

# ============================================================================
# DESIGN TOKENS
# ============================================================================

COLORS = {
    # Primary Palette
    "primary": "#6366F1",      # Indigo vibrante
    "primary_hover": "#4F46E5",
    "primary_light": "#EEF2FF",
    "primary_dark": "#3730A3",
    
    # Neutral Palette
    "bg_primary": "#0F0F12",    # Fundo principal (quase preto)
    "bg_secondary": "#18181B",  # Cards e elevações
    "bg_tertiary": "#27272A",   # Inputs e elementos interativos
    "bg_elevated": "#1E1E23",   # Modais e popovers
    
    # Text
    "text_primary": "#FAFAFA",
    "text_secondary": "#A1A1AA",
    "text_muted": "#71717A",
    
    # Semantic
    "success": "#22C55E",
    "success_bg": "rgba(34, 197, 94, 0.1)",
    "warning": "#F59E0B",
    "warning_bg": "rgba(245, 158, 11, 0.1)",
    "error": "#EF4444",
    "error_bg": "rgba(239, 68, 68, 0.1)",
    "info": "#3B82F6",
    "info_bg": "rgba(59, 130, 246, 0.1)",
    
    # Borders
    "border": "rgba(255, 255, 255, 0.08)",
    "border_hover": "rgba(255, 255, 255, 0.15)",
    
    # Gradients
    "gradient_primary": "linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)",
    "gradient_success": "linear-gradient(135deg, #22C55E 0%, #16A34A 100%)",
    "gradient_mesh": "radial-gradient(at 40% 20%, rgba(99, 102, 241, 0.15) 0px, transparent 50%), radial-gradient(at 80% 0%, rgba(139, 92, 246, 0.1) 0px, transparent 50%), radial-gradient(at 0% 50%, rgba(34, 197, 94, 0.05) 0px, transparent 50%)",
}

SPACING = {
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "1rem",
    "lg": "1.5rem",
    "xl": "2rem",
    "2xl": "3rem",
}

TYPOGRAPHY = {
    "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "font_mono": "'JetBrains Mono', 'Fira Code', monospace",
}

SHADOWS = {
    "sm": "0 1px 2px rgba(0, 0, 0, 0.3)",
    "md": "0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -2px rgba(0, 0, 0, 0.3)",
    "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -4px rgba(0, 0, 0, 0.4)",
    "glow": f"0 0 20px rgba(99, 102, 241, 0.3)",
}

# ============================================================================
# GLOBAL STYLES
# ============================================================================

def inject_global_styles():
    """Injeta o sistema de design completo na aplicação."""
    
    st.markdown(f"""
    <style>
    /* ========================================
       GOOGLE FONTS
    ======================================== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* ========================================
       CSS RESET & BASE
    ======================================== */
    *, *::before, *::after {{
        box-sizing: border-box;
    }}
    
    /* ========================================
       ROOT & BODY
    ======================================== */
    .stApp {{
        background: {COLORS['bg_primary']};
        background-image: {COLORS['gradient_mesh']};
        background-attachment: fixed;
        /* fonte padrão da aplicação (filhos herdam) */
        font-family: {TYPOGRAPHY['font_family']};
    }}
    
    /* (REMOVIDO) .stApp * para não sobrescrever fontes de ícones */
    
    /* ========================================
       SIDEBAR
    ======================================== */
    section[data-testid="stSidebar"] {{
        background: {COLORS['bg_secondary']};
        border-right: 1px solid {COLORS['border']};
    }}
    
    section[data-testid="stSidebar"] > div:first-child {{
        padding-top: 1rem;
        display: flex;
        flex-direction: column;
        height: 100%;
    }}
    
    /* Hide default nav */
    section[data-testid="stSidebarNav"],
    div[data-testid="stSidebarNav"],
    nav[data-testid="stSidebarNav"] {{
        display: none !important;
    }}
    
    /* ========================================
       TYPOGRAPHY
    ======================================== */
    h1, .stMarkdown h1 {{
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: {COLORS['text_primary']} !important;
        letter-spacing: -0.025em;
        margin-bottom: 0.5rem !important;
    }}
    
    h2, .stMarkdown h2 {{
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: {COLORS['text_primary']} !important;
        letter-spacing: -0.02em;
    }}
    
    h3, .stMarkdown h3 {{
        font-size: 1.125rem !important;
        font-weight: 600 !important;
        color: {COLORS['text_primary']} !important;
    }}
    
    p, .stMarkdown p {{
        color: {COLORS['text_secondary']};
        line-height: 1.6;
    }}
    
    /* ========================================
       BUTTONS
    ======================================== */
    .stButton > button {{
        background: {COLORS['gradient_primary']} !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.625rem 1.25rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        letter-spacing: 0.01em;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: {SHADOWS['md']}, {SHADOWS['glow']} !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-1px) !important;
        box-shadow: {SHADOWS['lg']}, 0 0 30px rgba(99, 102, 241, 0.4) !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(0) !important;
    }}
    
    /* Secondary button style */
    .stButton > button[kind="secondary"] {{
        background: transparent !important;
        border: 1px solid {COLORS['border']} !important;
        color: {COLORS['text_primary']} !important;
        box-shadow: none !important;
    }}
    
    .stButton > button[kind="secondary"]:hover {{
        background: {COLORS['bg_tertiary']} !important;
        border-color: {COLORS['border_hover']} !important;
    }}
    
    /* ========================================
       INPUTS & SELECTS
    ======================================== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        background: {COLORS['bg_tertiary']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 10px !important;
        color: {COLORS['text_primary']} !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: {COLORS['primary']} !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
        outline: none !important;
    }}
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {{
        color: {COLORS['text_muted']} !important;
    }}
    
    /* Selectbox */
    .stSelectbox > div > div {{
        background: {COLORS['bg_tertiary']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 10px !important;
    }}
    
    .stSelectbox [data-baseweb="select"] {{
        background: transparent !important;
    }}
    
    .stSelectbox [data-baseweb="select"] > div {{
        background: {COLORS['bg_tertiary']} !important;
        border: none !important;
        border-radius: 10px !important;
    }}
    
    /* Multiselect */
    .stMultiSelect > div > div {{
        background: {COLORS['bg_tertiary']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 10px !important;
    }}
    
    .stMultiSelect [data-baseweb="tag"] {{
        background: {COLORS['primary']} !important;
        border-radius: 6px !important;
    }}
    
    /* ========================================
       TOGGLE / CHECKBOX
    ======================================== */
    .stCheckbox > label > div[data-testid="stCheckbox"] {{
        background: {COLORS['bg_tertiary']} !important;
        border-radius: 4px !important;
    }}
    
    .stCheckbox > label > div[data-testid="stCheckbox"][aria-checked="true"] {{
        background: {COLORS['primary']} !important;
    }}
    
    /* Toggle */
    div[data-baseweb="toggle"] > div {{
        background: {COLORS['bg_tertiary']} !important;
    }}
    
    div[data-baseweb="toggle"][aria-checked="true"] > div {{
        background: {COLORS['primary']} !important;
    }}
    
    /* ========================================
       PROGRESS BAR
    ======================================== */
    .stProgress > div > div > div {{
        background: {COLORS['gradient_primary']} !important;
        border-radius: 999px !important;
    }}
    
    .stProgress > div > div {{
        background: {COLORS['primary']} !important;
        border-radius: 999px !important;
    }}
    
    /* ========================================
       EXPANDER
    ======================================== */
    .streamlit-expanderHeader {{
        background: {COLORS['bg_secondary']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 12px !important;
        color: {COLORS['text_primary']} !important;
        font-weight: 500 !important;
    }}
    
    .streamlit-expanderHeader:hover {{
        border-color: {COLORS['border_hover']} !important;
    }}
    
    .streamlit-expanderContent {{
        background: {COLORS['bg_secondary']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }}
    
    /* ========================================
       DATAFRAME
    ======================================== */
    .stDataFrame {{
        border: 1px solid {COLORS['border']} !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }}
    
    .stDataFrame [data-testid="stDataFrameResizable"] {{
        background: {COLORS['bg_secondary']} !important;
    }}
    
    /* ========================================
       ALERTS & MESSAGES
    ======================================== */
    .stAlert {{
        border-radius: 12px !important;
        border: none !important;
    }}
    
    div[data-testid="stNotification"] {{
        background: {COLORS['bg_elevated']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 12px !important;
    }}
    
    /* Success */
    .element-container div[data-testid="stAlert"][data-baseweb="notification"] {{
        border-left: 4px solid {COLORS['success']} !important;
    }}
    
    /* ========================================
       DIVIDER
    ======================================== */
    hr {{
        border: none !important;
        border-top: 1px solid {COLORS['border']} !important;
        margin: 1.5rem 0 !important;
    }}
    
    /* ========================================
       CODE BLOCKS
    ======================================== */
    .stCodeBlock {{
        border-radius: 12px !important;
        border: 1px solid {COLORS['border']} !important;
    }}
    
    code {{
        font-family: {TYPOGRAPHY['font_mono']} !important;
        background: {COLORS['bg_tertiary']} !important;
        padding: 0.2rem 0.4rem !important;
        border-radius: 6px !important;
        font-size: 0.85rem !important;
    }}
    
    /* ========================================
       TABS
    ======================================== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        background: transparent;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: transparent !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 10px !important;
        color: {COLORS['text_secondary']} !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
    }}
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background: {COLORS['primary']} !important;
        border-color: {COLORS['primary']} !important;
        color: white !important;
    }}
    
    .stTabs [data-baseweb="tab-highlight"] {{
        display: none !important;
    }}
    
    /* ========================================
       METRICS
    ======================================== */
    [data-testid="stMetric"] {{
        background: {COLORS['bg_secondary']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {COLORS['text_muted']} !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }}
    
    [data-testid="stMetricValue"] {{
        color: {COLORS['text_primary']} !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
    }}
    
    /* ========================================
       SCROLLBAR
    ======================================== */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {COLORS['bg_primary']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {COLORS['bg_tertiary']};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORS['text_muted']};
    }}
    
    /* ========================================
       ANIMATIONS
    ======================================== */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
    }}
    
    @keyframes shimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    
    .animate-fade-in {{
        animation: fadeIn 0.3s ease-out forwards;
    }}
    
    .animate-pulse {{
        animation: pulse 2s infinite;
    }}
    
    /* ========================================
       CUSTOM COMPONENTS
    ======================================== */
    .card {{
        background: {COLORS['bg_secondary']};
        border: 1px solid {COLORS['border']};
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.2s ease;
    }}
    
    .card:hover {{
        border-color: {COLORS['border_hover']};
        box-shadow: {SHADOWS['md']};
    }}
    
    .card-header {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }}
    
    .card-icon {{
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }}
    
    .badge {{
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.025em;
    }}
    
    .badge-success {{
        background: {COLORS['success_bg']};
        color: {COLORS['success']};
    }}
    
    .badge-warning {{
        background: {COLORS['warning_bg']};
        color: {COLORS['warning']};
    }}
    
    .badge-error {{
        background: {COLORS['error_bg']};
        color: {COLORS['error']};
    }}
    
    .badge-info {{
        background: {COLORS['info_bg']};
        color: {COLORS['info']};
    }}
    
    .stat-card {{
        background: linear-gradient(135deg, {COLORS['bg_secondary']} 0%, {COLORS['bg_tertiary']} 100%);
        border: 1px solid {COLORS['border']};
        border-radius: 16px;
        padding: 1.25rem;
        position: relative;
        overflow: hidden;
    }}
    
    .stat-card::before {{
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%);
    }}
    
    .nav-item {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        color: {COLORS['text_secondary']};
        text-decoration: none;
        transition: all 0.15s ease;
        cursor: pointer;
        font-weight: 500;
    }}
    
    .nav-item:hover {{
        background: {COLORS['bg_tertiary']};
        color: {COLORS['text_primary']};
    }}
    
    .nav-item.active {{
        background: {COLORS['primary']};
        color: white;
    }}
    
    .nav-item-icon {{
        font-size: 1.1rem;
        opacity: 0.8;
    }}
    
    .section-header {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }}
    
    .section-header h3 {{
        margin: 0;
    }}
    
    .section-header .line {{
        flex: 1;
        height: 1px;
        background: {COLORS['border']};
    }}
    
    /* Status indicator */
    .status-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }}
    
    .status-dot.online {{
        background: {COLORS['success']};
        box-shadow: 0 0 8px {COLORS['success']};
    }}
    
    .status-dot.offline {{
        background: {COLORS['error']};
    }}
    
    .status-dot.pending {{
        background: {COLORS['warning']};
        animation: pulse 1.5s infinite;
    }}
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# COMPONENT HELPERS
# ============================================================================

def render_sidebar_branding(
    title: str = "Portal Performance",
    subtitle: str = "Gestão de Relatórios HTML",
    version: str = "Allos"
):
    """Renderiza sidebar profissional com branding e navegação."""
    
    logo_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..", "assets", "logo-atlas.png"
    ))
    
    with st.sidebar:
        # Logo Container
        st.markdown("""
        <div style="
            padding: 1rem;
            margin-bottom: 0.5rem;
        ">
        """, unsafe_allow_html=True)
        
        try:
            st.image(logo_path, use_container_width=True)
        except Exception:
            # Fallback: logo placeholder
            st.markdown(f"""
            <div style="
                width: 100%;
                height: 60px;
                background: {COLORS['gradient_primary']};
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: 700;
                font-size: 1.5rem;
            ">
                ATLAS
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Title & Version
        st.markdown(f"""
        <div style="padding: 0 1rem; margin-bottom: 1.5rem;">
            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
            ">
                <h2 style="
                    margin: 0;
                    font-size: 1.25rem;
                    font-weight: 700;
                    color: {COLORS['text_primary']};
                ">{title}</h2>
                <span style="
                    background: {COLORS['bg_tertiary']};
                    color: {COLORS['text_muted']};
                    padding: 0.2rem 0.5rem;
                    border-radius: 6px;
                    font-size: 0.7rem;
                    font-weight: 600;
                ">{version}</span>
            </div>
            <p style="
                margin: 0.25rem 0 0 0;
                font-size: 0.8rem;
                color: {COLORS['text_muted']};
            ">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown(f"""
        <div style="
            padding: 0 0.5rem;
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        ">
        """, unsafe_allow_html=True)
        
        # Get current page for active state
        current_page = st.session_state.get("current_page", "execucao")
        
        nav_items = [
            ("execucao", "", "Execução", "pages/1_Execução.py"),
            ("preview", "", "Preview", "pages/2_Preview.py"),
            ("config", "", "Configurações", "pages/3_Configurações.py"),
            ("logs", "", "Logs", "pages/4_Logs.py"),
            ("help", "", "Ajuda", "pages/5_Ajuda.py"),
        ]
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Render navigation with Streamlit's page_link
        for key, icon, label, page in nav_items:
            st.page_link(page, label=f"{icon}  {label}")
        
                # Footer (ancorado no fim da coluna da sidebar, sem sobrepor o menu)
        st.markdown(f"""
        <div class="sidebar-footer" style="
            margin-top: auto;
            padding-top: 1rem;
            border-top: 1px solid {COLORS['border']};
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 0.5rem;
                color: {COLORS['text_muted']};
                font-size: 0.75rem;
            ">
                <span class="status-dot online"></span>
                Sistema operacional
            </div>
        </div>
        """, unsafe_allow_html=True)





def render_page_header(
    title: str,
    subtitle: Optional[str] = None,
    icon: Optional[str] = None,
    badge: Optional[tuple] = None  # (text, type: success/warning/error/info)
):
    """Renderiza header de página com título, subtítulo e badge opcional."""
    
    badge_html = ""
    if badge:
        badge_text, badge_type = badge
        badge_html = f'<span class="badge badge-{badge_type}">{badge_text}</span>'
    
    icon_html = f'<span style="font-size: 2rem; margin-right: 0.5rem;">{icon}</span>' if icon else ""
    
    st.markdown(f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
        animation: fadeIn 0.3s ease-out;
    ">
        <div>
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                {icon_html}
                <h1 style="margin: 0; font-size: 2rem;">{title}</h1>
                {badge_html}
            </div>
            {"<p style='margin: 0.25rem 0 0 0; color: " + COLORS['text_secondary'] + ";'>" + subtitle + "</p>" if subtitle else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_stat_card(
    label: str,
    value: str,
    icon: str,
    change: Optional[str] = None,
    change_type: Literal["positive", "negative", "neutral"] = "neutral"
):
    """Renderiza card de estatística."""
    
    change_color = {
        "positive": COLORS['success'],
        "negative": COLORS['error'],
        "neutral": COLORS['text_muted']
    }[change_type]
    
    change_html = f"""
    <div style="
        font-size: 0.75rem;
        color: {change_color};
        margin-top: 0.25rem;
    ">{change}</div>
    """ if change else ""
    
    st.markdown(f"""
    <div class="stat-card">
        <div style="
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
        ">
            <div>
                <div style="
                    font-size: 0.75rem;
                    color: {COLORS['text_muted']};
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    font-weight: 500;
                    margin-bottom: 0.25rem;
                ">{label}</div>
                <div style="
                    font-size: 1.75rem;
                    font-weight: 700;
                    color: {COLORS['text_primary']};
                ">{value}</div>
                {change_html}
            </div>
            <div style="
                width: 44px;
                height: 44px;
                background: {COLORS['primary']}20;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.25rem;
            ">{icon}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_card(title: str, content: str, icon: Optional[str] = None):
    """Renderiza um card genérico."""
    
    icon_html = f"""
    <div style="
        width: 40px;
        height: 40px;
        background: {COLORS['primary']}20;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    ">{icon}</div>
    """ if icon else ""
    
    st.markdown(f"""
    <div class="card">
        <div class="card-header">
            {icon_html}
            <h3 style="margin: 0; font-size: 1rem; color: {COLORS['text_primary']};">{title}</h3>
        </div>
        <div style="color: {COLORS['text_secondary']}; font-size: 0.9rem; line-height: 1.6;">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_section_header(title: str, show_line: bool = True):
    """Renderiza cabeçalho de seção com linha decorativa."""
    
    line_html = f'<div class="line"></div>' if show_line else ""
    
    st.markdown(f"""
    <div class="section-header">
        <h3 style="
            margin: 0;
            font-size: 1rem;
            font-weight: 600;
            color: {COLORS['text_primary']};
            white-space: nowrap;
        ">{title}</h3>
        {line_html}
    </div>
    """, unsafe_allow_html=True)


def render_empty_state(
    title: str,
    description: str,
    icon: str = "📭",
    action_label: Optional[str] = None
):
    """Renderiza estado vazio com call-to-action."""
    
    st.markdown(f"""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem;
        text-align: center;
        background: {COLORS['bg_secondary']};
        border: 1px dashed {COLORS['border']};
        border-radius: 16px;
        animation: fadeIn 0.3s ease-out;
    ">
        <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;">{icon}</div>
        <h3 style="margin: 0 0 0.5rem 0; color: {COLORS['text_primary']};">{title}</h3>
        <p style="margin: 0; color: {COLORS['text_muted']}; max-width: 300px;">{description}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if action_label:
        st.button(action_label, use_container_width=True)


def render_loading_skeleton(height: int = 100):
    """Renderiza skeleton loading animado."""
    
    st.markdown(f"""
    <div style="
        height: {height}px;
        background: linear-gradient(
            90deg,
            {COLORS['bg_tertiary']} 25%,
            {COLORS['bg_secondary']} 50%,
            {COLORS['bg_tertiary']} 75%
        );
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        border-radius: 12px;
    "></div>
    """, unsafe_allow_html=True)


def render_toast(message: str, type: Literal["success", "error", "warning", "info"] = "info"):
    """Renderiza notificação toast."""
    
    colors = {
        "success": (COLORS['success'], COLORS['success_bg'], "✓"),
        "error": (COLORS['error'], COLORS['error_bg'], "✕"),
        "warning": (COLORS['warning'], COLORS['warning_bg'], "⚠"),
        "info": (COLORS['info'], COLORS['info_bg'], "ℹ"),
    }
    
    color, bg, icon = colors[type]
    
    st.markdown(f"""
    <div style="
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: {COLORS['bg_elevated']};
        border: 1px solid {color}40;
        border-left: 4px solid {color};
        border-radius: 12px;
        padding: 1rem 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        box-shadow: {SHADOWS['lg']};
        z-index: 9999;
        animation: fadeIn 0.3s ease-out;
    ">
        <span style="
            width: 24px;
            height: 24px;
            background: {bg};
            color: {color};
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: bold;
        ">{icon}</span>
        <span style="color: {COLORS['text_primary']};">{message}</span>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# CONFIGURATION UI COMPONENTS
# ============================================================================

def render_column_selector(
    all_columns: list,
    selected_columns: list,
    categories: dict = None,
    search_enabled: bool = True
) -> list:
    """
    Renderiza seletor de colunas com busca e categorização.
    
    Args:
        all_columns: Lista de todas as colunas disponíveis
        selected_columns: Lista de colunas atualmente selecionadas
        categories: Dict de categorias {nome: [colunas]}
        search_enabled: Se deve mostrar campo de busca
        
    Returns:
        Lista de colunas selecionadas
    """
    result = selected_columns.copy()
    
    if search_enabled:
        search_term = st.text_input(
            "🔍 Buscar coluna",
            placeholder="Digite para filtrar..."
        )
    else:
        search_term = ""
    
    # Filtra colunas pela busca
    filtered_columns = [
        col for col in all_columns
        if not search_term or search_term.lower() in col.lower()
    ]
    
    if categories:
        # Renderiza por categoria
        for category_name, category_cols in categories.items():
            # Filtra colunas desta categoria
            visible_cols = [
                col for col in category_cols
                if col in filtered_columns
            ]
            
            if visible_cols:
                with st.expander(f"📁 {category_name} ({len(visible_cols)})", expanded=True):
                    for col in visible_cols:
                        is_selected = col in result
                        checked = st.checkbox(
                            col,
                            value=is_selected,
                            key=f"col_{category_name}_{col}"
                        )
                        
                        if checked and col not in result:
                            result.append(col)
                        elif not checked and col in result:
                            result.remove(col)
    else:
        # Listagem simples
        for col in filtered_columns:
            is_selected = col in result
            checked = st.checkbox(col, value=is_selected, key=f"col_{col}")
            
            if checked and col not in result:
                result.append(col)
            elif not checked and col in result:
                result.remove(col)
    
    return result


def render_preset_selector(presets: dict, on_select_callback=None) -> tuple:
    """
    Renderiza seletor de presets de configuração.
    
    Args:
        presets: Dict de presets {nome: {description, columns}}
        on_select_callback: Função callback quando preset é selecionado
        
    Returns:
        tuple: (preset_name, preset_data) ou (None, None)
    """
    preset_names = ["(Personalizado)"] + list(presets.keys())
    
    selected_preset = st.selectbox(
        "📋 Template de Configuração",
        options=preset_names,
        help="Selecione um template predefinido ou personalize"
    )
    
    if selected_preset and selected_preset != "(Personalizado)":
        preset_data = presets[selected_preset]
        
        # Mostra descrição
        st.info(f"ℹ️ {preset_data.get('description', '')}")
        
        # Mostra preview das colunas
        cols = preset_data.get('columns', [])
        if cols:
            st.caption(f"**{len(cols)} colunas** serão selecionadas")
        
        if on_select_callback:
            on_select_callback(selected_preset, preset_data)
        
        return selected_preset, preset_data
    
    return None, None


def render_scope_selector(
    unit: str,
    region: str,
    all_regions: list
) -> tuple:
    """
    Renderiza seletor de escopo de aplicação melhorado.
    
    Args:
        unit: Unidade atual
        region: Região atual
        all_regions: Lista de todas as regiões
        
    Returns:
        tuple: (scope_type, target_description)
    """
    st.subheader("🎯 Escopo de Aplicação")
    
    scope = st.radio(
        "Aplicar estas configurações em:",
        options=[
            "Somente esta unidade",
            "Todas as unidades desta região",
            "Todas as unidades (todas as regiões)"
        ],
        help="Escolha onde as configurações serão aplicadas"
    )
    
    # Feedback visual
    if scope == "Somente esta unidade":
        st.caption(f"✓ Afetará apenas: **{unit}**")
        target_desc = unit
    elif scope == "Todas as unidades desta região":
        st.caption(f"✓ Afetará todas as unidades da região **{region}**")
        target_desc = f"Região {region}"
    else:
        st.caption(f"⚠️ Afetará **TODAS** as unidades de **TODAS** as regiões")
        target_desc = "Todas as regiões"
    
    return scope, target_desc


def _format_month_year(ym: str) -> str:
    """Converte 'AAAA-MM' ou 'YYYY-MM' para 'MM/AAAA'."""
    if ym and '-' in ym:
        y, m = ym.split('-')
        return f"{m}/{y}"
    return ym


def render_config_summary(config_data: dict, column_manager=None):
    """
    Renderiza resumo visual da configuração.
    
    Args:
        config_data: Dados de configuração
        column_manager: Instância do ColumnManager (opcional)
    """
    st.subheader("📊 Resumo da Configuração")
    
    cols = st.columns([1, 1, 1])
    
    # Mês de referência
    with cols[0]:
        month_ref = config_data.get("month_reference", "N/A")
        st.metric("Mês de Referência", _format_month_year(month_ref))
    
    # Número de colunas
    with cols[1]:
        columns = config_data.get("columns", [])
        st.metric("Colunas Selecionadas", len(columns))
    
    # Tipo de relatório
    with cols[2]:
        has_extras = any(
            col for col in columns
            if column_manager and column_manager.is_extra_column(col)
        ) if column_manager else False
        
        report_type = "Completo" if has_extras else "Básico"
        st.metric("Tipo de Relatório", report_type)
    
    # Detalhes adicionais
    if column_manager and columns:
        st.divider()
        stats = column_manager.get_column_stats(columns)
        
        st.caption("**Por Categoria:**")
        for category, count in stats.get("by_category", {}).items():
            st.write(f"• {category}: {count} colunas")


def render_config_diff(old_config: dict, new_config: dict):
    """
    Renderiza diferenças entre duas configurações.
    
    Args:
        old_config: Configuração antiga
        new_config: Configuração nova
    """
    st.subheader("🔄 Mudanças Detectadas")
    
    has_changes = False
    
    # Compara mês
    old_month = old_config.get("month_reference")
    new_month = new_config.get("month_reference")
    
    if old_month != new_month:
        has_changes = True
        st.warning(f"**Mês alterado:** {old_month} → {new_month}")
    
    # Compara colunas
    old_cols = set(old_config.get("columns", []))
    new_cols = set(new_config.get("columns", []))
    
    added = new_cols - old_cols
    removed = old_cols - new_cols
    
    if added:
        has_changes = True
        st.success(f"**{len(added)} colunas adicionadas:**")
        for col in added:
            st.write(f"  + {col}")
    
    if removed:
        has_changes = True
        st.error(f"**{len(removed)} colunas removidas:**")
        for col in removed:
            st.write(f"  - {col}")
    
    if not has_changes:
        st.info("ℹ️ Nenhuma mudança detectada")


def render_copy_config_selector(available_units: list, current_unit: str) -> str:
    """
    Renderiza seletor para copiar configuração de outra unidade.
    
    Args:
        available_units: Lista de unidades disponíveis
        current_unit: Unidade atual
        
    Returns:
        Nome da unidade selecionada ou None
    """
    # Remove unidade atual da lista
    other_units = [u for u in available_units if u != current_unit]
    
    if not other_units:
        st.warning("Nenhuma outra unidade com configuração disponível")
        return None
    
    st.subheader("📋 Copiar de Outra Unidade")
    
    selected_unit = st.selectbox(
        "Selecione a unidade fonte:",
        options=["(Não copiar)"] + other_units,
        help="Copia todas as configurações de outra unidade"
    )
    
    if selected_unit and selected_unit != "(Não copiar)":
        st.info(f"ℹ️ Configurações de **{selected_unit}** serão copiadas")
        return selected_unit
    
    return None

