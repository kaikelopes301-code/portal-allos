"""
Serviço de configuração centralizado.
Gerencia presets, validações e aplicação de configurações.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import json
import os

from portal_streamlit.constants import PRESETS, SCOPE_OPTIONS
from portal_streamlit.services.column_manager import ColumnManager
from portal_streamlit.utils.config_manager import (
    get_units_overrides,
    save_unit_override,
    get_config,
    save_config
)


class ConfigService:
    """Serviço centralizado para gerenciamento de configurações."""
    
    def __init__(self):
        self.column_manager = ColumnManager()
        self._history_file = os.path.join(
            os.path.dirname(__file__), "..", "data", "config_history.json"
        )
    
    def get_column_presets(self) -> Dict[str, Dict[str, Any]]:
        """Retorna todos os presets disponíveis."""
        return PRESETS.copy()
    
    def get_preset_names(self) -> List[str]:
        """Retorna lista de nomes de presets."""
        return list(PRESETS.keys())
    
    def get_preset_columns(self, preset_name: str) -> Optional[List[str]]:
        """Retorna as colunas de um preset específico."""
        preset = PRESETS.get(preset_name)
        return preset["columns"].copy() if preset else None
    
    def get_preset_description(self, preset_name: str) -> Optional[str]:
        """Retorna a descrição de um preset."""
        preset = PRESETS.get(preset_name)
        return preset.get("description") if preset else None
    
    def get_unit_config(self, unit_name: str) -> Optional[Dict[str, Any]]:
        """
        Obtém configuração de uma unidade específica.
        
        Args:
            unit_name: Nome da unidade
            
        Returns:
            Dicionário com configuração ou None
        """
        overrides = get_units_overrides()
        return overrides.get(unit_name)
    
    def get_all_units_configs(self) -> Dict[str, Dict[str, Any]]:
        """Retorna configurações de todas as unidades."""
        return get_units_overrides()
    
    def validate_config(self, config_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Valida dados de configuração.
        
        Args:
            config_data: Dicionário com dados de configuração
            
        Returns:
            tuple: (is_valid, error_messages)
        """
        errors = []
        
        # Valida colunas
        if "columns" in config_data:
            columns = config_data["columns"]
            if not isinstance(columns, list):
                errors.append("'columns' deve ser uma lista")
            elif len(columns) == 0:
                errors.append("Deve selecionar pelo menos uma coluna")
            else:
                is_valid, invalid_cols = self.column_manager.validate_columns(columns)
                if not is_valid:
                    errors.append(f"Colunas inválidas: {', '.join(invalid_cols)}")
        
        # Valida mês de referência
        if "month_reference" in config_data:
            month_ref = config_data["month_reference"]
            if not self._validate_month_format(month_ref):
                errors.append(f"Formato de mês inválido: '{month_ref}'. Use AAAA-MM")
        
        return len(errors) == 0, errors
    
    def _validate_month_format(self, month_str: str) -> bool:
        """Valida formato de mês AAAA-MM."""
        import re
        pattern = r"^20\d{2}-(0[1-9]|1[0-2])$"
        return bool(re.match(pattern, str(month_str).strip()))
    
    def apply_config_to_units(
        self,
        config_data: Dict[str, Any],
        target_units: List[str],
        user: str = "system"
    ) -> Tuple[bool, str]:
        """
        Aplica configuração para múltiplas unidades.
        
        Args:
            config_data: Dados de configuração a aplicar
            target_units: Lista de unidades alvo
            user: Usuário que está fazendo a mudança
            
        Returns:
            tuple: (success, message)
        """
        # Valida configuração
        is_valid, errors = self.validate_config(config_data)
        if not is_valid:
            return False, "Erro de validação: " + "; ".join(errors)
        
        # Remove duplicatas preservando ordem
        unique_units = []
        seen = set()
        for unit in target_units:
            if unit not in seen:
                unique_units.append(unit)
                seen.add(unit)
        
        if not unique_units:
            return False, "Nenhuma unidade selecionada"
        
        # Aplica configuração
        try:
            for unit in unique_units:
                save_unit_override(unit, config_data)
            
            # Registra no histórico
            self._log_config_change(
                action="apply_config",
                units=unique_units,
                config=config_data,
                user=user
            )
            
            count = len(unique_units)
            if count == 1:
                return True, f"Configuração aplicada em 1 unidade"
            else:
                return True, f"Configuração aplicada em {count} unidades"
                
        except Exception as e:
            return False, f"Erro ao salvar configuração: {str(e)}"
    
    def copy_config_between_units(
        self,
        source_unit: str,
        target_units: List[str],
        user: str = "system"
    ) -> Tuple[bool, str]:
        """
        Copia configuração de uma unidade para outras.
        
        Args:
            source_unit: Unidade fonte
            target_units: Unidades destino
            user: Usuário fazendo a ação
            
        Returns:
            tuple: (success, message)
        """
        source_config = self.get_unit_config(source_unit)
        if not source_config:
            return False, f"Unidade '{source_unit}' não possui configuração"
        
        return self.apply_config_to_units(source_config, target_units, user)
    
    def get_config_summary(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera resumo visual de uma configuração.
        
        Args:
            config_data: Dados de configuração
            
        Returns:
            Dicionário com informações resumidas
        """
        summary = {
            "month_reference": config_data.get("month_reference", "N/A"),
            "column_count": 0,
            "column_stats": {},
            "has_intro": "intro" in config_data,
            "has_observation": "observation" in config_data,
            "has_subject_template": "subject_template" in config_data
        }
        
        if "columns" in config_data:
            columns = config_data["columns"]
            summary["column_count"] = len(columns)
            summary["column_stats"] = self.column_manager.get_column_stats(columns)
        
        return summary
    
    def get_config_diff(
        self,
        config1: Dict[str, Any],
        config2: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compara duas configurações e retorna diferenças.
        
        Args:
            config1: Primeira configuração
            config2: Segunda configuração
            
        Returns:
            Dicionário com diferenças
        """
        diff = {
            "month_changed": False,
            "columns_added": [],
            "columns_removed": [],
            "other_changes": []
        }
        
        # Compara mês
        month1 = config1.get("month_reference")
        month2 = config2.get("month_reference")
        if month1 != month2:
            diff["month_changed"] = True
            diff["month_old"] = month1
            diff["month_new"] = month2
        
        # Compara colunas
        cols1 = set(config1.get("columns", []))
        cols2 = set(config2.get("columns", []))
        diff["columns_added"] = list(cols2 - cols1)
        diff["columns_removed"] = list(cols1 - cols2)
        
        # Verifica outros campos
        for key in ["intro", "observation", "subject_template"]:
            if config1.get(key) != config2.get(key):
                diff["other_changes"].append(key)
        
        return diff
    
    def _log_config_change(
        self,
        action: str,
        units: List[str],
        config: Dict[str, Any],
        user: str
    ):
        """Registra mudança de configuração no histórico."""
        try:
            # Carrega histórico existente
            history = []
            if os.path.exists(self._history_file):
                with open(self._history_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    history = data.get("history", [])
            
            # Adiciona novo registro
            entry = {
                "timestamp": datetime.now().isoformat(),
                "user": user,
                "action": action,
                "units_affected": units,
                "config": config
            }
            history.append(entry)
            
            # Mantém apenas últimos 100 registros
            if len(history) > 100:
                history = history[-100:]
            
            # Salva histórico
            os.makedirs(os.path.dirname(self._history_file), exist_ok=True)
            with open(self._history_file, "w", encoding="utf-8") as f:
                json.dump({"history": history}, f, ensure_ascii=False, indent=2)
                
        except Exception:
            # Falha silenciosa - histórico é opcional
            pass
    
    def get_config_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Retorna histórico de mudanças de configuração.
        
        Args:
            limit: Número máximo de registros
            
        Returns:
            Lista de registros de histórico
        """
        try:
            if not os.path.exists(self._history_file):
                return []
            
            with open(self._history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                history = data.get("history", [])
                return history[-limit:] if history else []
        except Exception:
            return []
    
    def get_units_with_config(self) -> List[str]:
        """Retorna lista de unidades que possuem configuração."""
        overrides = get_units_overrides()
        return list(overrides.keys())
    
    def get_config_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas gerais sobre configurações."""
        overrides = get_units_overrides()
        
        total_units = len(overrides)
        units_with_custom_month = sum(
            1 for cfg in overrides.values()
            if "month_reference" in cfg
        )
        units_with_custom_columns = sum(
            1 for cfg in overrides.values()
            if "columns" in cfg
        )
        
        return {
            "total_configured_units": total_units,
            "units_with_custom_month": units_with_custom_month,
            "units_with_custom_columns": units_with_custom_columns
        }
