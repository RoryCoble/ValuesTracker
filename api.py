'''Web Api for Values Tracker'''
from flask import Flask, jsonify, request

from packages.databases import DatabaseConnector, EntitiesValuesFunctions
from packages.user_database import UserFunctions

def values_tracker_api(_entities_values, _user_functions):
    '''Builds the application api and endpoints for Flask to run'''
    app = Flask(__name__)
    app.config['EntitiesValues'] = _entities_values
    app.config['UserFunctions'] = _user_functions

    @app.route('/health', methods=['GET'])
    def health_check():
        return 200

    @app.route('/api/get_existing_entities', methods=['GET'])
    def get_entities():
        """Gets all of the currently existing Entities"""
        existing_entities = [i[0] for i in app.config['EntitiesValues'].get_existing_entities()]
        return jsonify(existing_entities)

    @app.route('/api/get_historical_values', methods=['GET'])
    def get_historical_values():
        """
        Gets all of the values for the given Entity up to the moment of calling based 
        on Pythons datetime.min
        Required Values:
        - code : string
        """
        code = request.args.get('code')
        historical_values = [{'value': i[2], 'count': i[1]} for i in
                            app.config['EntitiesValues'].get_values(code, 0)]
        return jsonify(historical_values)

    @app.route('/api/get_new_values', methods=['GET'])
    def get_new_values():
        """
        Gets all of the values for the given Entity from the provided timestamp 
        up to the moment of calling
        Required Values:
        - entityCode : code for the Entity whose values are being gotten
        - count : count for which Values occuring at or after are returned
        """
        code = request.args.get('code')
        count = request.args.get('count')
        new_values = [{'value': i[2], 'count': i[1]} for i in
                     app.config['EntitiesValues'].get_values(code, count)]
        return jsonify(new_values)

    @app.route('/api/create_user', methods=['POST'])
    def create_user():
        """
        Posts the provided information to create a new user
        Required Values:
        - userName : string
        - password : string
        - email : string
        """
        user_name = request.form['userName']
        password = request.form['password']
        email = request.form['email']
        success = app.config['UserFunctions'].add_user(user_name, password, email)
        return jsonify(success)

    @app.route('/api/login_user', methods=['POST'])
    def login_user():
        """
        Post to confirm that the provided user name and password
        Required Values:
        - userName : string
        - password : string
        """
        user_name = request.form['userName']
        password = request.form['password']
        success = app.config['UserFunctions'].login_user(user_name, password)
        return jsonify(success)

    @app.route('/api/get_entities_assigned_to_user', methods=['GET'])
    def get_entities_assigned_to_user():
        """
        Get the Entities assigned to the provided User
        Required Values:
        - userName : string
        """
        user_name = request.args.get('userName')
        entities = [i[1] for i in app.config['UserFunctions']
                    .get_entities_assigned_to_user(user_name)]
        return jsonify(entities)

    @app.route('/api/connect_user_entity', methods = ['POST'])
    def connect_user_entity():
        """
        Post to assign the provided Entity to the provided User
        Required Values:
        - userName : string
        - password : string
        """
        user_name = request.form['userName']
        entity_code = request.form['entityCode']
        success = app.config['UserFunctions'].connect_user_entity(user_name, entity_code)
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
        _entities_values = EntitiesValuesFunctions(conn)
        _user_functions = UserFunctions(conn)
        values_tracker_api(_entities_values, _user_functions).run(host='0.0.0.0', debug = True)
