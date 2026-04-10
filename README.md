# agente-langchain-pytest

# 🤖 AI QA Agent: Gerador e Executor de Testes com IA

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Azure](https://img.shields.io/badge/Azure-App%20Service%20%26%20ACR-0078D4?style=for-the-badge&logo=microsoftazure)](https://azure.microsoft.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)

Este projeto implementa um **Agente de IA Autônomo** capaz de analisar códigos Python, gerar testes unitários via LLM (Azure OpenAI) e executá-los dinamicamente utilizando `pytest`. A solução foi projetada para funcionar tanto em ambientes de desenvolvimento local quanto escalonada em containers na nuvem.

> **Upgrade Recente:** O projeto agora conta com arquitetura containerizada e deploy automatizado (CI/CD) para o Azure App Service.

---

## 🚀 Funcionalidades
- **Análise e Geração Automática:** Cria cenários de teste unitários abrangendo casos de sucesso, falha e exceções.
- **Execução Dinâmica:** O agente não apenas escreve o código, mas o executa em um ambiente isolado para validar o comportamento.
- **Relatórios Detalhados:** Retorno estruturado com o `test_code`, o `output` real do pytest e códigos de status de execução.
- **Arquitetura Containerizada:** Pronto para rodar via Docker em qualquer infraestrutura.
- **Pipeline CI/CD:** Integração nativa com GitHub Actions para deploy automatizado na Azure.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.10+
- **API Framework:** FastAPI
- **LLM:** Azure OpenAI (GPT-4 ou GPT-3.5)
- **Framework IA:** LangChain
- **Testes:** Pytest
- **Servidor ASGI:** Uvicorn
- **Controle de versão:** Git + GitHub
- **Deploy:** Azure App Service (integração com GitHub Actions / CI-CD)
- **Infraestrutura:** Azure Container Registry (Docker images), Azure App Service

> Antes de começar, você precisará de uma conta no **Azure** com o serviço **Azure OpenAI** habilitado e um modelo implantado (deployment).

---

## 📡 Como Utilizar o Agente

### Interface Online (Swagger)
Acesse a documentação interativa e teste diretamente pelo navegador:

[https://agente-qa-vinicius-ddhkfdf3f9f6fvh7.canadacentral-01.azurewebsites.net/docs](https://agente-qa-vinicius-ddhkfdf3f9f6fvh7.canadacentral-01.azurewebsites.net/docs)

**Como testar:** Abra o link, clique no método `POST`, depois em `Try it out`, insira seu código JSON e clique em `Execute`.

---

### Cenários de teste e comportamento

O Agente de QA adapta a geração dos testes de acordo com a robustez do seu código. Abaixo, mostramos a diferença entre usar apenas Type Hints e implementar uma validação explícita.

**1. Usando apenas Type Hints**

Neste cenário, o Python aceita os dados (devido à tipagem dinâmica), mas o Agente pode gerar testes rigorosos que falham ao tentar forçar erros de tipo.

### Endpoint Principal: `POST /generate-test`

**Exemplo de Requisição:**
```json
{
  "source_code": "def somar(a: int, b: int) -> int:\n    return a + b",
  "language": "python"
}
```
Saídas esperadas
```json
{
  "status": "success",
  "test_code": "import pytest...",
  "pytest_output": "8 passed in 0.09s",
  "return_code": 0
}   
```
ou
```json
{
  "status": "success",
  "pytest_output": "...FF  [100%]\nFAILED test_generated.py::test_somar_com_tipo_invalido - Failed: DID NOT RAISE <class 'TypeError'>",
  "return_code": 1
}
```
> Nota: O resultado pode variar. Se o Agente gerar apenas testes de lógica, ele retornará sucesso. Caso gere testes de estresse para validar tipos (edge cases), o teste falhará porque o Python, por natureza dinâmica, não lança o erro esperado.

**2. Implementando Validação Explícita**

**Exemplo de Requisição:**
```json
{
  "source_code": "def somar(a, b):\n    if not isinstance(a, int) or not isinstance(b, int):\n        raise ValueError('Notas devem ser números inteiros!')\n    return a + b",
  "language": "python"
}
```
Saída esperada
```json
{
  "status": "success",
  "pytest_output": ".. [100%]\n2 passed in 0.03s",
  "return_code": 0
}
```


> Nota: return_code 0 (Sucesso), 1 (Falha no teste), 2 (Erro de sintaxe).

---

### Execução Local
Para rodar o projeto na sua máquina e realizar modificações:

1. Clone o repositório:
```bash
git clone https://github.com/vicent777/agente-langchain-pytest.git
cd agente-langchain-pytest
```

2. Ambiente Virtual & Dependências:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Variáveis de Ambiente:
```bash
Crie um arquivo .env na raiz:

AZURE_OPENAI_API_KEY="sua_chave"
AZURE_OPENAI_ENDPOINT="https://seu-recurso.openai.azure.com"
AZURE_OPENAI_DEPLOYMENT_NAME="nome-do-deployment"
AZURE_OPENAI_API_VERSION="2023-05-15"
```

4. Execução:
```Bash
uvicorn app:app --reload
```
> Após iniciar, acesse localmente em: http://localhost:8000/docs


