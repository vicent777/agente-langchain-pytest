# agente-langchain-pytest

# 🤖 Agente Gerador de Testes Unitários com IA

Este projeto consiste em um agente de Inteligência Artificial capaz de analisar códigos Python e gerar automaticamente arquivos de testes unitários utilizando a biblioteca `pytest`. A solução utiliza **LangChain** para orquestração e **Azure OpenAI** como motor de inferência.

## 🚀 Funcionalidades
- **Análise Automática:** O agente lê arquivos `.py` existentes.
- **Geração de Casos de Teste:** Cria testes para fluxos de sucesso e tratamento de exceções (falhas).
- **Saída Pronta para Uso:** Gera um arquivo `test_<nome>.py` em formato Python puro.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.10+
- **LLM:** Azure OpenAI (GPT-4 ou GPT-3.5)
- **Framework IA:** LangChain
- **Testes:** Pytest

## 📋 Pré-requisitos
Antes de começar, você precisará de uma conta no **Azure** com o serviço **Azure OpenAI** habilitado e um modelo implantado (deployment).

## 🔧 Configuração do Ambiente

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/nome-do-repositorio.git](https://github.com/seu-usuario/nome-do-repositorio.git)
   cd nome-do-repositorio

2. **Crie um ambiente virtual:**
    ```python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate

3. **Instale as dependências:**

    ```pip install -r requirements.txt

4. **Configure as Variáveis de Ambiente:**
    ```Crie um arquivo .env na raiz do projeto:

    AZURE_OPENAI_API_KEY="sua_chave_aqui"
    AZURE_OPENAI_ENDPOINT="[https://seu-recurso.openai.azure.com/](https://seu-recurso.openai.azure.com/)"
    AZURE_OPENAI_DEPLOYMENT_NAME="nome-do-seu-deployment"
    AZURE_OPENAI_API_VERSION="2023-05-15"