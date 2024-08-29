import pytest
from flaskr.utils import eleva_ao_quadrado, requires_roles
from unittest.mock import Mock, patch
from http import HTTPStatus

# TESTES UNITARIOS, que nao tem dependencias:

def test_eleva_ao_quadrado_sucesso():
    resultado = eleva_ao_quadrado(2)
    assert resultado == 4

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


# TESTES com dependencias, mockado

def test_requires_role_sucesso():
    mock_user = Mock()
    mock_user.role.name = "adm"
    mock_get_jwt_identity = patch("flaskr.utils.get_jwt_identity")
    mock_db_get_or_404 = patch("flaskr.utils.db.get_or_404", return_value = mock_user)
    mock_get_jwt_identity.start()
    mock_db_get_or_404.start()

    decorated_function = requires_roles("adm")(lambda: "success")

    # o outro parenteses com a funcao lambda e necessario porque a funcao requires_roles e um decorador
    # ha outra alternativa: criar um funcao que retorne qualquer resultado que indique que funcionou, por exemplo:

    # def _f():
    #     return "sucesso"
    # ou usar a funcao anonima lambda

    resultado = decorated_function()
    
    assert resultado == "success"

    mock_get_jwt_identity.stop()
    mock_db_get_or_404.stop()

def test_requires_role_falha():
    mock_user = Mock()
    mock_user.role.name = "user"
    mock_get_jwt_identity = patch("flaskr.utils.get_jwt_identity")
    mock_db_get_or_404 = patch("flaskr.utils.db.get_or_404", return_value = mock_user)
    mock_get_jwt_identity.start()
    mock_db_get_or_404.start()

    decorated_function = requires_roles("adm")(lambda: "sucesso")

    resultado = decorated_function()
    
    assert resultado == ({'msg': 'Role unauthorized'}, HTTPStatus.UNAUTHORIZED)

    mock_get_jwt_identity.stop()
    mock_db_get_or_404.stop()

# Mesmo exemplo do teste anterior, mas agora usando o pytest-mock:
# start e stop automatico

def test_requires_role_falha_pytest_mock(mocker):
    # Given
    mock_user = mocker.Mock()
    mock_user.role.name = "user"
        
    mocker.patch("flaskr.utils.get_jwt_identity")
    mocker.patch("flaskr.utils.db.get_or_404", return_value = mock_user)
    decorated_function = requires_roles("adm")(lambda: "sucesso")

    # When
    resultado = decorated_function()
    
    # Then
    assert resultado == ({'msg': 'Role unauthorized'}, HTTPStatus.UNAUTHORIZED)



