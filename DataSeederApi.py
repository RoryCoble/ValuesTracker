from packages.Databases import DatabaseConnector, EntityOptions, EntitiesValuesFunctions
from DataSeeder import DataSeeder
from flask import Flask, jsonify, request

def DataSeederApi(_entitiesValues, _dataseeder):
    app = Flask(__name__)
    app.config['EntitiesValues'] = _entitiesValues
    app.config['DataSeeder'] = _dataseeder

    @app.route('/dataseed/add_entity', methods = ['POST'])
    def post_specific_entity():
        entityCode = request.form['entityCode']
        entityType = request.form['entityType']
        firstConstant = request.form['firstConstant']
        secondConstant = request.form['secondConstant']
        thirdConstant = request.form['thirdConstant']
        
        success = app.config['EntitiesValues'].add_entity(entityCode, entityType, firstConstant, secondConstant, thirdConstant)
        return jsonify(success)

    @app.route('/dataseed/add_value', methods = ['POST'])
    def post_add_value():
        count = int(request.form['count'])
        entityCode = request.form['entityCode']

        value = app.config['DataSeeder'].add_entity_value(count, entityCode)
        return jsonify(value)

    return app

if __name__ == "__main__":
    with DatabaseConnector('EntitiesAndValues', 'data_seeder', 'db', 5432) as conn:
        _entitiesValues = EntitiesValuesFunctions(conn)
        _dataSeeder = DataSeeder(_entitiesValues)
        app = DataSeederApi(_entitiesValues, _dataSeeder)
        app.run(host='0.0.0.0', port='5002', debug = True)