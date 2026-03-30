# agente-langchain-pytest

# 🤖 Agente Gerador de Testes Unitários com IA

Este projeto implementa um agente de Inteligência Artificial exposto via API REST, capaz de analisar códigos Python e gerar automaticamente testes unitários utilizando a biblioteca `pytest`.

A solução utiliza **FastAPI** para exposição da API e um modelo LLM (Azure OpenAI ou equivalente) para geração automática de testes, executando-os dinamicamente em ambiente isolado.

## 🚀 Funcionalidades
- **Análise automática de código Python**
- **Geração de testes unitários com IA**
- **Cobertura de cenários de sucesso e exceções**
- **Execução automática dos testes com pytest**
- **Retorno estruturado com resultado da execução**
- **Ambiente isolado para execução segura (temporary sandbox)**

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.10+
- **API Framework:** FastAPI
- **LLM:** Azure OpenAI (GPT-4 ou GPT-3.5)
- **Framework IA:** LangChain
- **Testes:** Pytest
- **Servidor ASGI:** Uvicorn
- **Ambiente:** Docker (opcional para deploy)
- **Controle de versão:** Git + GitHub
- **Deploy:** Azure App Service (integração com GitHub / CI-CD)
- **Infraestrutura:** Azure Container Registry (Docker images)

## 📋 Pré-requisitos
Antes de começar, você precisará de uma conta no **Azure** com o serviço **Azure OpenAI** habilitado e um modelo implantado (deployment).

---

## 📡 Endpoint Principal

### `POST /generate-test`

Gera automaticamente testes unitários para o código enviado e executa os testes.

---

### 📥 Exemplo de requisição
```Bash
{
  "source_code": "def somar(a, b):\n    return a + b\n\ndef dividir(a, b):\n    if b == 0:\n        raise ValueError('Não é possível dividir por zero.')\n    return a / b",
  "language": "python"
}


- Exemplo de resposta
```Bash
{
  "status": "success",
  "test_code": "import pytest ...",
  "pytest_output": "... 3 passed in 0.02s",
  "pytest_error": "",
  "return_code": 0
}

## 🔧 Configuração do Ambiente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/vicent777/agente-langchain-pytest.git
   cd agente-langchain-pytest

2. **Crie um ambiente virtual:**
     ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate

3. **Instale as dependências:**
     ```bash
    pip install -r requirements.txt

4. **Configure as Variáveis de Ambiente:**
     ```bash
    Crie um arquivo .env na raiz do projeto:

    AZURE_OPENAI_API_KEY="sua_chave_aqui"
    AZURE_OPENAI_ENDPOINT="https://seu-recurso.openai.azure.com"
    AZURE_OPENAI_DEPLOYMENT_NAME="nome-do-seu-deployment"
    AZURE_OPENAI_API_VERSION="2023-05-15"

## 💻 Como Executar a API
1. **Inicie o servidor:**
    ```Bash
    uvicorn app:app --reload

2. **Acesse a documentação automática.**
    ```Bash
    http://localhost:8000/docs

3. **Usar o endpoint**
    ```Bash
    POST /generate-tests

- Exemplo:
    ```Bash
    {
     "code": "def calcular_bonus(salario): return salario * 0.1"
    }
    
- Resposta esperada:
    ```
4. ****
