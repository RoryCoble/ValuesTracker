import pytest
from packages.Databases import DatabaseConnector, EntityOptions, EntitiesValuesFunctions
from DataSeeder import DataSeeder
from datetime import datetime, timedelta

@pytest.fixture(scope='session')
def setup():
    """
    Clears any existing data in the tables related to testing, renders the Dataseeder object for testing
    and the EntitiesValues object in order to compare that the values created match expectations
    then removes any generated data
    """
    with DatabaseConnector('EntitiesAndValues', 'data_seeder', "localhost", 5431) as conn:
        _entitiesValues = EntitiesValuesFunctions(conn)
        _dataSeeder = DataSeeder(_entitiesValues)
        with _entitiesValues.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.entities, public.entity_values;')
            conn.commit()
        yield (_entitiesValues, _dataSeeder)
        with _entitiesValues.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.entities, public.entity_values;')
            conn.commit()

def test_generate_value(setup):
    _entitiesValues, _dataSeeder = setup
    for option in list(EntityOptions):
        value = _dataSeeder.generate_value(1, option.value, 1, 1, 1)
        assert isinstance(value, (int, float)) and value >= 0

def test_generate_entity(setup):
    _entitiesValues, _dataSeeder = setup
    _dataSeeder.generate_new_entity()
    newEntity = _entitiesValues.get_existing_entities()[0][0]
    newEntityDetails = _entitiesValues.get_entity_details(newEntity)[0]
    assert newEntityDetails[0] == newEntity
    assert newEntityDetails[1] in set(option.value for option in EntityOptions)
    assert float(newEntityDetails[2]) >= 0
    assert float(newEntityDetails[3]) >= 0
    assert float(newEntityDetails[4]) >= 0

def test_add_value(setup):
    _entitiesValues, _dataSeeder = setup
    _dataSeeder.generate_new_entity()
    newEntity = _entitiesValues.get_existing_entities()[0][0]
    _dataSeeder.add_entity_value(1, newEntity)
    value = _entitiesValues.get_values(newEntity, datetime.now() - timedelta(days=1))[0]
    assert value[0] == newEntity
    assert value[1].year == datetime.now().year
    assert value[1].month == datetime.now().month
    assert value[1].day == datetime.now().day
    assert float(value[2]) >= 0 