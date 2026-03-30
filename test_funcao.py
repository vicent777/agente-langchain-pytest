import pytest
from funcao import somar, dividir

def test_somar():
    assert somar(2, 3) == 5
    assert somar(-1, 1) == 0
    assert somar(0, 0) == 0
    assert somar(1.5, 2.5) == 4.0

def test_dividir():
    assert dividir(10, 2) == 5
    assert dividir(5, 1) == 5
    assert dividir(0, 1) == 0
    assert dividir(7.5, 2.5) == 3.0

def test_dividir_por_zero():
    with pytest.raises(ValueError, match="Não é possível dividir por zero."):
        dividir(10, 0)