'''Tests for the Database functions not related to Users'''
from datetime import datetime, timedelta
from decimal import Decimal
import pytest
from packages.databases import DatabaseConnector, EntityOptions, EntitiesValuesFunctions

@pytest.fixture(scope='session', name='setup')
def fixture_setup():
    """
    Clears any data in the associated tables
    Renders the EntitiesValues object for testing
    then cleans up any generated data
    """
    with DatabaseConnector('EntitiesAndValues', 'data_seeder', "localhost", 5431) as conn:
        _entities_values = EntitiesValuesFunctions(conn)
        with _entities_values.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.entities, public.entity_values;')
            conn.commit()
        yield _entities_values
        with _entities_values.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.entities, public.entity_values;')
            conn.commit()

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
    assert setup.add_entity_value('AAAAA', datetime.now(), 7.2)

def test_get_values(setup):
    '''Tests the Get Values function'''
    values = setup.get_values('AAAAA', datetime.now() - timedelta(days=1))[0]
    assert values[0] == 'AAAAA'
    assert values[1].year == datetime.now().year
    assert values[1].month == datetime.now().month
    assert values[1].day == datetime.now().day
    assert values[2] == Decimal('7.2')
