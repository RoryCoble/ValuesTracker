from packages.Databases import DatabaseConnector, EntityOptions, EntitiesValuesFunctions
from datetime import datetime
import random
import string
import math
import time

class DataSeeder:
    def __init__(self, _entitiesValuesFunctions):
        self.entitiesValues = _entitiesValuesFunctions

    def generate_new_entity(self):
        existingEntities = [i[0] for i in self.entitiesValues.get_existing_entities()]
        for _ in range(1000000):
            newEntity = ''.join(random.choice(string.ascii_letters) for i in range(5)).upper()
            if newEntity not in existingEntities:
                break
        
        entityType = random.choice(list(EntityOptions)).value
        constants = []
        for _ in range(0,3):
            constants.append(float(random.randrange(0, 10000))/100)
            
        self.entitiesValues.add_entity(newEntity, entityType, constants[0], constants[1], constants[2])

    def generate_value(self, count, entityType, firstConstant, secondConstant, thirdConstant) -> float:
        if entityType == EntityOptions.SGFB.value:
            if random.randrange(0,10) <= 7:
                return firstConstant*count + secondConstant*count + thirdConstant
            else:
                return (firstConstant*count)**-2 + (secondConstant*count)**-3 + (thirdConstant*count)**-4 + 1
        elif entityType == EntityOptions.V.value:
            return abs(firstConstant*math.sin(count)) + secondConstant*random.uniform(-1,1) + thirdConstant*random.randrange(0,2) + 1
        elif entityType == EntityOptions.FD.value:
            return firstConstant*secondConstant/(count + 1) + thirdConstant*random.randrange(0,2) + 1
        elif entityType == EntityOptions.FR.value:    
            return abs(firstConstant*count + secondConstant*count + thirdConstant*random.uniform(-1,1)) + 1

    def add_entity_value(self, count, code):
        entityDetails = self.entitiesValues.get_entity_details(code)[0]
        value = self.generate_value(count, 
                                    entityDetails[1], 
                                    float(entityDetails[2]), 
                                    float(entityDetails[3]), 
                                    float(entityDetails[4]))
        self.entitiesValues.add_entity_value(code, datetime.now(), value)

    def run(self):
        for _ in range(0,10):
            self.generate_new_entity()
        entities = [i[0] for i in self.entitiesValues.get_existing_entities()]
        i=0
        while True:
            i+=1
            for entity in entities:
                self.add_entity_value(i, entity)
            time.sleep(random.randrange(0,5))

if __name__ == "__main__":
    with DatabaseConnector('EntitiesAndValues', 'data_seeder', 'db', 5432) as conn:
        _entitiesValues = EntitiesValuesFunctions(conn)
        _dataSeeder = DataSeeder(_entitiesValues)
        _dataSeeder.run()