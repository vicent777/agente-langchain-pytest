from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from main import gerar_testes

app = FastAPI(title="QA Agent API", description="Geração de testes unitários com LLM")

# Definindo o que a API espera receber
class CodeRequest(BaseModel):
    source_code: str
    language: Optional[str] = "python"

@app.post("/generate-test")
async def api_generate_test(request: CodeRequest):
    try:
        # Chamamos passando o código e deixamos 'eh_arquivo' como False (padrão)
        resultado = gerar_testes(request.source_code)
        return {"status": "success", "test_code": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "online", "message": "MLOps Agent is ready!"}