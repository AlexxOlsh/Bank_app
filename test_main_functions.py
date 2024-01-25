import builtins

from main import main_functions
import pytest


@pytest.mark.parametrize("saved_pass, input_pass, expected_result", [('password', 'password', True),
                                                                     ('password', 'password1', False),
                                                                     ('password', '', False)])
def test_check_password(saved_pass, input_pass, expected_result):
    assert main_functions.check_password(saved_pass, input_pass) == expected_result


# @pytest.mark.parametrize("user, login, expected_result", [({'fio': 'Bob',
#                                                             'password': '12345',
#                                                             'birth': 0,
#                                                             'age': 0,
#                                                             'balance': 0,
#                                                             'limit': -1}, True, True),
#                                                           ({'fio': 'Bob',
#                                                             'password': '12345',
#                                                             'birth': 0,
#                                                             'age': 0,
#                                                             'balance': 0,
#                                                             'limit': -1}, False, False),
#                                                           ({'fio': '',
#                                                             'password': '',
#                                                             'birth': 0,
#                                                             'age': 0,
#                                                             'balance': 0,
#                                                             'limit': -1}, False, False),
#                                                           ({'fio': '',
#                                                             'password': '',
#                                                             'birth': 0,
#                                                             'age': 0,
#                                                             'balance': 0,
#                                                             'limit': -1}, True, False)
#                                                           ])
# def test_check_auth(user, login, expected_result, monkeypatch):
#     input_password = '12345'
#     monkeypatch.setattr(builtins.input(), input_password)
#     main_functions.check_password('12345', '12345')
#     assert main_functions.check_auth(user, login) == expected_result
