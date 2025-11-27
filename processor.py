# processor_optimized.py — processamento otimizado com vetorização

from typing import Dict, Any, List, Tuple, Optional
from decimal import Decimal
import unicodedata
import re
import pandas as pd
import numpy as np
from functools import lru_cache

from utils import (
    fmt_brl,
    PENDENTE_LABELS, 
    PENDENTE_LABELS_NORMALIZED,
    split_emails,
    normalize_unit,
    parse_year_month,
    is_missing_like,    
    parse_brl_money,
    normalize_text_full,
)

# --------------------------
# Constantes (pré-computadas)
# --------------------------
SLA_DESCONTO_CANONICAL = "Desconto SLA Mês"
SLA_DESCONTO_SYNONYMS = [
    "Desc. SLA Mês","Desc. SLA Mês / Equip.","Desc_SLA","Desconto_SLA_Mes",
    "Desconto_SLA_Mês","Desconto SLA Mes","SLA Desconto Mês","Desconto SLA",
]

EXTRA_OPTIONAL_CANONICALS = [
    "Desconto SLA Retroativo","Desconto Equipamentos","Prêmio Assiduidade",
    "Outros descontos","Taxa de prorrogação do prazo pagamento",
    "Valor mensal com prorrogação do prazo pagamento","Retroativo de dissídio",
    "Parcela (x/x)","Valor extras validado Atlas",
]

COLUMN_CANDIDATES = {
    "Unidade": ["Unidade","Shopping","Unidade/Shopping","Unid."],
    "Mes_Emissao_NF": [
        "Mês de emissão da NF","Mês emissão NF","Mes Emissao NF","Mes NF",
        "Competencia NF","Competência NF","Competencia","Competência",
    ],
    "Email_Destinatario": [
        "E-mail","Email","E-mails","Emails","Contatos","Destinatários",
    ],
    "Valor_Mensal_Final": [
        "Valor Mensal Final","Valor Mensal","Total Faturamento","Valor Final",
    ],
    "Contrato": ["Contrato","Número do Pedido","Pedido","OrderNumber"],
    "Funcionario": ["Funcionário","Colaborador"],
    "Status": ["Status","Status do Contrato","Situação"],
}

DEFAULT_DISPLAY_COLUMNS = [
    "Unidade","Categoria","Fornecedor","HC Planilha","Dias Faltas","Horas Atrasos",
    "Valor Planilha","Desc. Falta Validado Atlas","Desc. Atraso Validado Atlas",
    SLA_DESCONTO_CANONICAL,"Valor Mensal Final","Mês referência para faturamento",
    "Mês de emissão da NF",
]

DISPLAY_HEADER_SYNONYMS = {
    "Desc. Falta Validado Atlas": ["Desconto Falta Validado Atlas","Desc_Falta"],
    "Desc. Atraso Validado Atlas": ["Desconto Atraso Validado Atlas","Desc_Atraso"],
    SLA_DESCONTO_CANONICAL: SLA_DESCONTO_SYNONYMS,
    "Desconto SLA Retroativo": [
        "Desc. SLA Retroativo","Desc SLA Retroativo","Retroativo SLA",
        "Desc. SLA Ret.","Desc SLA Ret","SLA Ret.","Retro. SLA",
    ],
}

EXTRA_TOKEN_SETS = {
    "Desconto SLA Retroativo": [
        ["sla","retro"],["retroativo","sla"],["desc","sla","ret"],
    ],
    "Desconto Equipamentos": [["equip"],["equipamentos"]],
}

# Regex pré-compilados
HORAS_PATTERN_1 = re.compile(r"^\s*([+-]?\d+):\s*(\d{1,2})\s*$")
HORAS_PATTERN_2 = re.compile(r"^\s*([+-]?\d+)\s*h\s*(\d{1,2})?\s*m?\s*$", re.IGNORECASE)

# --------------------------
# Funções com cache
# --------------------------
@lru_cache(maxsize=512)
def _norm(s: str) -> str:
    """Normalização com cache."""
    return normalize_text_full(s)


@lru_cache(maxsize=256)
def _key_equiv(s: str) -> str:
    """Chave equivalente com cache."""
    return re.sub(r"[^a-z0-9]", "", _norm(s))


# Sets pré-computados
SLA_DESCONTO_NAMES_NORMALIZED = frozenset(_norm(n) for n in [SLA_DESCONTO_CANONICAL, *SLA_DESCONTO_SYNONYMS])
PENDENTE_LABELS_NORMALIZED = frozenset(_norm(x) for x in PENDENTE_LABELS)


