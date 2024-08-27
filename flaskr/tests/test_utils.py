import pytest
from flaskr.utils import eleva_ao_quadrado

# teste simples:

# def test_eleva_ao_quadrado_sucesso():
#     resultado = eleva_ao_quadrado(2)
#     assert resultado == 4

# passando varios cenarios de teste (varios argumentos), usar o decorador @pytest.mark.parametrize("test_input,expected", [(2, 4), (5, 25), (10, 100)])

@pytest.mark.parametrize("test_input,expected", [(2, 4), (5, 25), (10, 100)])
def test_eleva_ao_quadrado_sucesso_argumentos(test_input, expected):
    resultado = eleva_ao_quadrado(test_input)
    assert resultado == expected

# para a falha, deve-se pegar a exception lancada e inserir no testem, usando um bloco de contexto

def test_eleva_ao_quadrado_falha():
    with pytest.raises(TypeError) as exc:
        eleva_ao_quadrado("a")
    assert str(exc.value) == "unsupported operand type(s) for ** or pow(): 'str' and 'int'"

# exemplo de falha usando o decorador para passar varios cenarios de falha
#Alterei o expected para exc_class e inclui msg

@pytest.mark.parametrize("test_input,exc_class, msg", [('a', TypeError , "unsupported operand type(s) for ** or pow(): 'str' and 'int'" ), (None, TypeError, "unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'")])
def test_eleva_ao_quadrado_falha_argumentos(test_input, exc_class, msg):
    with pytest.raises(exc_class) as exc:
        eleva_ao_quadrado(test_input)
    assert str(exc.value) == msg