from datetime import datetime
import random
import string
import math
import time
from packages.databases import DatabaseConnector, EntityOptions, EntitiesValuesFunctions

class Dataseeder:
    """Simple application that provides 10 Entities and Values over time for those Entities"""
    def __init__(self, _entitiesValuesFunctions):
        self.entitiesValues = _entitiesValuesFunctions

    def generate_new_entity(self):
        """Randomly creates the details of an Entity"""
        existingEntities = [i[0] for i in self.entitiesValues.get_existing_entities()]
        for _ in range(1000000):
            newEntity = ''.join(random.choice(string.ascii_letters) for i in range(5)).upper()
            if newEntity not in existingEntities:
                break

        entityType = random.choice(list(EntityOptions)).value
        constants = []
        for _ in range(0,3):
            constants.append(float(random.randrange(0, 10000))/100)

        self.entitiesValues.add_entity(newEntity,
                                       entityType,
                                       constants[0],
                                       constants[1],
                                       constants[2])

    def generate_value(self,
                       count,
                       entity_type, firstConstant, secondConstant, thirdConstant) -> float:
        """
        Randomly generates a value for the provided entity type and constants for a given count
        Keyword arguments:
        count -- value provided to these functions that acts as a traditional x for f(x)
        entityType -- EntityOptions enum value that specifies the equation to use 
                        when generating the value
        firstConstant -- float used in value calculation
        secondConstant -- float used in value calculation
        thirdConstant -- float used in value calculation
        """
        match entity_type:
            case EntityOptions.SGFB.value:
                common_value = firstConstant*count + secondConstant*count + thirdConstant
                uncommon_value = (firstConstant*count)**-2 + (secondConstant*count)**-3 \
                    + (thirdConstant*count)**-4 + 1
                return common_value if random.randrange(0,10) <= 7 else uncommon_value
            case EntityOptions.V.value:
                return abs(firstConstant*math.sin(count)) + secondConstant*random.uniform(-1,1) \
                + thirdConstant*random.randrange(0,2) + 1
            case EntityOptions.FD.value:
                return firstConstant*secondConstant/(count + 1) \
                + thirdConstant*random.randrange(0,2) + 1
            case EntityOptions.FR.value:
                return abs(firstConstant*count + secondConstant*count \
                           + thirdConstant*random.uniform(-1,1)) + 1
            case _:
                return 0

    def add_entity_value(self, count, code):
        """
        Adds a value to the database for a given Entity at the given count
        Keyword arguments:
        count -- value provided to these functions that acts as a traditional x for f(x)
        code -- code for the Entity to which the Value is added
        """
        entityDetails = self.entitiesValues.get_entity_details(code)[0]
        value = self.generate_value(count,
                                    entityDetails[1],
                                    float(entityDetails[2]),
                                    float(entityDetails[3]),
                                    float(entityDetails[4]))
        self.entitiesValues.add_entity_value(code, datetime.now(), value)
        return value

    def run(self):
        """Active generator of Values and sample Entities for the application"""
        for _ in range(0,10):
            self.generate_new_entity()
        entities = [i[0] for i in self.entitiesValues.get_existing_entities()]
        i=0
        while True:
            i+=1
            for entity in entities:
                self.add_entity_value(i, entity)
            time.sleep(random.randrange(10,60))

if __name__ == "__main__":
    with DatabaseConnector('EntitiesAndValues', 'data_seeder', 'db', 5432) as conn:
        _entitiesValues = EntitiesValuesFunctions(conn)
        _dataseeder = Dataseeder(_entitiesValues)
        _dataseeder.run()