# --------------------------
# Funções de mapeamento (otimizadas)
# --------------------------
def _pick_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    """Busca coluna de forma otimizada."""
    # Normaliza todas as colunas uma vez
    norm_map = {_norm(c): c for c in df.columns}
    
    # Busca exata
    for cand in candidates:
        nc = _norm(cand)
        if nc in norm_map:
            return norm_map[nc]
    
    # Busca parcial
    for cand in candidates:
        nc = _norm(cand)
        if nc:
            for k, original in norm_map.items():
                if nc in k:
                    return original
    return None


def _find_col_by_tokens(df: pd.DataFrame, token_sets: List[List[str]]) -> Optional[str]:
    """Busca por tokens."""
    norm_cols = {c: _norm(c) for c in df.columns}
    for tokens in token_sets:
        toks = [_norm(t) for t in tokens if t]
        for original, n in norm_cols.items():
            if all(t in n for t in toks):
                return original
    return None


def map_columns(df: pd.DataFrame) -> Dict[str, Optional[str]]:
    """Mapeia colunas de forma otimizada."""
    mapping = {key: _pick_column(df, cands) for key, cands in COLUMN_CANDIDATES.items()}
    
    # Fallback para Mês de emissão
    if not mapping.get("Mes_Emissao_NF") or mapping["Mes_Emissao_NF"] not in df.columns:
        aliases = ["mes de emissao da nf", "mes emissao nf", "mes nf"]
        for c in df.columns:
            nc = _norm(c)
            if any(alias in nc for alias in aliases):
                mapping["Mes_Emissao_NF"] = c
                break
    
    if mapping.get("Mes_Emissao_NF"):
        mapping["Mes_Emissão_NF"] = mapping["Mes_Emissao_NF"]
    
    return mapping


# --------------------------
# Processamento vetorizado
# --------------------------
def _vectorized_parse_year_month(series: pd.Series) -> pd.Series:
    """Parse vetorizado de ano/mês."""
    return series.apply(parse_year_month)


def _vectorized_normalize_unit(series: pd.Series) -> pd.Series:
    """Normalização vetorizada de unidades."""
    return series.astype(str).apply(normalize_unit)


def _to_decimal_sane_vectorized(series: pd.Series) -> pd.Series:
    """Conversão vetorizada para Decimal."""
    def convert(x):
        if isinstance(x, Decimal):
            return x if not (x.is_nan() or x.is_infinite()) else Decimal("0")
        if x is None or (isinstance(x, float) and (pd.isna(x) or np.isnan(x) or np.isinf(x))):
            return Decimal("0")
        try:
            return Decimal(str(x))
        except:
            return Decimal("0")
    
    return series.apply(convert)


def _format_horas_atrasos_vectorized(series: pd.Series) -> pd.Series:
    """Formatação vetorizada de horas."""
    def format_val(val):
        if not val or _norm(str(val)) == _norm("Informação pendente"):
            return "Informação pendente"
        
        s = str(val).strip()
        
        # Formato H:MM
        m = HORAS_PATTERN_1.match(s)
        if m:
            try:
                h, mi = int(m.group(1)), int(m.group(2))
                if mi >= 60:
                    h += mi // 60
                    mi = mi % 60
                negative = h < 0
                h = abs(h)
                total_min = h * 60 + mi
                dec = (Decimal(total_min) / Decimal("60")).quantize(Decimal("0.1"))
                if negative:
                    dec = -dec
                return str(dec).replace(".", ",")
            except:
                pass
        
        # Formato 4h 30m
        m = HORAS_PATTERN_2.match(s)
        if m:
            try:
                h = int(m.group(1))
                mi = int(m.group(2)) if m.group(2) else 0
                if mi >= 60:
                    h += mi // 60
                    mi = mi % 60
                negative = h < 0
                h = abs(h)
                total_min = h * 60 + mi
                dec = (Decimal(total_min) / Decimal("60")).quantize(Decimal("0.1"))
                if negative:
                    dec = -dec
                return str(dec).replace(".", ",")
            except:
                pass
        
        # Decimal direto
        raw = s.replace(" ", "")
        if "," in raw:
            raw = raw.replace(",", ".")
        try:
            dec = Decimal(raw).quantize(Decimal("0.1"))
            return str(dec).replace(".", ",")
        except:
            return s
    
    return series.apply(format_val)


def _format_month_year(ym: str) -> str:
    """Converte 'AAAA-MM' ou 'YYYY-MM' para 'MM/AAAA'."""
    if ym and '-' in ym:
        y, m = ym.split('-')
        return f"{m}/{y}"
    return ym


