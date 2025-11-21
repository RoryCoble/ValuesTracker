'''Tests for the Database functions not related to Users'''
import os
from decimal import Decimal
import pytest
from packages.databases import DatabaseConnector, EntityOptions, EntitiesValuesFunctions
from tests.setup_functions import SetupFunctions

@pytest.fixture(scope='session', name='setup')
def fixture_setup():
    """
    Clears any data in the associated tables
    Renders the EntitiesValues object for testing
    then cleans up any generated data
    """
    host = os.getenv('HOST', 'localhost')
    port = os.getenv('PORT', 5431)
    SetupFunctions().truncate_entities()
    with DatabaseConnector('EntitiesAndValues', 'data_seeder', host, port) as conn:
        _entities_values = EntitiesValuesFunctions(conn)
        yield _entities_values
    SetupFunctions().truncate_entities()

def test_add_entity(setup):
    '''Tests the Add Entity function'''
    assert setup.add_entity('AAAAA', EntityOptions.SGFB.value, 0.2, 0.1, 0.5)

def test_get_entities(setup):
    '''Tests the Get Entities function'''
    assert 'AAAAA' in setup.get_existing_entities()[0]

def test_get_entity_details(setup):
    '''Tests the Get Entity Details function'''
    assert ('AAAAA', EntityOptions.SGFB.value, Decimal('0.2'), Decimal('0.1'), Decimal('0.5')) \
    == setup.get_entity_details('AAAAA')[0]

def test_add_entity_value(setup):
    '''Tests the Add Entity Value function'''
    assert setup.add_entity_value('AAAAA', 0, 7.2)

def test_get_values(setup):
    '''Tests the Get Values function'''
    values = setup.get_values('AAAAA', 0)[0]
    assert values[0] == 'AAAAA'
    assert values[1] == 0
    assert values[2] == Decimal('7.2')
