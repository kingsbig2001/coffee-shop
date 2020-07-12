import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/drinks*": {"origins": "*"}})

'''
@TODO: Use the after_request decorator to set Access-Control-Allow
'''
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''


@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_list_of_drinks():
    '''This is a Public route for every  one to 
    view drinks with lesser details on the menu'''

    drinks = Drink.query.all()
    drinks_short = [drink.short() for drink in drinks]

    return jsonify({
        "success": True,
        "drinks": drinks_short
    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_detail(payload):
    '''This route is used to fetch full details of drinks 
    on the database by user with get:drinks-detail permissions  '''
    drinks = Drink.query.all()
    drinks_long = [drink.long() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': drinks_long
    }), 200

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(payload):
    ''' This route is reserved to user with Manager roles. It allows user to add drinks to the database '''
    data = request.get_json()
    try:
        drink_recipe = data.get('recipe')

        if isinstance(drink_recipe, dict):
            drink_recipe = [drink_recipe]

        drink_recipe = json.dumps(drink_recipe)
        drink_title = data.get('title')

        drink = Drink(title=drink_title, recipe=drink_recipe)
            
        drink.insert()

    except:
        abort(400)

    new_drink = [drink.long()]

    return jsonify({
        'success': True,
        'drinks': new_drink
        }),200


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    ''' This route is reserved to user with Manager roles. It allows user to modify drinks in the database '''
    data = request.get_json()
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if drink is None:
        abort(404)

    try:
        drink_title = data.get('title')
        drink_recipe = data.get('recipe')
        if drink_title:
            drink.title = drink_title

        if drink_recipe:
            drink.recipe = json.dumps(data['recipe'])

        drink.update()
    except BaseException:
        abort(400)

    updated_drink =  [drink.long()]

    return jsonify({
        'success': True,
        'drinks': updated_drink
        }),200

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    ''' This route is reserved to user with Manager roles. It allows user to delete drinks in the database '''
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if drink is None:
        abort(404)

    try:
        drink.delete()
    except BaseException:
        abort(400)

    return jsonify({
        'success': True,
        'delete': id
        }), 200

## Error Handling
'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
'''
@TODO implement error handler for 400
    error handler should conform to general task above 
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request"
        }), 400

'''
@TODO implement error handler for 401
    error handler should conform to general task above 
'''
@app.errorhandler(401)
def unauthorised(error):
    return jsonify({
        "success": False, 
        "error": 401,
        "message": "unauthorised"
        }), 401

'''
@TODO implement error handler for 403
    error handler should conform to general task above 
'''
@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False, 
        "error": 403,
        "message": "forbidden"
        }), 403
'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
        }), 404

'''
@TODO implement error handler for 405
    error handler should conform to general task above 
'''
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False, 
        "error": 405,
        "message": "method not allowed"
        }), 405

'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422
'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
