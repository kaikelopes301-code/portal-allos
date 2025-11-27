import os
import sys
import importlib.util
from pathlib import Path
from typing import List, Optional
from functools import lru_cache

# Garante acesso ao projeto raiz (extractor, emailer) e carrega utils.py da raiz
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from extractor import Extractor  # type: ignore

# Carrega funções do utils.py da raiz sem colidir com portal_streamlit.utils
_normalize_unit = None
_parse_year_month = None
_root_utils_path = PROJECT_ROOT / "utils.py"
try:
    if _root_utils_path.exists():
        spec = importlib.util.spec_from_file_location("root_utils", str(_root_utils_path))
        if spec and spec.loader:
            _root_utils = importlib.util.module_from_spec(spec)
            sys.modules["root_utils"] = _root_utils  # ajuda em depuração
            spec.loader.exec_module(_root_utils)  # type: ignore[attr-defined]
            _normalize_unit = getattr(_root_utils, "normalize_unit", None)
            _parse_year_month = getattr(_root_utils, "parse_year_month", None)
except Exception:
    # fallback simples definido abaixo
    _normalize_unit = None
    _parse_year_month = None

def normalize_unit(x: str) -> str:  # type: ignore[override]
    if callable(_normalize_unit):
        try:
            return _normalize_unit(x)
        except Exception:
            pass
    return str(x).strip()

def parse_year_month(x: str) -> Optional[str]:  # type: ignore[override]
    if callable(_parse_year_month):
        try:
            return _parse_year_month(x)
        except Exception:
            pass
    import re
    s = str(x)
    m = re.search(r"(20\d{2})[-/](0?[1-9]|1[0-2])", s)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}"
    return None


def list_output_html_files(output_dir: str) -> List[str]:
    if not output_dir or not os.path.isdir(output_dir):
        return []
    files = [f for f in os.listdir(output_dir) if f.lower().endswith(".html")]
    files.sort()
    return [os.path.join(output_dir, f) for f in files]


def read_html_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Erro ao ler {path}: {e}"


# Constantes privadas
_REGIOES = ["SP1", "SP2", "SP3", "RJ", "NNE"]


def get_regions() -> List[str]:
    """Retorna lista de regiões disponíveis."""
    return _REGIOES

@lru_cache(maxsize=64)
def list_units_for_region(xlsx_dir: str, regiao: str) -> List[str]:
    try:
        ex = Extractor(Path(xlsx_dir))
        wb = ex.find_workbook(regiao)
        if not wb or not wb.exists():
            return []
        df, _ = ex.read_region_sheet(wb, regiao)
        # coleta unidades similares ao main.collect_units
        units = []
        seen = set()
        # heurística: encontrar coluna de unidade
        unit_cols = [c for c in df.columns if str(c).strip().lower().startswith("unidade") or "shopping" in str(c).strip().lower()]
        unit_col = unit_cols[0] if unit_cols else None
        if not unit_col:
            return []
        INVALID_MARKERS = {
            "", "-", "nan", "na", "n/a", "preenchimento pendente", "pendente", "nao informado", "não informado",
        }
        for v in df[unit_col].dropna().astype(str):
            raw = v.strip()
            low = raw.lower()
            if low in INVALID_MARKERS:
                continue
            nu = normalize_unit(raw)
            if nu and nu not in seen:
                seen.add(nu); units.append(raw)
        units.sort()
        return units
    except Exception:
        return []


def sanitize_filename_unit(unidade: str) -> str:
    s = "".join(ch for ch in unidade if ch.isalnum() or ch in {"_","-"," "}).strip()
    return s.replace(" ", "_")

def find_unit_html(output_dir: str, unidade: str, ym: str) -> Optional[str]:
    base = sanitize_filename_unit(unidade)
    candidate = os.path.join(output_dir, f"{base}_{ym}.html")
    return candidate if os.path.exists(candidate) else None
