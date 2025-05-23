from unittest.mock import Mock, patch

import pytest

from src.utils.eleva_quadrado import eleva_quadrado
from src.utils.requires_roles import requires_role


@pytest.mark.parametrize("test_input,expected", [(2, 4), (3, 9), (4, 16)])
def test_elevar_successo(test_input, expected):
    assert eleva_quadrado(test_input) == expected


@pytest.mark.parametrize(
    "test_input,type_error, msg",
    [
        (
            "a",
            TypeError,
            "unsupported operand type(s) for ** or pow(): 'str' and 'int'",
        ),
        (
            None,
            TypeError,
            "unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'",
        ),
    ],
)
def test_elevar_quadrado_falha(test_input, type_error, msg):
    with pytest.raises(type_error) as exc:
        eleva_quadrado(test_input)
    assert str(exc.value) == msg


from http import HTTPStatus
from unittest.mock import Mock, patch

from src.utils.requires_roles import requires_role


def test_requires_role_success(mocker):
    # Mock do usuário com papel "admin"
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"

    mocker.patch("src.utils.requires_roles.get_jwt_identity", return_value=123)
    mock_user_class = mocker.patch("src.utils.requires_roles.User")

    # Simulando o resultado de User.query.filter_by(id=123).first()
    mock_user_class.query.filter_by.return_value.first.return_value = mock_user

    @requires_role("admin")
    def protected_function():
        return "success"

    result = protected_function()

    assert result == "success"


def test_requires_role_fail(mocker):
    # Given
    mock_user = mocker.Mock()
    mock_user.role.name = "user"
    mocker.patch("src.utils.requires_roles.get_jwt_identity", return_value=123)
    mock_user_class = mocker.patch("src.utils.requires_roles.User")
    mock_user_class.query.filter_by.return_value.first.return_value = mock_user

    @requires_role("admin")
    def protected_function():
        return "success"

    # when
    result = protected_function()

    # then
    assert result == ({"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED)
