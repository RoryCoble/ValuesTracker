import pytest
from packages.Databases import DatabaseConnector, EntityOptions, EntitiesValuesFunctions
from packages.UserDatabase import UserFunctions
from packages.ApiRequests import ApiRequests
from datetime import datetime, timedelta

@pytest.fixture(scope='session')
def setup():
    with DatabaseConnector('EntitiesAndValues', 'data_seeder', "localhost", 5431) as conn:
        _entitiesValues = EntitiesValuesFunctions(conn)
        with _entitiesValues.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.entities, public.entity_values;')
            conn.commit()

        _entitiesValues.add_entity('AAAAA', EntityOptions.SGFB.value, 0.2, 0.1, 0.5)
        _entitiesValues.add_entity_value('AAAAA', datetime.now(), 7.2)

    with DatabaseConnector('EntitiesAndValues', 'api', "localhost", 5431) as conn:
        _user = UserFunctions(conn)
        with _user.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.users, public.user_entities;')
            conn.commit()

        yield ApiRequests("http://localhost:5001/")

        with _user.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.users, public.user_entities;')
            conn.commit()

    with DatabaseConnector('EntitiesAndValues', 'data_seeder', "localhost", 5431) as conn:
        _entitiesValues = EntitiesValuesFunctions(conn)
        with _entitiesValues.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.entities, public.entity_values;')
            conn.commit()

def test_get_entities(setup):
    assert 'AAAAA' in setup.get_entities().json()

def test_get_historical_values(setup):
    response = setup.get_historical_values('AAAAA').json()[0]
    assert datetime.now().strftime('%a, %d %b %Y') in response['timestamp']
    assert '7.2' == response['value']

def test_get_new_values(setup):
    response = setup.get_new_values('AAAAA', datetime.now() - timedelta(days=1)).json()[0]
    assert datetime.now().strftime('%a, %d %b %Y') in response['timestamp']
    assert '7.2' == response['value']

def test_create_user(setup):
    assert setup.create_user('Test', 'Test', 'Test').json() == True

def test_login_user(setup):
    assert setup.login_user('Test', 'Test').json() == True

def test_connect_user_entities(setup):
    assert setup.connect_user_entity('Test', 'AAAAA').json() == True

def test_get_entities_assigned_to_user(setup):
    assert 'AAAAA' in setup.get_entities_assigned_to_user('Test').json()

def test_get_entity_details(setup):
    assert ['AAAAA', EntityOptions.SGFB.value, '0.2', '0.1', '0.5'] == setup.get_entity_details('AAAAA').json()[0]