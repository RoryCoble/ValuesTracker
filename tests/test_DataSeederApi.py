from packages.Databases import DatabaseConnector, EntityOptions, EntitiesValuesFunctions
from DataSeeder import DataSeeder
import pytest
import DataSeederApi
from datetime import datetime, timedelta
from decimal import Decimal

@pytest.fixture(scope='session')
def setup():
    """
    Clears any existing data in the tables related to testing, renders the DataseederApi object for testing
    and the EntitiesValues object in order to compare that the values created match expectations
    then removes any generated data
    """
    with DatabaseConnector('EntitiesAndValues', 'data_seeder', "localhost", 5431) as conn:
        _entitiesValues = EntitiesValuesFunctions(conn)
        with _entitiesValues.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.entities, public.entity_values;')
            conn.commit()

        _dataSeeder = DataSeeder(_entitiesValues)
        app = DataSeederApi.DataSeederApi(_entitiesValues, _dataSeeder)
        with app.test_client() as test_client:
            with app.app_context():
                yield (test_client, _entitiesValues)

        with _entitiesValues.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.entities, public.entity_values;')
            conn.commit()

def test_add_entity(setup):
    test_client, _entitiesValues = setup
    response = test_client.post('/dataseed/add_entity', data = {
        'entityCode'     : 'AAAAA',
        'entityType'     : 'Volatile',
        'firstConstant'  : '5.2',
        'secondConstant' : '3.4',
        'thirdConstant'  : '6.9',
    }).json

    assert response == True
    assert ('AAAAA', 'Volatile', Decimal('5.2'), Decimal('3.4'), Decimal('6.9')) == _entitiesValues.get_entity_details('AAAAA')[0]

def test_add_value(setup):
    test_client, _entitiesValues = setup
    response = test_client.post('/dataseed/add_value', data = {
        'count'      : '1',
        'entityCode' : 'AAAAA',
    }).json

    values = _entitiesValues.get_values('AAAAA', datetime.now() - timedelta(days=1))[0]
    assert values[0] == 'AAAAA'
    assert values[1].year == datetime.now().year
    assert values[1].month == datetime.now().month
    assert values[1].day == datetime.now().day
    assert values[2] != 0