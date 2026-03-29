import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def gerar_testes(arquivo_alvo):
    # Inicializa o modelo potente da sua conta nova
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=0
    )

    with open(arquivo_alvo, "r", encoding="utf-8") as f:
        codigo_fonte = f.read()

    # Prompt ajustado para forçar apenas código no retorno
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um especialista em QA. Gere apenas o código de testes unitários com pytest. Não inclua explicações ou textos introdutórios."),
        ("user", "Crie testes para este código, incluindo casos de erro e garantindo o import correto de {arquivo}:\n\n{code}")
    ])

    chain = prompt | llm | StrOutputParser()
    
    print(f"🤖 GPT-4o gerando testes para {arquivo_alvo}...")
    resultado = chain.invoke({"code": codigo_fonte, "arquivo": arquivo_alvo})

    nome_teste = f"test_{arquivo_alvo}"
    
    with open(nome_teste, "w", encoding="utf-8") as f:
        conteudo = resultado
        
        # 1. Tenta limpar qualquer texto explicativo antes do primeiro import
        if "import " in conteudo:
            conteudo = conteudo[conteudo.find("import "):]
        
        # 2. Remove as marcações de markdown do GPT
        conteudo_limpo = conteudo.replace("```python", "").replace("```", "").strip()
        
        f.write(conteudo_limpo)
    
    print(f"✅ Arquivo {nome_teste} criado com sucesso!")

if __name__ == "__main__":
    # Garanta que o arquivo 'funcao.py' existe e tem código dentro
    gerar_testes("funcao.py")