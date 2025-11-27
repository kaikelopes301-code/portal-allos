"""
Portal Streamlit - Sistema de Gestão de Relatórios de Faturamento
==================================================================
Pacote principal do portal Streamlit para automação de relatórios.

Este módulo configura o ambiente e garante que o projeto raiz
esteja disponível no sys.path para todos os submódulos.
"""

import os
import sys
from pathlib import Path

# Setup do path uma única vez para todo o pacote
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

__version__ = "2.0.0"
__author__ = "Atlas Inovações"
