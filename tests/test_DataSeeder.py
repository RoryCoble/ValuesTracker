'''Tests the functions used by the Dataseeder'''
import pytest
from packages.databases import DatabaseConnector, EntityOptions, EntitiesValuesFunctions
from dataseeder import Dataseeder
from tests.setup_functions import SetupFunctions

@pytest.fixture(scope='session', name='setup')
def fixture_setup():
    """
    Clears any existing data in the tables related to testing, renders the 
    Dataseeder object for testing and the EntitiesValues object in order to
    compare that the values created match expectations then removes any 
    generated data
    """
    SetupFunctions().truncate_entities()
    with DatabaseConnector('EntitiesAndValues', 'data_seeder', "localhost", 5431) as conn:
        _entities_values = EntitiesValuesFunctions(conn)
        _dataseeder = Dataseeder(_entities_values)
        yield (_entities_values, _dataseeder)
    SetupFunctions().truncate_entities()

def test_generate_value(setup):
    '''Tests the Generate Value method'''
    _entities_values, _dataseeder = setup
    for option in list(EntityOptions):
        value = _dataseeder.generate_value(1, option.value, 1, 1, 1)
        assert isinstance(value, (int, float)) and value >= 0

def test_generate_entity(setup):
    '''Tests the Generate Entity method'''
    _entities_values, _dataseeder = setup
    _dataseeder.generate_new_entity()
    new_entity = _entities_values.get_existing_entities()[0][0]
    new_entity_details = _entities_values.get_entity_details(new_entity)[0]
    assert new_entity_details[0] == new_entity
    assert new_entity_details[1] in set(option.value for option in EntityOptions)
    assert float(new_entity_details[2]) >= 0
    assert float(new_entity_details[3]) >= 0
    assert float(new_entity_details[4]) >= 0

def test_add_value(setup):
    '''Tests the Add Value method'''
    _entities_values, _dataseeder = setup
    _dataseeder.generate_new_entity()
    new_entity = _entities_values.get_existing_entities()[0][0]
    _dataseeder.add_entity_value(1, new_entity)
    value = _entities_values.get_values(new_entity, 0)[0]
    assert value[0] == new_entity
    assert value[1] == 1
    assert float(value[2]) >= 0
