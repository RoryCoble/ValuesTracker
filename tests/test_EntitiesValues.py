import pytest
from packages.Databases import DatabaseConnector, EntityOptions, EntitiesValuesFunctions
from datetime import datetime, timedelta
from decimal import Decimal

@pytest.fixture(scope='session')
def setup():
    with DatabaseConnector('EntitiesAndValues', 'data_seeder', "localhost", 5431) as conn:
        _entitiesValues = EntitiesValuesFunctions(conn)
        with _entitiesValues.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.entities, public.entity_values;')
            conn.commit()
        yield _entitiesValues
        with _entitiesValues.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE public.entities, public.entity_values;')
            conn.commit()

def test_add_entity(setup):
    assert setup.add_entity('AAAAA', EntityOptions.SGFB.value, 0.2, 0.1, 0.5)

def test_get_entities(setup):
    assert 'AAAAA' in setup.get_existing_entities()[0]

def test_get_entity_details(setup):
    assert ('AAAAA', EntityOptions.SGFB.value, Decimal('0.2'), Decimal('0.1'), Decimal('0.5')) == setup.get_entity_details('AAAAA')[0]

def test_add_entity_value(setup):
    assert setup.add_entity_value('AAAAA', datetime.now(), 7.2)

def test_get_values(setup):
    values = setup.get_values('AAAAA', datetime.now() - timedelta(days=1))[0]
    assert values[0] == 'AAAAA'
    assert values[1].year == datetime.now().year
    assert values[1].month == datetime.now().month
    assert values[1].day == datetime.now().day
    assert values[2] == Decimal('7.2')