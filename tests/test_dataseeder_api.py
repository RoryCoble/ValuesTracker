'''Tests the Dataseeder Api endpoints'''
import os
from decimal import Decimal
import pytest
from packages.databases import DatabaseConnector, EntitiesValuesFunctions
from dataseeder import Dataseeder
from tests.setup_functions import SetupFunctions
import dataseeder_api

@pytest.fixture(scope='session', name='setup')
def fixture_setup():
    """
    Clears any existing data in the tables related to testing, renders the DataseederApi 
    object for testing and the EntitiesValues object in order to compare that the values
    created match expectations then removes any generated data
    """
    host = os.getenv('HOST', 'localhost')
    port = os.getenv('PORT', 5431)
    SetupFunctions().truncate_entities()
    with DatabaseConnector('EntitiesAndValues', 'data_seeder', host, port) as conn:
        _entities_values = EntitiesValuesFunctions(conn)
        _dataseeder = Dataseeder(_entities_values)
        app = dataseeder_api.dataseeder_api(_entities_values, _dataseeder)
        with app.test_client() as test_client:
            with app.app_context():
                yield (test_client, _entities_values)

    SetupFunctions().truncate_entities()

def test_add_entity(setup):
    '''Tests the Add Entity endpoint'''
    test_client, _entities_values = setup
    response = test_client.post('/dataseed/add_entity', data = {
        'entityCode'     : 'AAAAA',
        'entityType'     : 'Volatile',
        'firstConstant'  : '5.2',
        'secondConstant' : '3.4',
        'thirdConstant'  : '6.9',
    }).json

    assert response is True

    assert ('AAAAA', 'Volatile', Decimal('5.2'), Decimal('3.4'), Decimal('6.9')) \
    == _entities_values.get_entity_details('AAAAA')[0]

def test_add_value(setup):
    '''Tests the Add Value endpoint'''
    test_client, _entities_values = setup
    _ = test_client.post('/dataseed/add_value', data = {
        'count'      : '1',
        'entityCode' : 'AAAAA',
    }).json

    values = _entities_values.get_values('AAAAA', 0)[0]
    assert values[0] == 'AAAAA'
    assert values[1] == 1
    assert values[2] != 0
