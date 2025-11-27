"""
Portal Performance - Template Helper
=====================================
Funções auxiliares para manipulação de templates HTML e substituição de placeholders.
Centraliza lógica de renderização de templates evitando duplicação.
"""

import re
from typing import Dict, Any, Optional
from pathlib import Path


class TemplateRenderer:
    """
    Renderizador de templates HTML com substituição de placeholders.
    
    Segue o padrão Single Responsibility Principle (SRP).
    """
    
    # Padrão para detectar placeholders {{ nome }}
    PLACEHOLDER_PATTERN = re.compile(r'\{\{\s*(\w+)\s*\}\}')
    
    def __init__(self, template_path: Optional[Path] = None):
        """
        Inicializa o renderizador.
        
        Args:
            template_path: Caminho para arquivo de template (opcional)
        """
        self.template_path = template_path
        self._template_cache: Optional[str] = None
    
    def load_template(self, path: Optional[Path] = None) -> str:
        """
        Carrega template de arquivo.
        
        Args:
            path: Caminho do template (usa self.template_path se None)
            
        Returns:
            Conteúdo do template
            
        Raises:
            FileNotFoundError: Se template não existe
        """
        template_file = path or self.template_path
        
        if not template_file:
            raise ValueError("Nenhum caminho de template fornecido")
        
        template_path_obj = Path(template_file)
        
        if not template_path_obj.exists():
            raise FileNotFoundError(f"Template não encontrado: {template_file}")
        
        with open(template_path_obj, 'r', encoding='utf-8') as f:
            self._template_cache = f.read()
        
        return self._template_cache
    
    def render(
        self,
        template: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        safe: bool = True
    ) -> str:
        """
        Renderiza template substituindo placeholders.
        
        Args:
            template: String do template (usa cached se None)
            context: Dicionário com valores para substituição
            safe: Se True, mantém placeholders não encontrados no contexto
            
        Returns:
            Template renderizado
            
        Example:
            >>> renderer = TemplateRenderer()
            >>> renderer.render("Olá {{ nome }}", {"nome": "João"})
            "Olá João"
        """
        content = template or self._template_cache
        
        if not content:
            raise ValueError("Nenhum template fornecido ou carregado")
        
        context = context or {}
        
        def replace_placeholder(match):
            placeholder_name = match.group(1)
            value = context.get(placeholder_name)
            
            # Se safe=True e valor não existe, mantém placeholder original
            if value is None and safe:
                return match.group(0)
            
            # Converte valor para string
            return str(value) if value is not None else ""
        
        return self.PLACEHOLDER_PATTERN.sub(replace_placeholder, content)
    
    def render_from_file(
        self,
        path: Path,
        context: Optional[Dict[str, Any]] = None,
        safe: bool = True
    ) -> str:
        """
        Carrega e renderiza template em uma única operação.
        
        Args:
            path: Caminho do arquivo template
            context: Contexto para substituição
            safe: Modo seguro (mantém placeholders não encontrados)
            
        Returns:
            Template renderizado
        """
        template = self.load_template(path)
        return self.render(template, context, safe)
    
    def get_placeholders(self, template: Optional[str] = None) -> set:
        """
        Extrai todos os placeholders encontrados no template.
        
        Args:
            template: String do template (usa cached se None)
            
        Returns:
            Set com nomes de placeholders
            
        Example:
            >>> renderer = TemplateRenderer()
            >>> renderer.get_placeholders("{{ nome }} e {{ idade }}")
            {'nome', 'idade'}
        """
        content = template or self._template_cache
        
        if not content:
            return set()
        
        return {match.group(1) for match in self.PLACEHOLDER_PATTERN.finditer(content)}


class HTMLCleaner:
    """
    Limpeza e sanitização de HTML.
    
    Útil para preparar conteúdo antes de envio por email ou exibição.
    """
    
    # Tags HTML permitidas (whitelist básica)
    ALLOWED_TAGS = {
        'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li', 'a', 'img', 'div', 'span', 'table', 'tr', 'td', 'th'
    }
    
    @staticmethod
    def strip_comments(html: str) -> str:
        """
        Remove comentários HTML.
        
        Args:
            html: String HTML
            
        Returns:
            HTML sem comentários
        """
        return re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    
    @staticmethod
    def minify(html: str) -> str:
        """
        Minifica HTML removendo espaços desnecessários.
        
        Args:
            html: String HTML
            
        Returns:
            HTML minificado
            
        Note:
            Não remove espaços dentro de tags <pre> ou <code>
        """
        # Remove múltiplos espaços em branco
        html = re.sub(r'\s+', ' ', html)
        
        # Remove espaços entre tags
        html = re.sub(r'>\s+<', '><', html)
        
        return html.strip()
    
    @staticmethod
    def extract_text(html: str) -> str:
        """
        Extrai apenas texto de HTML (remove todas as tags).
        
        Args:
            html: String HTML
            
        Returns:
            Texto sem tags HTML
        """
        # Remove tags
        text = re.sub(r'<[^>]+>', '', html)
        
        # Normaliza espaços
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    @staticmethod
    def add_inline_styles(html: str, styles: Dict[str, str]) -> str:
        """
        Adiciona estilos inline a tags específicas.
        
        Args:
            html: String HTML
            styles: Dicionário {tag: style_string}
            
        Returns:
            HTML com estilos inline
            
        Example:
            >>> HTMLCleaner.add_inline_styles(
            ...     "<p>Texto</p>",
            ...     {"p": "color: blue; font-size: 14px;"}
            ... )
            '<p style="color: blue; font-size: 14px;">Texto</p>'
        """
        result = html
        
        for tag, style in styles.items():
            # Adiciona style apenas se tag não tem style já definido
            pattern = rf'<{tag}(?!\s+style=)([^>]*)>'
            replacement = rf'<{tag} style="{style}"\1>'
            result = re.sub(pattern, replacement, result)
        
        return result


