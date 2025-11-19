'''Tests the functions used to call the User database functions'''
import pytest
from packages.databases import DatabaseConnector
from packages.user_database import UserFunctions
from tests.setup_functions import SetupFunctions

@pytest.fixture(scope='session', name='setup')
def fixture_setup():
    """
    Clears any data in the associated tables
    Renders the UserDatabase object for testing
    then cleans up any generated data
    """
    SetupFunctions().truncate_users()
    host = os.getenv('HOST', 'localhost')
    port = os.getenv('PORT', 5431)
    with DatabaseConnector('EntitiesAndValues', 'api', host, port) as conn:
        _user = UserFunctions(conn)
        yield _user
    SetupFunctions().truncate_users()

def test_add_user(setup):
    '''Tests Add User function'''
    assert setup.add_user('Test', 'Test', 'Test@testing.com')

def test_login_user(setup):
    '''Tests Login User function'''
    assert setup.login_user('Test', 'Test')

def test_connect_user_entity(setup):
    '''Tests Connect User Entity function'''
    assert setup.connect_user_entity('Test', 'AAAAA')

def test_get_entities_assigned_to_user(setup):
    '''Tests Get Entities Assigned to User function'''
    assert 'AAAAA' == setup.get_entities_assigned_to_user('Test')[0][1]
