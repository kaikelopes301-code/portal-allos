import streamlit as st
from portal_streamlit.pages import init_page

# Inicialização da página
config = init_page("Ajuda", "ℹ️")

st.title("Ajuda e Dicas")

st.markdown(
    """
    Execução: rode a automação em modo Dry-run para gerar prévias dos HTMLs. Se tudo ok, rode sem Dry-run para enviar.
    
    Preview: visualize os HTMLs gerados diretamente no navegador do portal.
    
    Configurações: ajuste caminhos, mês/região padrão e crie overrides de texto por unidade.
    
    Logs: consulta rápida do banco SQLite gerado pela automação.
    
    O que já está integrado:
    
    Seleção de Unidades e Colunas pode ser informada na tela Execução (separe por vírgula).
    
    Limitações atuais:
    
    Dúvidas? entre em contato Kaike.costa@atlasinovacoes.com.br
    """
)