class EmailTemplateTagger:
    """
    Gerador de tags dinâmicas para templates de email.
    
    Centraliza criação de componentes HTML comuns em emails.
    """
    
    @staticmethod
    def create_button(
        text: str,
        url: str,
        bg_color: str = "#6366F1",
        text_color: str = "#FFFFFF"
    ) -> str:
        """
        Cria um botão HTML compatível com email.
        
        Args:
            text: Texto do botão
            url: Link do botão
            bg_color: Cor de fundo
            text_color: Cor do texto
            
        Returns:
            HTML do botão
        """
        return f"""
        <table border="0" cellpadding="0" cellspacing="0" role="presentation">
            <tr>
                <td style="border-radius: 8px; background-color: {bg_color};">
                    <a href="{url}" style="
                        display: inline-block;
                        padding: 12px 24px;
                        font-size: 14px;
                        font-weight: 600;
                        color: {text_color};
                        text-decoration: none;
                        border-radius: 8px;
                    ">{text}</a>
                </td>
            </tr>
        </table>
        """
    
    @staticmethod
    def create_alert_box(
        message: str,
        type: str = "info",
        title: Optional[str] = None
    ) -> str:
        """
        Cria caixa de alerta estilizada.
        
        Args:
            message: Mensagem do alerta
            type: Tipo (info, success, warning, error)
            title: Título opcional
            
        Returns:
            HTML do alerta
        """
        colors = {
            "info": {"bg": "#EEF2FF", "border": "#6366F1", "text": "#3730A3"},
            "success": {"bg": "#F0FDF4", "border": "#22C55E", "text": "#166534"},
            "warning": {"bg": "#FFFBEB", "border": "#F59E0B", "text": "#92400E"},
            "error": {"bg": "#FEF2F2", "border": "#EF4444", "text": "#991B1B"},
        }
        
        color_scheme = colors.get(type, colors["info"])
        
        title_html = f"<strong>{title}</strong><br>" if title else ""
        
        return f"""
        <div style="
            background: {color_scheme['bg']};
            border-left: 4px solid {color_scheme['border']};
            border-radius: 8px;
            padding: 16px;
            margin: 16px 0;
            color: {color_scheme['text']};
        ">
            {title_html}{message}
        </div>
        """
    
    @staticmethod
    def create_divider(color: str = "#E5E7EB", margin: str = "24px 0") -> str:
        """
        Cria divisor horizontal.
        
        Args:
            color: Cor da linha
            margin: Margem CSS
            
        Returns:
            HTML do divisor
        """
        return f'<hr style="border: none; border-top: 1px solid {color}; margin: {margin};">'
    
    @staticmethod
    def create_table_row(cells: list, is_header: bool = False) -> str:
        """
        Cria linha de tabela HTML.
        
        Args:
            cells: Lista de valores das células
            is_header: Se é linha de cabeçalho
            
        Returns:
            HTML da linha
        """
        tag = "th" if is_header else "td"
        style = "font-weight: bold; background: #F3F4F6;" if is_header else ""
        
        cells_html = "".join([
            f'<{tag} style="padding: 12px; border: 1px solid #E5E7EB; {style}">{cell}</{tag}>'
            for cell in cells
        ])
        
        return f"<tr>{cells_html}</tr>"


# ============================================================================
# FUNÇÕES DE CONVENIÊNCIA
# ============================================================================

def render_template(template: str, **kwargs) -> str:
    """
    Função de conveniência para renderização rápida.
    
    Args:
        template: String do template
        **kwargs: Valores para substituição
        
    Returns:
        Template renderizado
        
    Example:
        >>> render_template("Olá {{ nome }}", nome="Maria")
        "Olá Maria"
    """
    renderer = TemplateRenderer()
    return renderer.render(template, kwargs)


def clean_html(html: str, minify: bool = False, strip_comments: bool = True) -> str:
    """
    Função de conveniência para limpeza de HTML.
    
    Args:
        html: String HTML
        minify: Se deve minificar
        strip_comments: Se deve remover comentários
        
    Returns:
        HTML limpo
    """
    result = html
    
    if strip_comments:
        result = HTMLCleaner.strip_comments(result)
    
    if minify:
        result = HTMLCleaner.minify(result)
    
    return result
