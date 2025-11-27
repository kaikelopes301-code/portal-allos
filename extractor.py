# extractor_optimized.py — leitura Excel otimizada com cache

from pathlib import Path
import pandas as pd
import re
from typing import Optional, Tuple
from functools import lru_cache

# Regex pré-compilado
HEADER_CLEANUP = re.compile(r"\s+")


class Extractor:
    def __init__(self, xlsx_dir: Path):
        self.xlsx_dir = Path(xlsx_dir)
        self._sheet_cache = {}  # Cache de abas por arquivo

    def find_workbook(self, regiao: str) -> Optional[Path]:
        """Busca workbook de forma otimizada."""
        patterns = [
            f"*planilha *Medição Mensal*_{regiao}_*.xlsx",
            f"*Medição Mensal*_{regiao}.xlsx",
            f"*Medição*{regiao}*.xlsx",
        ]
        
        # Busca direta por padrões
        for pat in patterns:
            matches = [
                m for m in self.xlsx_dir.glob(pat) 
                if not m.name.startswith("~$")
            ]
            if matches:
                # Ordena por modificação (mais recente primeiro)
                matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                return matches[0]
        
        # Fallback: busca em todos os .xlsx
        target = f"Faturamento {regiao}".lower().strip()
        candidates = [
            p for p in self.xlsx_dir.glob("*.xlsx") 
            if not p.name.startswith("~$")
        ]
        
        for p in candidates:
            try:
                # Usa cache se possível
                sheet_names = self._get_sheet_names(p)
                for s in sheet_names:
                    if s.lower().strip() == target or target in s.lower().strip():
                        return p
            except Exception:
                continue
        
        return None

    @lru_cache(maxsize=10)
    def _get_sheet_names(self, path: Path) -> Tuple[str, ...]:
        """Obtém nomes de abas com cache."""
        try:
            xl = pd.ExcelFile(path)
            return tuple(xl.sheet_names)
        except Exception:
            return tuple()

    def read_region_sheet(
        self, 
        path: Path, 
        regiao: str,
        use_cache: bool = True
    ) -> Tuple[pd.DataFrame, str]:
        """Lê aba regional de forma otimizada."""
        
        # Cache key
        cache_key = f"{path}:{regiao}"
        if use_cache and cache_key in self._sheet_cache:
            return self._sheet_cache[cache_key]
        
        target = f"Faturamento {regiao}".lower().strip()
        sheet_names = self._get_sheet_names(path)
        
        sheet_name = None
        for s in sheet_names:
            if s.lower().strip() == target or target in s.lower().strip():
                sheet_name = s
                break
        
        if sheet_name is None:
            raise RuntimeError(
                f"Aba 'Faturamento {regiao}' não encontrada em {path.name}. "
                f"Abas: {list(sheet_names)}"
            )

        # Leitura otimizada do Excel
        df = pd.read_excel(
            path, 
            sheet_name=sheet_name, 
            dtype=object,
            engine='openpyxl'  # Engine mais rápida
        )

        # Limpeza de cabeçalhos (vetorizada)
        df.columns = [
            HEADER_CLEANUP.sub(" ", str(c).replace("\u00A0", " ").replace("&nbsp;", " ").replace("\r", " ").replace("\n", " ")).strip()
            for c in df.columns
        ]

        # Limpeza de valores (vetorizada quando possível)
        for c in df.columns:
            # Usa vectorized operations do pandas
            df[c] = df[c].fillna("").astype(str).str.strip()
        
        result = (df, sheet_name)
        
        # Armazena no cache
        if use_cache:
            self._sheet_cache[cache_key] = result
        
        return result

    def clear_cache(self):
        """Limpa cache de sheets."""
        self._sheet_cache.clear()