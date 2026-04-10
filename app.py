from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import subprocess
import tempfile
import os
from main import gerar_testes, explicar_resultado, sugerir_correcao

app = FastAPI(title="QA Agent API", description="Geração de testes unitários com LLM")


class CodeRequest(BaseModel):
    source_code: str
    language: Optional[str] = "python"


@app.post("/generate-test")
async def api_generate_test(request: CodeRequest):
    try:
        # 1. Gera testes via LLM
        resultado = gerar_testes(request.source_code)

        # 2. Cria pasta temporária isolada
        with tempfile.TemporaryDirectory() as tmpdir:

            # 3. Código fonte
            codigo_path = os.path.join(tmpdir, "codigo_enviado.py")

            with open(codigo_path, "w", encoding="utf-8") as f:
                f.write(request.source_code)

            # 4. Testes gerados
            test_file_path = os.path.join(tmpdir, "test_generated.py")

            with open(test_file_path, "w", encoding="utf-8") as f:
                f.write(resultado)

            # 5. PYTHONPATH para pytest achar o módulo
            env = os.environ.copy()
            env["PYTHONPATH"] = tmpdir

            # 6. Executa pytest
            processo = subprocess.run(
                ["pytest", test_file_path, "-q"],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                env=env
            )

        # 7. Gera resumo com LLM do resultado do pytest
        resumo = explicar_resultado(
            processo.stdout + "\n" + processo.stderr,
            processo.returncode
        )

        # 8. Sugere correção

        correcao = None
        if processo.returncode != 0:
            correcao = sugerir_correcao(
                request.source_code,
                processo.stdout + "\n" + processo.stderr,
                processo.returncode
            )

        # 9. Retorno
        return {
            "status": "success",
            "test_code": resultado,
            "pytest_output": processo.stdout,
            "pytest_error": processo.stderr,
            "return_code": processo.returncode,
            "summary": resumo,
            "suggested_fix": correcao
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "online", "message": "MLOps Agent is ready!"}