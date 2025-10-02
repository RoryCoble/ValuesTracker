from packages.Databases import DatabaseConnector, EntityOptions, EntitiesValuesFunctions
from packages.UserDatabase import UserFunctions
from flask import Flask, jsonify, request
from datetime import datetime

def ValuesTrackerApi(_entitiesValues, _userFunctions):
    app = Flask(__name__)
    app.config['EntitiesValues'] = _entitiesValues
    app.config['UserFunctions'] = _userFunctions
    
    @app.route('/api/get_existing_entities', methods=['GET'])
    def get_entities():
        """Gets all of the currently existing Entities"""
        existingEntities = [i[0] for i in app.config['EntitiesValues'].get_existing_entities()]
        return jsonify(existingEntities)
        
    @app.route('/api/get_historical_values', methods=['GET'])
    def get_historical_values():
        """
        Gets all of the values for the given Entity up to the moment of calling based on Pythons datetime.min
        Required Values:
        - code : string
        """
        code = request.args.get('code')
        historicalValues = [{'value': i[2], 'timestamp': i[1]} for i in app.config['EntitiesValues'].get_values(code, datetime.min)]
        return jsonify(historicalValues)
    
    @app.route('/api/get_new_values', methods=['GET'])
    def get_new_values():
        """
        Gets all of the values for the given Entity from the provided timestamp up to the moment of calling
        Required Values:
        - entityCode : code for the Entity whose values are being gotten
        - timestamp : time for which Values occuring at or after are returned
        """
        code = request.args.get('code')
        timestamp = request.args.get('timestamp')
        newValues = [{'value': i[2], 'timestamp': i[1]} for i in app.config['EntitiesValues'].get_values(code, timestamp)]
        return jsonify(newValues)
    
    @app.route('/api/create_user', methods=['POST'])
    def create_user():
        """
        Posts the provided information to create a new user
        Required Values:
        - userName : string
        - password : string
        - email : string
        """
        userName = request.form['userName']
        password = request.form['password']
        email = request.form['email']
        success = app.config['UserFunctions'].add_user(userName, password, email)
        return jsonify(success)
    
    @app.route('/api/login_user', methods=['POST'])
    def login_user():
        """
        Post to confirm that the provided user name and password
        Required Values:
        - userName : string
        - password : string
        """
        userName = request.form['userName']
        password = request.form['password']
        success = app.config['UserFunctions'].login_user(userName, password)
        return jsonify(success)
    
    @app.route('/api/get_entities_assigned_to_user', methods=['GET'])
    def get_entities_assigned_to_user():
        """
        Get the Entities assigned to the provided User
        Required Values:
        - userName : string
        """
        userName = request.args.get('userName')
        entities = [i[1] for i in app.config['UserFunctions'].get_entities_assigned_to_user(userName)]
        return jsonify(entities)
    
    @app.route('/api/connect_user_entity', methods = ['POST'])
    def connect_user_entity():
        """
        Post to assign the provided Entity to the provided User
        Required Values:
        - userName : string
        - password : string
        """
        userName = request.form['userName']
        entityCode = request.form['entityCode']
        success = app.config['UserFunctions'].connect_user_entity(userName, entityCode)
        return jsonify(success)

    @app.route('/api/get_entity_details', methods=['GET'])
    def get_entity_details():
        """
        Get the Details of the provided Entity
        Required Values:
        - code : string
        """
        code = request.args.get('code')
        response = app.config['EntitiesValues'].get_entity_details(code)
        return jsonify(response)

    return app

if __name__ == "__main__":
    with DatabaseConnector('EntitiesAndValues', 'api', 'db', 5432) as conn:
        _entitiesValues = EntitiesValuesFunctions(conn)
        _userFunctions = UserFunctions(conn)
        app = ValuesTrackerApi(_entitiesValues, _userFunctions)
        app.run(host='0.0.0.0', debug = True)