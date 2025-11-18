'''General functions that tests use to modify data'''
from packages.databases import EntityOptions, DatabaseConnector, EntitiesValuesFunctions
from packages.user_database import UserFunctions

class SetupFunctions:
    '''Common test setup functions'''
    self.host = os.getenv('HOST', 'localhost')
    self.port = os.getenv('PORT', 5431)

    def truncate_entities(self):
        '''Clears the Entities and Entity Values tables via truncation'''
        with DatabaseConnector('EntitiesAndValues', 'data_seeder', self.host, self.port) as conn:
            _entities_values = EntitiesValuesFunctions(conn)
            with _entities_values.conn.cursor() as cur:
                cur.execute('TRUNCATE TABLE public.entities, public.entity_values;')
                conn.commit()

    def truncate_users(self):
        '''Clears the Users and User Entities tables via truncation'''
        with DatabaseConnector('EntitiesAndValues', 'api', self.host, self.port) as conn:
            _user = UserFunctions(conn)
            with _user.conn.cursor() as cur:
                cur.execute('TRUNCATE TABLE public.users, public.user_entities;')
                conn.commit()

    def seed_entities(self):
        '''Creates sample entities for the Api to play with for testing'''
        with DatabaseConnector('EntitiesAndValues', 'data_seeder', self.host, self.port) as conn:
            _entities_values = EntitiesValuesFunctions(conn)
            _entities_values.add_entity('AAAAA', EntityOptions.SGFB.value, 0.2, 0.1, 0.5)
            _entities_values.add_entity('BBBBB', EntityOptions.V.value, 0.2, 0.1, 0.5)
            _entities_values.add_entity_value('AAAAA', 1, 7.2)
            _entities_values.add_entity_value('BBBBB', 1, 15.2)
