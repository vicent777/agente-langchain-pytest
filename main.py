import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()


# ------------------
# LLM centralizado 
# ------------------
def get_llm():
    return AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=0
    )


# ------------------
# GERA TESTES
# --------------
def gerar_testes(conteudo_ou_caminho, eh_arquivo=False):
    llm = get_llm()

    if eh_arquivo:
        with open(conteudo_ou_caminho, "r", encoding="utf-8") as f:
            codigo_fonte = f.read()
        nome_referencia = conteudo_ou_caminho
    else:
        codigo_fonte = conteudo_ou_caminho
        nome_referencia = "codigo_enviado.py"

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um especialista em QA. Gere apenas código de testes unitários com pytest. Não inclua explicações."),
        ("user", "Crie testes para este código, incluindo casos de erro. Use import correto de {arquivo}:\n\n{code}")
    ])

    chain = prompt | llm | StrOutputParser()

    resultado = chain.invoke({
        "code": codigo_fonte,
        "arquivo": nome_referencia
    })

    conteudo_limpo = resultado.replace("```python", "").replace("```", "").strip()

    if "import " in conteudo_limpo:
        conteudo_limpo = conteudo_limpo[conteudo_limpo.find("import "):]

    if eh_arquivo:
        nome_teste = f"test_{nome_referencia}"
        with open(nome_teste, "w", encoding="utf-8") as f:
            f.write(conteudo_limpo)

    return conteudo_limpo


# -----------------------------
# EXPLICA RESULTADO DO PYTEST
# -----------------------------
def explicar_resultado(pytest_output: str, return_code: int) -> str:
    llm = get_llm()

    response = llm.invoke([
        SystemMessage(content="Você é um engenheiro de QA. Seja claro e objetivo."),
        HumanMessage(content=f"""
Analise o resultado do pytest:

OUTPUT:
{pytest_output}

RETURN CODE:
{return_code}

Responda:
- se passou ou falhou
- quantos testes rodaram
- causa de erro se existir
""")
    ])

    return response.content


# -----------------------------
# SUGERE CORREÇÃO
# -----------------------------
def sugerir_correcao(codigo: str, pytest_output: str, return_code: int) -> str:
    llm = get_llm()

    response = llm.invoke([
        SystemMessage(content="Você é um engenheiro de software especialista em debugging."),
        HumanMessage(content=f"""
Analise o código e o erro dos testes.

CÓDIGO:
{codigo}

OUTPUT DO PYTEST:
{pytest_output}

RETURN CODE:
{return_code}

TAREFA:
- identifique o problema
- explique o motivo do erro
- sugira uma correção no código (mostre o código corrigido)
""")
    ])

    return response.content

if __name__ == "__main__":
    gerar_testes("funcao.py", eh_arquivo=True)