import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def gerar_testes(conteudo_ou_caminho, eh_arquivo=False):
    # Inicializa o modelo potente da sua conta nova
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=0
    )

    # Se for arquivo (uso via terminal), ele lê. Se não, usa a string direto (uso via API).
    if eh_arquivo:
        with open(conteudo_ou_caminho, "r", encoding="utf-8") as f:
            codigo_fonte = f.read()
        nome_referencia = conteudo_ou_caminho
    else:
        codigo_fonte = conteudo_ou_caminho
        nome_referencia = "codigo_enviado.py"

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um especialista em QA. Gere apenas o código de testes unitários com pytest. Não inclua explicações ou textos introdutórios."),
        ("user", "Crie testes para este código, incluindo casos de erro e garantindo o import correto de {arquivo}:\n\n{code}")
    ])

    chain = prompt | llm | StrOutputParser()
    
    print(f"🤖 GPT-4o gerando testes...")
    resultado = chain.invoke({"code": codigo_fonte, "arquivo": nome_referencia})

    # Limpeza do Markdown que o GPT costuma enviar
    conteudo_limpo = resultado.replace("```python", "").replace("```", "").strip()
    if "import " in conteudo_limpo:
        conteudo_limpo = conteudo_limpo[conteudo_limpo.find("import "):]

    # Na API, geralmente não queremos salvar um arquivo físico toda vez, 
    # apenas retornar o texto. Vamos salvar apenas se for via terminal.
    if eh_arquivo:
        nome_teste = f"test_{nome_referencia}"
        with open(nome_teste, "w", encoding="utf-8") as f:
            f.write(conteudo_limpo)
        print(f"✅ Arquivo {nome_teste} criado com sucesso!")

    return conteudo_limpo # A API precisa desse retorno

if __name__ == "__main__":
    # Quando rodar direto o main.py, avisa que é arquivo
    gerar_testes("funcao.py", eh_arquivo=True)