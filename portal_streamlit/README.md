# Portal Streamlit - Sistema de Gestão de Relatórios

Interface web Streamlit para automação de relatórios de faturamento Atlas.

## 📁 Estrutura

```
portal_streamlit/
├── __init__.py              # Inicialização do pacote e configuração de paths
├── app.py                   # Ponto de entrada principal
├── requirements.txt         # Dependências Python
├── data/                    # Dados e configurações
│   ├── config.json         # Configurações gerais
│   ├── overrides.json      # Overrides por unidade
│   └── logo-atlas.png      # Logo da empresa
├── pages/                   # Páginas do portal
│   ├── __init__.py         # Funções compartilhadas (init_page)
│   ├── 1_Execução.py       # Execução do pipeline
│   ├── 2_Preview.py        # Preview de emails HTML
│   ├── 3_Configurações.py  # Configurações do sistema
│   ├── 4_Logs.py           # Visualização de logs
│   └── 5_Ajuda.py          # Ajuda e documentação
└── utils/                   # Utilitários
    ├── __init__.py
    ├── config_manager.py   # Gerenciamento de configurações
    ├── pipeline.py         # Funções de pipeline e extração
    └── ui.py               # Design System e componentes UI
```

## 🚀 Como Executar

### Pré-requisitos

```bash
# Instalar dependências
pip install -r requirements.txt
```

### Execução

```bash
# A partir do diretório raiz do projeto
python -m streamlit run portal_streamlit/app.py

# Ou a partir do diretório portal_streamlit
streamlit run app.py
```

O portal abrirá automaticamente em `http://localhost:8501`.

## 📖 Funcionalidades

### 1. Execução do Pipeline
- Seleção de região e unidades
- Modo Dry-Run (simulação)
- Modo Produção (envio real via SendGrid)
- Monitoramento em tempo real
- Logs detalhados

### 2. Preview
- Visualização de emails HTML gerados
- Edição de introdução e observação por unidade
- Auto-save de alterações
- Preview em tempo real

### 3. Configurações
- Configuração de colunas do relatório
- Definição de mês de referência
- Aplicação de preferências por unidade, região ou global

### 4. Logs
- Consulta ao banco de dados de logs
- Filtros por região, unidade e status
- Visualização de histórico de execuções

### 5. Ajuda
- Documentação do sistema
- Dicas de uso

## 🎨 Design System

O portal utiliza um Design System profissional v2.0 com:
- Paleta de cores consistente
- Tokens de design (spacing, typography, shadows)
- Componentes reutilizáveis
- Tema dark OLED
- Animações e transições suaves

## ⚙️ Configuração

### config.json
```json
{
  "python_path": "python",
  "main_py_path": "c:/backpperformance/main.py",
  "xlsx_dir": "c:/backpperformance/planilhas",
  "output_html_dir": "c:/backpperformance/output_html",
  "default_regiao": "SP1",
  "default_mes": "2025-08"
}
```

### overrides.json
Armazena configurações específicas por unidade:
```json
{
  "Nome da Unidade": {
    "intro": "Texto de introdução customizado",
    "observation": "Observação customizada",
    "columns": ["Coluna1", "Coluna2"],
    "month_reference": "2025-08"
  }
}
```

## 🔧 Desenvolvimento

### Estrutura de Código

Todas as páginas seguem o padrão:
```python
from portal_streamlit.pages import init_page

# Inicialização simplificada
config = init_page("Nome da Página", "🎯")

# Resto do código da página...
```

### Componentes UI Disponíveis
```python
from portal_streamlit.utils.ui import (
    render_page_header,
    render_stat_card,
    render_card,
    render_section_header,
    render_empty_state,
    render_loading_skeleton,
    render_toast,
)
```

## 📝 Versão

**v2.0.0** - Refatoração Profissional
- ✅ Código duplicado removido
- ✅ Padrões de inicialização centralizados
- ✅ Funções não utilizadas removidas
- ✅ Imports padronizados
- ✅ Design System profissional

---

**Desenvolvido por:** Atlas Inovações  
**Contato:** Kaike.costa@atlasinovacoes.com.br
