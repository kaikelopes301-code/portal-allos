"""
Portal Performance - Validadores e Formatadores
=================================================
Funções utilitárias para validação de dados e formatação de mensagens.
Segue princípios SOLID e DRY para maximizar reusabilidade.
"""

import re
from typing import Optional, List, Union, Any
from decimal import Decimal
from pathlib import Path


# ============================================================================
# VALIDATORS - Responsabilidade única de validação
# ============================================================================

class EmailValidator:
    """Validador de endereços de email."""
    
    # RFC 5322 simplified pattern
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    @staticmethod
    def is_valid(email: str) -> bool:
        """
        Valida se uma string é um email válido.
        
        Args:
            email: String a ser validada
            
        Returns:
            True se válido, False caso contrário
            
        Example:
            >>> EmailValidator.is_valid("user@example.com")
            True
            >>> EmailValidator.is_valid("invalid.email")
            False
        """
        if not email or not isinstance(email, str):
            return False
        return bool(EmailValidator.EMAIL_PATTERN.match(email.strip()))
    
    @staticmethod
    def validate_list(emails: List[str]) -> tuple[List[str], List[str]]:
        """
        Valida uma lista de emails e separa válidos de inválidos.
        
        Args:
            emails: Lista de strings de email
            
        Returns:
            Tupla (emails_válidos, emails_inválidos)
            
        Example:
            >>> EmailValidator.validate_list(["user@test.com", "invalid"])
            (["user@test.com"], ["invalid"])
        """
        valid = []
        invalid = []
        
        for email in emails:
            email = email.strip()
            if EmailValidator.is_valid(email):
                valid.append(email)
            else:
                invalid.append(email)
                
        return valid, invalid


class PathValidator:
    """Validador de caminhos de arquivos e diretórios."""
    
    @staticmethod
    def is_valid_path(path: Union[str, Path]) -> bool:
        """
        Verifica se um caminho é válido (não necessariamente existente).
        
        Args:
            path: Caminho a ser validado
            
        Returns:
            True se o caminho é válido
        """
        try:
            Path(path)
            return True
        except (TypeError, ValueError):
            return False
    
    @staticmethod
    def exists(path: Union[str, Path]) -> bool:
        """
        Verifica se um caminho existe no sistema de arquivos.
        
        Args:
            path: Caminho a ser verificado
            
        Returns:
            True se existe
        """
        return Path(path).exists() if PathValidator.is_valid_path(path) else False
    
    @staticmethod
    def is_file(path: Union[str, Path]) -> bool:
        """Verifica se é um arquivo."""
        return Path(path).is_file() if PathValidator.exists(path) else False
    
    @staticmethod
    def is_directory(path: Union[str, Path]) -> bool:
        """Verifica se é um diretório."""
        return Path(path).is_dir() if PathValidator.exists(path) else False


class DataValidator:
    """Validador de dados gerais."""
    
    @staticmethod
    def is_empty(value: Any) -> bool:
        """
        Verifica se um valor é considerado vazio.
        
        Args:
            value: Valor a ser verificado
            
        Returns:
            True se vazio (None, "", [], {}, etc.)
        """
        if value is None:
            return True
        if isinstance(value, str):
            return not value.strip()
        if isinstance(value, (list, dict, tuple, set)):
            return len(value) == 0
        return False
    
    @staticmethod
    def is_numeric(value: Any) -> bool:
        """
        Verifica se um valor pode ser convertido para número.
        
        Args:
            value: Valor a ser verificado
            
        Returns:
            True se pode ser convertido para número
        """
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False


# ============================================================================
# FORMATTERS - Responsabilidade única de formatação
# ============================================================================

