'''Tests the api.py module'''
from datetime import datetime, timedelta
import pytest
from packages.databases import EntityOptions, DatabaseConnector, EntitiesValuesFunctions
from packages.user_database import UserFunctions
from tests.setup_functions import SetupFunctions
import api

@pytest.fixture(scope='session', name='setup')
def fixture_setup():
    """Creates the expected test data, renders the API object for testing, 
    then cleans up any added data after the tests have run"""
    SetupFunctions().truncate_entities()
    SetupFunctions().truncate_users()
    SetupFunctions().seed_entities()
    with DatabaseConnector('EntitiesAndValues', 'data_seeder', "localhost", 5431) as conn:
        _entities_values = EntitiesValuesFunctions(conn)
        with DatabaseConnector('EntitiesAndValues', 'api', "localhost", 5431) as conn:
            _user = UserFunctions(conn)
            app = api.values_tracker_api(_entities_values, _user)
            with app.test_client() as test_client:
                with app.app_context():
                    yield test_client
    SetupFunctions().truncate_users()
    SetupFunctions().truncate_entities()

def test_get_entities(setup):
    '''Tests the Get Existing Entities endpoint'''
    assert 'AAAAA' in setup.get('/api/get_existing_entities').json

def test_get_historical_values(setup):
    '''Tests the Get Historical Values endpoint'''
    response_json = setup.get('/api/get_historical_values?code=AAAAA').json[0]
    assert datetime.now().strftime('%a, %d %b %Y') in response_json['timestamp']
    assert '7.2' == response_json['value']

def test_get_new_values(setup):
    '''Tests the Get New Values endpoint'''
    # pylint: disable=line-too-long
    response_json = setup.get(f'/api/get_new_values?code=AAAAA&timestamp={datetime.now() - timedelta(days=1)}').json[0]
    assert datetime.now().strftime('%a, %d %b %Y') in response_json['timestamp']
    assert '7.2' == response_json['value']

def test_create_user(setup):
    '''Tests the Create User endpoint'''
    response = setup.post('/api/create_user', data = {
        'userName' : 'test',
        'password' : 'test',
        'email'    : 'test@testing.com',
    }).json

    assert response is True

def test_login_user(setup):
    '''Tests the Login User endpoint'''
    response = setup.post('/api/login_user', data = {
        'userName' : 'test',
        'password' : 'test',
    }).json

    assert response is True

def test_connect_user_entity(setup):
    '''Tests the Connect User Entity endpoint'''
    response = setup.post('/api/connect_user_entity', data = {
        'userName'   : 'test',
        'entityCode' : 'AAAAA',
    }).json

    assert response is True

def test_get_entities_assigned_to_user(setup):
    '''Tests the Get Entities Assigned to User endpoint'''
    assert 'AAAAA' in setup.get('/api/get_entities_assigned_to_user?userName=test').json

def test_get_entity_details(setup):
    '''Tests the Get Entity Details endpoint'''
    assert ['AAAAA', EntityOptions.SGFB.value, '0.2', '0.1', '0.5'] \
    == setup.get('/api/get_entity_details?code=AAAAA').json[0]
