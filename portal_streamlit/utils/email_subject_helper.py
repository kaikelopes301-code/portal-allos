"""
Portal Performance - Email Subject Helper
==========================================
Helper para renderização e validação de assuntos de emails.
Centraliza lógica de templates de assunto seguindo DRY.
"""

import re
from typing import Dict, Any, Tuple, Optional, List


class EmailSubjectHelper:
    """
    Helper para gerenciar assuntos de emails com templates e placeholders.
    
    Segue Single Responsibility Principle - responsável apenas por assuntos.
    """
    
    # Placeholders válidos para templates de assunto
    AVAILABLE_PLACEHOLDERS = {
        "unidade": "Nome da unidade",
        "mes_ref": "Mês referência (formato YYYY-MM)",
        "mes_extenso": "Mês por extenso (ex: Novembro/2025)",
        "regiao": "Código da região (ex: SP1, RJ, NNE)"
    }
    
    # Template padrão se nenhum for fornecido
    DEFAULT_TEMPLATE = "Medição mensal - {unidade} - {mes_extenso}"
    
    # Regex para encontrar placeholders no formato {nome}
    PLACEHOLDER_PATTERN = re.compile(r'\{(\w+)\}')
    
    @classmethod
    def get_default_template(cls) -> str:
        """
        Retorna o template padrão de assunto.
        
        Returns:
            Template padrão
        """
        return cls.DEFAULT_TEMPLATE
    
    @classmethod
    def get_available_placeholders(cls) -> Dict[str, str]:
        """
        Retorna dicionário de placeholders disponíveis e suas descrições.
        
        Returns:
            Dict com {nome_placeholder: descrição}
        """
        return cls.AVAILABLE_PLACEHOLDERS.copy()
    
    @classmethod
    def extract_placeholders(cls, template: str) -> List[str]:
        """
        Extrai todos os placeholders encontrados em um template.
        
        Args:
            template: String do template
            
        Returns:
            Lista de nomes de placeholders encontrados
            
        Example:
            >>> EmailSubjectHelper.extract_placeholders("Oi {nome}, mês {mes}")
            ['nome', 'mes']
        """
        if not template:
            return []
        
        return cls.PLACEHOLDER_PATTERN.findall(template)
    
    @classmethod
    def validate_template(cls, template: str) -> Tuple[bool, Optional[str]]:
        """
        Valida se um template de assunto é válido.
        
        Verifica se todos os placeholders usados são válidos.
        
        Args:
            template: Template a validar
            
        Returns:
            Tupla (is_valid, error_message)
            - is_valid: True se válido
            - error_message: Mensagem de erro se inválido, None se válido
            
        Example:
            >>> EmailSubjectHelper.validate_template("Email - {unidade}")
            (True, None)
            >>> EmailSubjectHelper.validate_template("Email - {invalido}")
            (False, "Placeholder inválido: invalido")
        """
        if not template or not isinstance(template, str):
            return False, "Template não pode ser vazio"
        
        # Extrair placeholders usados
        used_placeholders = cls.extract_placeholders(template)
        
        # Verificar se todos são válidos
        valid_placeholders = set(cls.AVAILABLE_PLACEHOLDERS.keys())
        invalid = [p for p in used_placeholders if p not in valid_placeholders]
        
        if invalid:
            return False, f"Placeholder(s) inválido(s): {', '.join(invalid)}"
        
        return True, None
    
    @classmethod
    def render_subject(
        cls,
        template: str,
        context: Dict[str, Any],
        safe: bool = True
    ) -> str:
        """
        Renderiza template de assunto substituindo placeholders.
        
        Args:
            template: String do template com placeholders
            context: Dicionário com valores para substituição
            safe: Se True, mantém placeholders não encontrados no contexto
            
        Returns:
            Assunto renderizado
            
        Raises:
            ValueError: Se template for inválido e safe=False
            
        Example:
            >>> context = {"unidade": "Shopping ABC", "mes_extenso": "Nov/2025"}
            >>> EmailSubjectHelper.render_subject(
            ...     "Medição - {unidade} - {mes_extenso}",
            ...     context
            ... )
            "Medição - Shopping ABC - Nov/2025"
        """
        if not template:
            template = cls.DEFAULT_TEMPLATE
        
        # Validar template
        is_valid, error = cls.validate_template(template)
        if not is_valid and not safe:
            raise ValueError(f"Template inválido: {error}")
        
        try:
            # Renderizar usando str.format
            rendered = template.format(**context)
            return rendered
        except KeyError as e:
            if safe:
                # Em modo seguro, retorna o template original se falhar
                return template
            else:
                raise ValueError(f"Placeholder não encontrado no contexto: {e}")
    
    @classmethod
    def format_mes_extenso(cls, ym: str) -> str:
        """
        Formata ano-mês (YYYY-MM) para extenso em português.
        
        Args:
            ym: String no formato YYYY-MM (ex: "2025-11")
            
        Returns:
            Mês por extenso (ex: "Novembro/2025")
            
        Example:
            >>> EmailSubjectHelper.format_mes_extenso("2025-11")
            "Novembro/2025"
        """
        PT_BR = [
            "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        
        try:
            # Aceita formatos YYYY-MM ou YYYY/MM
            ym_clean = ym.replace("/", "-")
            parts = ym_clean.split("-")
            
            if len(parts) >= 2:
                year = int(parts[0])
                month = int(parts[1])
                
                if 1 <= month <= 12:
                    return f"{PT_BR[month]}/{year}"
        except (ValueError, IndexError):
            pass
        
        # Fallback se formato inválido
        return ym
    
    @classmethod
    def create_context(
        cls,
        unidade: str,
        mes_ref: str,
        regiao: str
    ) -> Dict[str, str]:
        """
        Cria contexto completo para renderização de assunto.
        
        Args:
            unidade: Nome da unidade
            mes_ref: Mês de referência (YYYY-MM)
            regiao: Código da região
            
        Returns:
            Dicionário com todos os placeholders preenchidos
            
        Example:
            >>> EmailSubjectHelper.create_context("Shop A", "2025-11", "SP1")
            {
                'unidade': 'Shop A',
                'mes_ref': '2025-11',
                'mes_extenso': 'Novembro/2025',
                'regiao': 'SP1'
            }
        """
        return {
            "unidade": unidade,
            "mes_ref": mes_ref,
            "mes_extenso": cls.format_mes_extenso(mes_ref),
            "regiao": regiao
        }
    
    @classmethod
    def render_with_defaults(
        cls,
        template: Optional[str],
        unidade: str,
        mes_ref: str,
        regiao: str
    ) -> str:
        """
        Renderiza assunto com template e contexto, usando defaults quando necessário.
        
        Função de conveniência que combina create_context e render_subject.
        
        Args:
            template: Template do assunto (usa padrão se None)
            unidade: Nome da unidade
            mes_ref: Mês de referência
            regiao: Código da região
            
        Returns:
            Assunto renderizado
        """
        if not template:
            template = cls.DEFAULT_TEMPLATE
        
        context = cls.create_context(unidade, mes_ref, regiao)
        return cls.render_subject(template, context, safe=True)


# Função de conveniência para compatibilidade
def render_email_subject(
    template: str,
    unidade: str,
    mes_ref: str,
    regiao: str
) -> str:
    """
    Função de conveniência para renderizar assunto de email.
    
    Args:
        template: Template do assunto
        unidade: Nome da unidade
        mes_ref: Mês de referência (YYYY-MM)
        regiao: Código da região
        
    Returns:
        Assunto renderizado
        
    Example:
        >>> render_email_subject(
        ...     "Faturamento {unidade} - {mes_extenso}",
        ...     "Shopping ABC",
        ...     "2025-11",
        ...     "SP1"
        ... )
        "Faturamento Shopping ABC - Novembro/2025"
    """
    return EmailSubjectHelper.render_with_defaults(
        template, unidade, mes_ref, regiao
    )
