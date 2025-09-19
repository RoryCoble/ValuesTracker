import pytest
from packages.Databases import DatabaseConnector, EntityOptions, EntitiesValuesFunctions
from packages.UserDatabase import UserFunctions
from datetime import datetime, timedelta
import Api

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

        _entitiesValues = EntitiesValuesFunctions(conn)
        app = Api.ValuesTrackerApi(_entitiesValues, _user)

        with app.test_client() as test_client:
            with app.app_context():
                yield test_client

        with _user.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.users, public.user_entities;')
            conn.commit()

    with DatabaseConnector('EntitiesAndValues', 'data_seeder', "localhost", 5431) as conn:
        _entitiesValues = EntitiesValuesFunctions(conn)
        with _entitiesValues.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.entities, public.entity_values;')
            conn.commit()

def test_get_entities(setup):
    assert 'AAAAA' in setup.get('/api/get_existing_entities').json

def test_get_historical_values(setup):
    responseJson = setup.get('/api/get_historical_values?code=AAAAA').json[0]
    assert datetime.now().strftime('%a, %d %b %Y') in responseJson['timestamp']
    assert '7.2' == responseJson['value']

def test_get_new_values(setup):
    responseJson = setup.get(f'/api/get_new_values?code=AAAAA&timestamp={datetime.now() - timedelta(days=1)}').json[0]
    assert datetime.now().strftime('%a, %d %b %Y') in responseJson['timestamp']
    assert '7.2' == responseJson['value']

def test_create_user(setup):
    response = setup.post('/api/create_user', data = {
        'userName' : 'test',
        'password' : 'test',
        'email'    : 'test@testing.com',
    }).json

    assert True == response

def test_login_user(setup):
    response = setup.post('/api/login_user', data = {
        'userName' : 'test',
        'password' : 'test',
    }).json
    
    assert True == response

def test_connect_user_entity(setup):
    response = setup.post('/api/connect_user_entity', data = {
        'userName'   : 'test',
        'entityCode' : 'AAAAA',
    }).json

    assert True == response

def test_get_entities_assigned_to_user(setup):
    assert 'AAAAA' in setup.get('/api/get_entities_assigned_to_user?userName=test').json

def test_get_entity_details(setup):
    assert ['AAAAA', EntityOptions.SGFB.value, '0.2', '0.1', '0.5'] == setup.get('/api/get_entity_details?code=AAAAA').json[0]