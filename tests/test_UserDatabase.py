import pytest
from packages.Databases import DatabaseConnector
from packages.UserDatabase import UserFunctions

@pytest.fixture(scope='session')
def setup():
    """
    Clears any data in the associated tables
    Renders the UserDatabase object for testing
    then cleans up any generated data
    """
    with DatabaseConnector('EntitiesAndValues', 'api', "localhost", 5431) as conn:
        _user = UserFunctions(conn)
        with _user.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.users, public.user_entities;')
            conn.commit()
        yield _user
        with _user.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.users, public.user_entities;')
            conn.commit()

def test_add_user(setup):
    assert setup.add_user('Test', 'Test', 'Test@testing.com')

def test_login_user(setup):
    assert setup.login_user('Test', 'Test')

def test_connect_user_entity(setup):
    assert setup.connect_user_entity('Test', 'AAAAA')

def test_get_entities_assigned_to_user(setup):
    assert 'AAAAA' == setup.get_entities_assigned_to_user('Test')[0][1]