"""
Constantes centralizadas para o portal Streamlit.
"""

# Colunas padrão (sempre recomendadas)
COLUMN_DEFAULTS = [
    "Unidade",
    "Categoria",
    "Fornecedor",
    "HC Planilha",
    "Dias Faltas",
    "Horas Atrasos",
    "Valor Planilha",
    "Desc. Falta Validado Atlas",
    "Desc. Atraso Validado Atlas",
    "Desconto SLA Mês",
    "Valor Mensal Final",
    "Mês de emissão da NF",
    "Mês de referência para faturamento"
]

# Colunas extras (opcionais)
COLUMN_EXTRAS = [
    "Desconto SLA Retroativo",
    "Desconto Equipamentos",
    "Prêmio Assiduidade",
    "Outros descontos",
    "Taxa de prorrogação do prazo pagamento",
    "Valor mensal com prorrogação do prazo pagamento",
    "Retroativo de dissídio",
    "Parcela (x/x)",
    "Valor extras validado Atlas"
]

# Categorização de colunas para melhor visualização
COLUMN_CATEGORIES = {
    "Identificação": [
        "Unidade",
        "Categoria",
        "Fornecedor"
    ],
    "Recursos Humanos": [
        "HC Planilha",
        "Dias Faltas",
        "Horas Atrasos"
    ],
    "Valores Base": [
        "Valor Planilha",
        "Valor Mensal Final"
    ],
    "Descontos e Ajustes": [
        "Desc. Falta Validado Atlas",
        "Desc. Atraso Validado Atlas",
        "Desconto SLA Mês",
        "Desconto SLA Retroativo",
        "Desconto Equipamentos",
        "Outros descontos"
    ],
    "Benefícios": [
        "Prêmio Assiduidade"
    ],
    "Financeiro": [
        "Taxa de prorrogação do prazo pagamento",
        "Valor mensal com prorrogação do prazo pagamento",
        "Retroativo de dissídio",
        "Valor extras validado Atlas"
    ],
    "Metadata": [
        "Mês de emissão da NF",
        "Parcela (x/x)"
    ]
}

# Presets de configuração predefinidos
PRESETS = {
    "Padrão": {
        "description": "Configuração padrão com todas as colunas recomendadas",
        "columns": COLUMN_DEFAULTS.copy()
    },
    "Caxias Shopping": {
        "description": "Configuração especial para Caxias Shopping (padrão + prorrogação)",
        "columns": COLUMN_DEFAULTS + [
            "Taxa de prorrogação do prazo pagamento",
            "Valor mensal com prorrogação do prazo pagamento"
        ]
    }
}

# Valores padrão de configuração
DEFAULT_CONFIG_VALUES = {
    "default_regiao": "SP1",
    "default_mes": "2025-08",
    "python_path": "python",
    "main_py_path": "c:/backpperformance/main.py",
    "xlsx_dir": "c:/backpperformance/planilhas",
    "output_html_dir": "c:/backpperformance/output_html"
}

# Opções de escopo para aplicação de configurações
SCOPE_OPTIONS = [
    "Somente esta unidade",
    "Todas as unidades desta região",
    "Todas as unidades (todas as regiões)"
]
