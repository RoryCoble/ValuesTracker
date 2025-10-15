'''Tests the ApiRequest module the UI uses to call the Api'''
from datetime import datetime, timedelta
import pytest
from packages.databases import DatabaseConnector, EntityOptions, EntitiesValuesFunctions
from packages.user_database import UserFunctions
from packages.api_requests import ApiRequests

@pytest.fixture(scope='session', name='setup')
def fixture_setup():
    """Creates the expected test data, renders the API object for testing, 
    then cleans up any added data after the tests have run"""
    with DatabaseConnector('EntitiesAndValues', 'data_seeder', "localhost", 5431) as conn:
        _entities_values = EntitiesValuesFunctions(conn)
        with _entities_values.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.entities, public.entity_values;')
            conn.commit()

        _entities_values.add_entity('AAAAA', EntityOptions.SGFB.value, 0.2, 0.1, 0.5)
        _entities_values.add_entity_value('AAAAA', datetime.now(), 7.2)

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
        _entities_values = EntitiesValuesFunctions(conn)
        with _entities_values.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.entities, public.entity_values;')
            conn.commit()

def test_get_entities(setup):
    '''Tests the Get Entities endpoint function'''
    assert 'AAAAA' in setup.get_entities().json()

def test_get_historical_values(setup):
    '''Tests the Get Historical Values endpoint function'''
    response = setup.get_historical_values('AAAAA').json()[0]
    assert datetime.now().strftime('%a, %d %b %Y') in response['timestamp']
    assert '7.2' == response['value']

def test_get_new_values(setup):
    '''Tests the Get New Values endpoint function'''
    response = setup.get_new_values('AAAAA', datetime.now() - timedelta(days=1)).json()[0]
    assert datetime.now().strftime('%a, %d %b %Y') in response['timestamp']
    assert '7.2' == response['value']

def test_create_user(setup):
    '''Tests the Create User endpoint function'''
    assert setup.create_user('Test', 'Test', 'Test').json() is True

def test_login_user(setup):
    '''Tests the Login User endpoint function'''
    assert setup.login_user('Test', 'Test').json() is True

def test_connect_user_entities(setup):
    '''Tests the Connect User Entities endpoint function'''
    assert setup.connect_user_entity('Test', 'AAAAA').json() is True

def test_get_entities_assigned_to_user(setup):
    '''Tests Get Entities Assigned to User endpoint function'''
    assert 'AAAAA' in setup.get_entities_assigned_to_user('Test').json()

def test_get_entity_details(setup):
    '''Tests Get Entity Details endpoint function'''
    # pylint: disable=line-too-long
    assert ['AAAAA', EntityOptions.SGFB.value, '0.2', '0.1', '0.5'] == setup.get_entity_details('AAAAA').json()[0]
