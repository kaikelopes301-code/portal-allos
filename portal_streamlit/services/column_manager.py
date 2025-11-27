"""
Gerenciador de colunas para relatórios.
Fornece funcionalidades para manipular, validar e categorizar colunas.
"""
from typing import Dict, List, Optional, Set
from portal_streamlit.constants import (
    COLUMN_DEFAULTS,
    COLUMN_EXTRAS,
    COLUMN_CATEGORIES
)


class ColumnManager:
    """Gerenciador centralizado para manipulação de colunas de relatório."""
    
    def __init__(self):
        self._all_columns = COLUMN_DEFAULTS + COLUMN_EXTRAS
        self._column_set = set(self._all_columns)
    
    def get_all_columns(self) -> List[str]:
        """Retorna lista de todas as colunas disponíveis."""
        return self._all_columns.copy()
    
    def get_default_columns(self) -> List[str]:
        """Retorna lista de colunas padrão (recomendadas)."""
        return COLUMN_DEFAULTS.copy()
    
    def get_extra_columns(self) -> List[str]:
        """Retorna lista de colunas extras (opcionais)."""
        return COLUMN_EXTRAS.copy()
    
    def get_column_categories(self) -> Dict[str, List[str]]:
        """Retorna colunas agrupadas por categoria."""
        return {k: v.copy() for k, v in COLUMN_CATEGORIES.items()}
    
    def get_category_for_column(self, column_name: str) -> Optional[str]:
        """Retorna a categoria de uma coluna específica."""
        for category, columns in COLUMN_CATEGORIES.items():
            if column_name in columns:
                return category
        return None
    
    def validate_columns(self, columns: List[str]) -> tuple[bool, List[str]]:
        """
        Valida uma lista de colunas.
        
        Args:
            columns: Lista de nomes de colunas
            
        Returns:
            tuple: (is_valid, invalid_columns)
        """
        if not columns:
            return False, []
        
        invalid = [col for col in columns if col not in self._column_set]
        return len(invalid) == 0, invalid
    
    def filter_columns(self, search_term: str) -> List[str]:
        """
        Filtra colunas por termo de busca.
        
        Args:
            search_term: Termo para buscar nos nomes das colunas
            
        Returns:
            Lista de colunas que correspondem ao termo
        """
        if not search_term:
            return self._all_columns.copy()
        
        term_lower = search_term.lower()
        return [
            col for col in self._all_columns
            if term_lower in col.lower()
        ]
    
    def filter_by_category(self, category: str) -> List[str]:
        """
        Retorna colunas de uma categoria específica.
        
        Args:
            category: Nome da categoria
            
        Returns:
            Lista de colunas da categoria
        """
        return COLUMN_CATEGORIES.get(category, []).copy()
    
    def merge_column_sets(self, *column_lists: List[str]) -> List[str]:
        """
        Mescla múltiplos conjuntos de colunas removendo duplicatas.
        Preserva a ordem de aparição.
        
        Args:
            *column_lists: Listas de colunas para mesclar
            
        Returns:
            Lista única de colunas
        """
        seen: Set[str] = set()
        result = []
        
        for col_list in column_lists:
            for col in col_list:
                if col not in seen and col in self._column_set:
                    seen.add(col)
                    result.append(col)
        
        return result
    
    def get_columns_by_type(self, include_defaults: bool = True, 
                           include_extras: bool = False) -> List[str]:
        """
        Retorna colunas baseado no tipo.
        
        Args:
            include_defaults: Se deve incluir colunas padrão
            include_extras: Se deve incluir colunas extras
            
        Returns:
            Lista de colunas conforme os filtros
        """
        result = []
        if include_defaults:
            result.extend(COLUMN_DEFAULTS)
        if include_extras:
            result.extend(COLUMN_EXTRAS)
        return result
    
    def is_default_column(self, column_name: str) -> bool:
        """Verifica se uma coluna é do tipo padrão."""
        return column_name in COLUMN_DEFAULTS
    
    def is_extra_column(self, column_name: str) -> bool:
        """Verifica se uma coluna é do tipo extra."""
        return column_name in COLUMN_EXTRAS
    
    def get_column_stats(self, selected_columns: List[str]) -> Dict[str, int]:
        """
        Retorna estatísticas sobre colunas selecionadas.
        
        Args:
            selected_columns: Lista de colunas selecionadas
            
        Returns:
            Dict com estatísticas
        """
        total = len(selected_columns)
        defaults = sum(1 for col in selected_columns if col in COLUMN_DEFAULTS)
        extras = sum(1 for col in selected_columns if col in COLUMN_EXTRAS)
        
        # Conta por categoria
        by_category = {}
        for category, cols in COLUMN_CATEGORIES.items():
            count = sum(1 for col in selected_columns if col in cols)
            if count > 0:
                by_category[category] = count
        
        return {
            "total": total,
            "defaults": defaults,
            "extras": extras,
            "by_category": by_category
        }