# --------------------------
# Função principal (otimizada)
# --------------------------
def filter_and_prepare(
    df: pd.DataFrame,
    unidade: str,
    ym: str,
    columns_whitelist: Optional[List[str]] = None,
) -> Tuple[List[Dict[str, Any]], List[str], Dict[str, Any]]:
    """Filtra e prepara dados de forma otimizada."""
    
    # 1. Mapeamento de colunas (uma vez)
    mapping = map_columns(df)
    uni_col = mapping.get("Unidade")
    mes_col = mapping.get("Mes_Emissão_NF") or mapping.get("Mes_Emissao_NF")
    email_col = mapping.get("Email_Destinatario")
    vmf_col = mapping.get("Valor_Mensal_Final")

    if not uni_col or not mes_col:
        return [], [], {"row_count": 0, "sum_valor_mensal_final": 0.0}

    # 2. Filtragem por mês (vetorizada)
    ym_series = _vectorized_parse_year_month(df[mes_col])
    dfm = df.loc[ym_series == ym].copy()
    
    if dfm.empty:
        return [], [], {"row_count": 0, "sum_valor_mensal_final": 0.0}

    # 3. Filtragem por unidade (vetorizada)
    target_nu = normalize_unit(unidade)
    dfm["_nu"] = _vectorized_normalize_unit(dfm[uni_col])
    dfu = dfm.loc[dfm["_nu"] == target_nu].copy()
    dfu.drop(columns=["_nu"], errors="ignore", inplace=True)
    
    if dfu.empty:
        return [], [], {"row_count": 0, "sum_valor_mensal_final": 0.0}

    # 4. Processamento de colunas canônicas
    # Mês de emissão da NF (formato MM/YY) e Mês referência (sempre anterior)
    from datetime import date, timedelta
    
    def _format_mmyy(ym_str: str) -> str:
        """Converte YYYY-MM para MM/YY."""
        if not ym_str: return ""
        try:
            # Espera YYYY-MM do parse_year_month
            y, m = ym_str.split('-')
            return f"{m}/{y[2:]}"
        except:
            return ym_str

    def _get_prev_month(ym_str: str) -> str:
        """Retorna YYYY-MM do mês anterior."""
        if not ym_str: return ""
        try:
            y, m = map(int, ym_str.split('-'))
            dt = date(y, m, 1) - timedelta(days=1)
            return f"{dt.year:04d}-{dt.month:02d}"
        except:
            return ym_str

    # Processa Mês de Emissão
    dfu["Mês de emissão da NF"] = dfu[mes_col].apply(
        lambda x: _format_mmyy(parse_year_month(x) or ym)
    )

    # Força Mês de Referência como (Mês da NF - 1)
    # Nota: Usamos 'ym' (que é o filtro do mês da NF) como base se a linha não tiver data válida
    ref_ym = _get_prev_month(ym)
    ref_formatted = _format_mmyy(ref_ym)
    
    # Se a coluna existir, sobrescrevemos. Se não, criamos.
    dfu["Mês referência para faturamento"] = ref_formatted
    
    # Valor Mensal Final (vetorizado)
    if vmf_col and vmf_col in dfu.columns:
        dfu["_vmf_num"] = _to_decimal_sane_vectorized(dfu[vmf_col])
    else:
        dfu["_vmf_num"] = Decimal("0")

    dfu["Valor Mensal Final"] = dfu["_vmf_num"].apply(fmt_brl)

    # Horas Atrasos (vetorizada)
    if "Horas Atrasos" in dfu.columns:
        dfu["Horas Atrasos"] = _format_horas_atrasos_vectorized(dfu["Horas Atrasos"])
    
    # 5. Cálculo de totais (operação única no final)
    total_vmf = dfu["_vmf_num"].sum()
    
    # 6. Coleta de destinatários
    recipients = []
    if email_col and email_col in dfu.columns:
        raw = dfu[email_col].dropna().astype(str).tolist()
        for cell in raw:
            recipients.extend(split_emails(cell) or [])
        recipients = list(dict.fromkeys(recipients))  # Remove duplicatas mantendo ordem
    
    # 7. Montagem de colunas de display
    display_columns = columns_whitelist or DEFAULT_DISPLAY_COLUMNS
    
    # Garante colunas críticas
    for col in ["Valor Mensal Final", "Mês de emissão da NF"]:
        if col not in display_columns:
            display_columns.append(col)
    
    # 8. Conversão para dicionários (operação final)
    df_display = dfu[display_columns].copy() if all(c in dfu.columns for c in display_columns) else dfu
    rows = df_display.to_dict(orient="records")
    
    summary = {
        "row_count": len(rows),
        "sum_valor_mensal_final": float(total_vmf),
        "display_columns": display_columns,
        "missing_columns": [],
        "requested_columns": columns_whitelist or [],
        "fallback_used": False,
    }
    
    return rows, recipients, summary