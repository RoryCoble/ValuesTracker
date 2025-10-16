'''Dataseeder class'''
from datetime import datetime
import random
import string
import math
import time
from packages.databases import DatabaseConnector, EntityOptions, EntitiesValuesFunctions

class Dataseeder:
    """Simple application that provides 10 Entities and Values over time for those Entities"""
    def __init__(self, _entities_values_functions):
        self.entities_values = _entities_values_functions

    def generate_new_entity(self):
        """Randomly creates the details of an Entity"""
        existing_entities = [i[0] for i in self.entities_values.get_existing_entities()]
        for _ in range(1000000):
            new_entity = ''.join(random.choice(string.ascii_letters) for i in range(5)).upper()
            if new_entity not in existing_entities:
                break

        entity_type = random.choice(list(EntityOptions)).value
        constants = []
        for _ in range(0,3):
            constants.append(float(random.randrange(0, 10000))/100)

        self.entities_values.add_entity(new_entity,
                                        entity_type,
                                        constants[0],
                                        constants[1],
                                        constants[2])

    def generate_value(self,
                       count,
                       entity_type, first_constant, second_constant, third_constant) -> float:
        """
        Randomly generates a value for the provided entity type and constants for a given count
        Keyword arguments:
        count -- value provided to these functions that acts as a traditional x for f(x)
        entity_type -- EntityOptions enum value that specifies the equation to use 
                        when generating the value
        first_constant -- float used in value calculation
        second_constant -- float used in value calculation
        third_constant -- float used in value calculation
        """
        match entity_type:
            case EntityOptions.SGFB.value:
                common_value = first_constant*count + second_constant*count + third_constant
                uncommon_value = (first_constant*count)**-2 + (second_constant*count)**-3 \
                    + (third_constant*count)**-4 + 1
                return common_value if random.randrange(0,10) <= 7 else uncommon_value
            case EntityOptions.V.value:
                return abs(first_constant*math.sin(count)) + second_constant*random.uniform(-1,1) \
                + third_constant*random.randrange(0,2) + 1
            case EntityOptions.FD.value:
                return first_constant*second_constant/(count + 1) \
                + third_constant*random.randrange(0,2) + 1
            case EntityOptions.FR.value:
                return abs(first_constant*count + second_constant*count \
                           + third_constant*random.uniform(-1,1)) + 1
            case _:
                return 0

    def add_entity_value(self, count, code):
        """
        Adds a value to the database for a given Entity at the given count
        Keyword arguments:
        count -- value provided to these functions that acts as a traditional x for f(x)
        code -- code for the Entity to which the Value is added
        """
        entity_details = self.entities_values.get_entity_details(code)[0]
        value = self.generate_value(count,
                                    entity_details[1],
                                    float(entity_details[2]),
                                    float(entity_details[3]),
                                    float(entity_details[4]))
        self.entities_values.add_entity_value(code, datetime.now(), value)
        return value

    def run(self):
        """Active generator of Values and sample Entities for the application"""
        for _ in range(0,10):
            self.generate_new_entity()
        entities = [i[0] for i in self.entities_values.get_existing_entities()]
        i=0
        while True:
            i+=1
            for entity in entities:
                self.add_entity_value(i, entity)
            time.sleep(random.randrange(10,60))

if __name__ == "__main__":
    with DatabaseConnector('EntitiesAndValues', 'data_seeder', 'db', 5432) as conn:
        _entities_values = EntitiesValuesFunctions(conn)
        _dataseeder = Dataseeder(_entities_values)
        _dataseeder.run()