class RegionFormatter:
    """Formatador para nomes de regiões."""
    
    REGION_FULL_NAMES = {
        "SP1": "São Paulo 1",
        "SP2": "São Paulo 2",
        "SP3": "São Paulo 3",
        "RJ": "Rio de Janeiro",
        "NNE": "Norte e Nordeste"
    }
    
    @staticmethod
    def to_full_name(region_code: str) -> str:
        """
        Converte código de região para nome completo.
        
        Args:
            region_code: Código da região (ex: "SP1")
            
        Returns:
            Nome completo da região
            
        Example:
            >>> RegionFormatter.to_full_name("SP1")
            "São Paulo 1"
        """
        return RegionFormatter.REGION_FULL_NAMES.get(
            region_code.upper(),
            region_code
        )
    
    @staticmethod
    def format_with_code(region_code: str) -> str:
        """
        Formata região com código e nome completo.
        
        Args:
            region_code: Código da região
            
        Returns:
            Formato "CÓDIGO - Nome Completo"
            
        Example:
            >>> RegionFormatter.format_with_code("SP1")
            "SP1 - São Paulo 1"
        """
        full_name = RegionFormatter.to_full_name(region_code)
        if full_name == region_code:
            return region_code
        return f"{region_code} - {full_name}"


class MessageFormatter:
    """Formatador para mensagens de status e feedback."""
    
    @staticmethod
    def success(message: str, emoji: bool = True) -> str:
        """
        Formata mensagem de sucesso.
        
        Args:
            message: Mensagem a ser formatada
            emoji: Se deve incluir emoji
            
        Returns:
            Mensagem formatada
        """
        prefix = "✅ " if emoji else ""
        return f"{prefix}{message}"
    
    @staticmethod
    def error(message: str, emoji: bool = True) -> str:
        """Formata mensagem de erro."""
        prefix = "❌ " if emoji else ""
        return f"{prefix}{message}"
    
    @staticmethod
    def warning(message: str, emoji: bool = True) -> str:
        """Formata mensagem de aviso."""
        prefix = "⚠️ " if emoji else ""
        return f"{prefix}{message}"
    
    @staticmethod
    def info(message: str, emoji: bool = True) -> str:
        """Formata mensagem informativa."""
        prefix = "ℹ️ " if emoji else ""
        return f"{prefix}{message}"
    
    @staticmethod
    def progress(current: int, total: int, description: str = "") -> str:
        """
        Formata mensagem de progresso.
        
        Args:
            current: Valor atual
            total: Valor total
            description: Descrição opcional
            
        Returns:
            Mensagem formatada de progresso
            
        Example:
            >>> MessageFormatter.progress(5, 10, "processando")
            "processando: 5/10 (50%)"
        """
        percentage = (current / total * 100) if total > 0 else 0
        prefix = f"{description}: " if description else ""
        return f"{prefix}{current}/{total} ({percentage:.0f}%)"


# ============================================================================
# HELPERS - Funções auxiliares específicas
# ============================================================================

class StringHelper:
    """Auxiliar para manipulação de strings."""
    
    @staticmethod
    def truncate(text: str, max_length: int, suffix: str = "...") -> str:
        """
        Trunca texto se exceder tamanho máximo.
        
        Args:
            text: Texto a truncar
            max_length: Tamanho máximo
            suffix: Sufixo para indicar truncamento
            
        Returns:
            Texto truncado se necessário
        """
        if not text or len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def to_snake_case(text: str) -> str:
        """
        Converte texto para snake_case.
        
        Args:
            text: Texto a converter
            
        Returns:
            Texto em snake_case
            
        Example:
            >>> StringHelper.to_snake_case("Hello World")
            "hello_world"
        """
        # Remove caracteres especiais e substitui espaços por underscores
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '_', text)
        return text.lower()
    
    @staticmethod
    def pluralize(count: int, singular: str, plural: Optional[str] = None) -> str:
        """
        Retorna forma singular ou plural baseado na contagem.
        
        Args:
            count: Número de itens
            singular: Forma singular
            plural: Forma plural (se None, adiciona 's')
            
        Returns:
            Texto no plural/singular apropriado
            
        Example:
            >>> StringHelper.pluralize(1, "arquivo")
            "1 arquivo"
            >>> StringHelper.pluralize(5, "arquivo", "arquivos")
            "5 arquivos"
        """
        if plural is None:
            plural = f"{singular}s"
        
        word = singular if count == 1 else plural
        return f"{count} {word}"


