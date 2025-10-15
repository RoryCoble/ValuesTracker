'''Api to perform dataseeding efforts on demand for Cypress testing'''
from flask import Flask, jsonify, request
from packages.databases import DatabaseConnector, EntitiesValuesFunctions
from dataseeder import Dataseeder

def dataseeder_api(_entities_values, _dataseeder):
    """Creates an API that allows for data seeding of specific Entity & Value data"""
    app = Flask(__name__)
    app.config['EntitiesValues'] = _entities_values
    app.config['DataSeeder'] = _dataseeder

    @app.route('/dataseed/add_entity', methods = ['POST'])
    def post_specific_entity():
        """
        Creates an Entity based on the provided request body
        Required Values:
        - entity_code : String
        - entity_type : String Enum from EntityOptions class in Databases, possible values are
            - Slow Growth Fast Bust
            - Volatile
            - Fluctuating Decline
            - Fluctuating Rise
        - first_constant : String that can resolve to a Decimal
        - second_constant : String that can resolve to a Decimal
        - third_constant : String that can resolve to a Decimal
        """
        entity_code = request.form['entityCode']
        entity_type = request.form['entityType']
        first_constant = request.form['firstConstant']
        second_constant = request.form['secondConstant']
        third_constant = request.form['thirdConstant']

        success = app.config['EntitiesValues'].add_entity(entity_code,
                                                          entity_type,
                                                          first_constant,
                                                          second_constant,
                                                          third_constant)
        return jsonify(success)

    @app.route('/dataseed/add_value', methods = ['POST'])
    def post_add_value():
        """
        Adds a Value for a provided Entity using the Data Seeder's underlying random functions
        Required Values:
        - count : String that can resolve to an Integer
        - entity_code : String
        """
        count = int(request.form['count'])
        entity_code = request.form['entityCode']

        value = app.config['DataSeeder'].add_entity_value(count, entity_code)
        return jsonify(value)

    return app

if __name__ == "__main__":
    with DatabaseConnector('EntitiesAndValues', 'data_seeder', 'db', 5432) as conn:
        _entities_values = EntitiesValuesFunctions(conn)
        _dataseeder = Dataseeder(_entities_values)
        dataseeder_api(_entities_values, _dataseeder).run(host='0.0.0.0',
                                                         port='5002',
                                                         debug = True)
