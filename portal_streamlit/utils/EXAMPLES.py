"""
Exemplos de Uso das Novas Utilidades
=====================================
Este arquivo demonstra como usar as funções utilitárias adicionadas ao projeto.
"""

# ============================================================================
# 1. VALIDAÇÃO DE EMAILS
# ============================================================================

from portal_streamlit.utils import EmailValidator

# Validar um único email
email = "usuario@example.com"
if EmailValidator.is_valid(email):
    print(f"✅ {email} é válido")
else:
    print(f"❌ {email} é inválido")

# Validar lista de emails (útil para processar múltiplos destinatários)
emails_para_validar = [
    "contato@atlasinovacoes.com.br",
    "email_invalido",
    "outro@valid.com",
    "sem_arroba.com"
]

validos, invalidos = EmailValidator.validate_list(emails_para_validar)
print(f"\n📧 Emails válidos: {validos}")
print(f"⚠️ Emails inválidos: {invalidos}")


# ============================================================================
# 2. FORMATAÇÃO DE MENSAGENS
# ============================================================================

from portal_streamlit.utils import MessageFormatter

# Mensagens de status (útil para Streamlit)
print("\n" + MessageFormatter.success("Relatório enviado com sucesso!"))
print(MessageFormatter.error("Falha ao processar planilha"))
print(MessageFormatter.warning("Alguns dados estão pendentes"))
print(MessageFormatter.info("Processando 10 unidades..."))

# Progresso (substitui formatações manuais)
total_unidades = 15
for processadas in [3, 7, 12, 15]:
    msg = MessageFormatter.progress(processadas, total_unidades, "Enviando emails")
    print(msg)


# ============================================================================
# 3. FORMATAÇÃO DE REGIÕES
# ============================================================================

from portal_streamlit.utils import RegionFormatter

regioes = ["SP1", "SP2", "RJ", "NNE"]

print("\n🗺️ Regiões:")
for regiao in regioes:
    print(f"  - {RegionFormatter.format_with_code(regiao)}")


# ============================================================================
# 4. HELPERS DE STRING
# ============================================================================

from portal_streamlit.utils import StringHelper

# Truncar textos longos (útil para exibição em tabelas)
texto_longo = "Este é um texto muito longo que precisa ser truncado para exibição"
print(f"\n✂️ Texto truncado: {StringHelper.truncate(texto_longo, 30)}")

# Converter para snake_case (útil para nomes de arquivo)
nome_unidade = "Shopping Center ABC"
arquivo = StringHelper.to_snake_case(nome_unidade) + ".html"
print(f"📁 Nome do arquivo: {arquivo}")

# Pluralização automática (mensagens mais naturais)
for count in [0, 1, 5]:
    msg = StringHelper.pluralize(count, "unidade", "unidades")
    print(f"  {msg} processada(s)")


# ============================================================================
# 5. HELPERS DE LISTA
# ============================================================================

from portal_streamlit.utils import ListHelper

# Dividir em chunks (útil para processar em lotes)
unidades = ["SP1-A", "SP1-B", "SP2-A", "SP2-B", "RJ-A", "RJ-B", "NNE-A"]
chunks = ListHelper.chunk(unidades, 3)
print(f"\n📦 Unidades divididas em lotes de 3:")
for i, chunk in enumerate(chunks, 1):
    print(f"  Lote {i}: {chunk}")

# Remover duplicatas mantendo ordem
lista_com_duplicatas = ["SP1", "RJ", "SP1", "SP2", "RJ", "SP3"]
lista_unica = ListHelper.unique_preserve_order(lista_com_duplicatas)
print(f"\n🔍 Removendo duplicatas:")
print(f"  Original: {lista_com_duplicatas}")
print(f"  Única: {lista_unica}")

# Acesso seguro a índices
lista = ["primeiro", "segundo", "terceiro"]
print(f"\n🔒 Acesso seguro:")
print(f"  Índice 1: {ListHelper.safe_get(lista, 1)}")  # "segundo"
print(f"  Índice 10: {ListHelper.safe_get(lista, 10, default='N/A')}")  # "N/A"


# ============================================================================
# 6. RENDERIZAÇÃO DE TEMPLATES
# ============================================================================

from portal_streamlit.utils import TemplateRenderer, render_template

# Uso simples
saudacao = render_template(
    "Olá {{ nome }}, você tem {{ mensagens }} mensagem(ns) nova(s)!",
    nome="João",
    mensagens=3
)
print(f"\n📧 Template renderizado: {saudacao}")

# Uso avançado com arquivo
renderer = TemplateRenderer()
template_email = """
<html>
<body>
    <h1>Relatório de {{ mes }}</h1>
    <p>Unidade: {{ unidade }}</p>
    <p>Região: {{ regiao }}</p>
    <p>Faturamento: {{ valor }}</p>
</body>
</html>
"""

html_renderizado = renderer.render(template_email, {
    "mes": "Novembro/2025",
    "unidade": "Shopping ABC",
    "regiao": "SP1 - São Paulo 1",
    "valor": "R$ 1.234.567,89"
})

print("\n📄 Template HTML renderizado:")
print(html_renderizado[:150] + "...")

# Listar placeholders
placeholders = renderer.get_placeholders(template_email)
print(f"\n🔍 Placeholders encontrados: {placeholders}")


# ============================================================================
# 7. LIMPEZA DE HTML
# ============================================================================

from portal_streamlit.utils import HTMLCleaner, clean_html

# Remover comentários
html_com_comentarios = """
<!-- Este é um comentário -->
<p>Conteúdo visível</p>
<!-- Outro comentário -->
"""
html_limpo = HTMLCleaner.strip_comments(html_com_comentarios)
print(f"\n🧹 HTML sem comentários:")
print(html_limpo)