class ListHelper:
    """Auxiliar para manipulação de listas."""
    
    @staticmethod
    def chunk(items: List[Any], chunk_size: int) -> List[List[Any]]:
        """
        Divide lista em chunks menores.
        
        Args:
            items: Lista de itens
            chunk_size: Tamanho de cada chunk
            
        Returns:
            Lista de chunks
            
        Example:
            >>> ListHelper.chunk([1,2,3,4,5], 2)
            [[1,2], [3,4], [5]]
        """
        return [
            items[i:i + chunk_size]
            for i in range(0, len(items), chunk_size)
        ]
    
    @staticmethod
    def unique_preserve_order(items: List[Any]) -> List[Any]:
        """
        Remove duplicatas preservando ordem original.
        
        Args:
            items: Lista com possíveis duplicatas
            
        Returns:
            Lista sem duplicatas na ordem original
        """
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    
    @staticmethod
    def safe_get(items: List[Any], index: int, default: Any = None) -> Any:
        """
        Obtém item de lista com índice seguro.
        
        Args:
            items: Lista
            index: Índice
            default: Valor padrão se índice inválido
            
        Returns:
            Item ou valor padrão
        """
        try:
            return items[index]
        except (IndexError, TypeError):
            return default


class ConfigValidator:
    """Validador específico para dados de configuração."""
    
    MONTH_PATTERN = re.compile(r'^20\d{2}-(0[1-9]|1[0-2])$')
    
    @staticmethod
    def validate_month_format(month_str: str) -> bool:
        """
        Valida formato de mês AAAA-MM.
        
        Args:
            month_str: String no formato AAAA-MM
            
        Returns:
            True se válido
            
        Example:
            >>> ConfigValidator.validate_month_format("2025-10")
            True
            >>> ConfigValidator.validate_month_format("2025-13")
            False
        """
        if not month_str or not isinstance(month_str, str):
            return False
        return bool(ConfigValidator.MONTH_PATTERN.match(month_str.strip()))
    
    @staticmethod
    def validate_column_list(columns: List[str], available_columns: List[str]) -> tuple[bool, List[str]]:
        """
        Valida lista de colunas contra lista de colunas disponíveis.
        
        Args:
            columns: Lista de colunas a validar
            available_columns: Lista de colunas válidas
            
        Returns:
            tuple: (is_valid, invalid_columns)
        """
        if not columns or not isinstance(columns, list):
            return False, []
        
        available_set = set(available_columns)
        invalid = [col for col in columns if col not in available_set]
        
        return len(invalid) == 0, invalid
    
    @staticmethod
    def validate_unit_scope(scope: str) -> bool:
        """
        Valida escopo de aplicação de configuração.
        
        Args:
            scope: Escopo selecionado
            
        Returns:
            True se válido
        """
        valid_scopes = [
            "Somente esta unidade",
            "Todas as unidades desta região",
            "Todas as unidades (todas as regiões)"
        ]
        return scope in valid_scopes
    
    @staticmethod
    def sanitize_config_data(config_data: dict) -> dict:
        """
        Sanitiza dados de configuração removendo valores vazios e normalizando.
        
        Args:
            config_data: Dicionário com dados de configuração
            
        Returns:
            Dicionário sanitizado
        """
        sanitized = {}
        
        # Sanitiza colunas
        if "columns" in config_data:
            columns = config_data["columns"]
            if isinstance(columns, list):
                # Remove vazios e duplicatas preservando ordem
                seen = set()
                clean_columns = []
                for col in columns:
                    col_str = str(col).strip()
                    if col_str and col_str not in seen:
                        clean_columns.append(col_str)
                        seen.add(col_str)
                if clean_columns:
                    sanitized["columns"] = clean_columns
        
        # Sanitiza mês de referência
        if "month_reference" in config_data:
            month = str(config_data["month_reference"]).strip()
            if month:
                sanitized["month_reference"] = month
        
        # Copia outros campos mantendo estrutura
        for key in ["intro", "observation", "subject_template"]:
            if key in config_data and config_data[key]:
                value = str(config_data[key]).strip()
                if value:
                    sanitized[key] = value
        
        return sanitized