# Minificar (remover espaços desnecessários)
html_espacado = """
<div>
    <p>  Texto  com  espaços  </p>
    <span>  Outro  elemento  </span>
</div>
"""
html_minificado = HTMLCleaner.minify(html_espacado)
print(f"\n⚡ HTML minificado:")
print(html_minificado)

# Extrair apenas texto
html_complexo = "<div><h1>Título</h1><p>Parágrafo com <strong>negrito</strong> e <em>itálico</em>.</p></div>"
texto_puro = HTMLCleaner.extract_text(html_complexo)
print(f"\n📝 Texto extraído: {texto_puro}")

# Função de conveniência
html_final = clean_html(
    "<!-- comentário --><p>  Texto  com  espaços  </p>",
    minify=True,
    strip_comments=True
)
print(f"✨ HTML limpo final: {html_final}")


# ============================================================================
# 8. COMPONENTES DE EMAIL
# ============================================================================

from portal_streamlit.utils import EmailTemplateTagger

# Criar botão
botao = EmailTemplateTagger.create_button(
    text="Acessar Relatório Completo",
    url="https://portal.atlasinovacoes.com.br/relatorio",
    bg_color="#6366F1",
    text_color="#FFFFFF"
)
print("\n🔘 Botão HTML criado:")
print(botao[:100] + "...")

# Criar caixa de alerta
alerta_info = EmailTemplateTagger.create_alert_box(
    message="Os dados deste relatório são referentes ao mês de Novembro/2025.",
    type="info",
    title="Informação"
)
print("\nℹ️ Alerta criado:")
print(alerta_info[:100] + "...")

# Criar divisor
divisor = EmailTemplateTagger.create_divider(color="#E5E7EB", margin="24px 0")
print(f"\n➖ Divisor: {divisor}")

# Criar tabela
header = EmailTemplateTagger.create_table_row(
    ["Unidade", "Região", "Faturamento"],
    is_header=True
)
linha1 = EmailTemplateTagger.create_table_row(
    ["Shopping ABC", "SP1", "R$ 123.456,78"],
    is_header=False
)

tabela_completa = f"""
<table style="width: 100%; border-collapse: collapse;">
    {header}
    {linha1}
</table>
"""
print("\n📊 Tabela criada:")
print(tabela_completa[:150] + "...")


# ============================================================================
# 9. VALIDAÇÃO DE CAMINHOS
# ============================================================================

from portal_streamlit.utils import PathValidator

# Verificar se caminhos existem
caminhos = [
    "c:/backpperformance/main.py",
    "c:/backpperformance/planilhas",
    "c:/caminho/inexistente.txt"
]

print("\n📁 Validação de caminhos:")
for caminho in caminhos:
    exists = PathValidator.exists(caminho)
    tipo = ""
    if exists:
        if PathValidator.is_file(caminho):
            tipo = " (arquivo)"
        elif PathValidator.is_directory(caminho):
            tipo = " (diretório)"
    
    status = "✅" if exists else "❌"
    print(f"  {status} {caminho}{tipo}")


# ============================================================================
# 10. VALIDAÇÃO DE DADOS
# ============================================================================

from portal_streamlit.utils import DataValidator

# Verificar valores vazios
valores = [None, "", "  ", [], {}, "texto", [1, 2], 0]

print("\n🔍 Verificação de valores vazios:")
for valor in valores:
    vazio = DataValidator.is_empty(valor)
    status = "Vazio" if vazio else "Com valor"
    print(f"  {repr(valor):20} -> {status}")

# Verificar se é numérico
valores_para_testar = ["123", "45.67", "-89", "abc", "12.34.56", None]

print("\n🔢 Verificação de valores numéricos:")
for valor in valores_para_testar:
    numerico = DataValidator.is_numeric(valor)
    status = "✅ Numérico" if numerico else "❌ Não numérico"
    print(f"  {str(valor):15} -> {status}")


# ============================================================================
# EXEMPLO INTEGRADO: PROCESSAMENTO DE EMAILS
# ============================================================================

print("\n" + "="*70)
print("EXEMPLO INTEGRADO: Processamento de Emails")
print("="*70)

# Simular dados de entrada
emails_raw = [
    "admin@atlasinovacoes.com.br",
    "email_invalido",
    "contato@empresa.com",
    "",
    "outro@valido.com.br"
]

# 1. Validar emails
validos, invalidos = EmailValidator.validate_list(emails_raw)

# 2. Formatar mensagem de resultado
total = len(emails_raw)
count_validos = len(validos)
count_invalidos = len(invalidos)

print(MessageFormatter.info(f"Processando {total} emails..."))
print(MessageFormatter.success(f"Encontrados {count_validos} emails válidos"))
if invalidos:
    print(MessageFormatter.warning(f"Encontrados {count_invalidos} emails inválidos: {invalidos}"))

# 3. Dividir em lotes para envio
batch_size = 2
lotes = ListHelper.chunk(validos, batch_size)

print(f"\n📤 Emails serão enviados em {len(lotes)} lotes de até {batch_size} emails:")
for i, lote in enumerate(lotes, 1):
    print(f"  Lote {i}: {lote}")

# 4. Simular envio com progresso
print("\n📧 Simulando envio...")
for i, email in enumerate(validos, 1):
    progresso = MessageFormatter.progress(i, count_validos, "Enviando")
    print(f"  {progresso} -> {email}")

print("\n" + MessageFormatter.success("Processamento concluído!"))

print("\n" + "="*70)
