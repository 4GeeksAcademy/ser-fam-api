"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET', 'POST'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {}
    if request.method == 'GET':
        response_body['mesagge'] = 'Todos los miembros de la familia'
        response_body['results'] = members
        return jsonify(response_body), 200
    if request.method == 'POST':
        data = request.json
        members.append(data)
        response_body['mesagge'] = 'Se añadió un nuevo miembro'
        response_body['results'] = members[-1]
        return jsonify(response_body), 200

@app.route('/members/<int:member_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_member(member_id):
    members = jackson_family.get_all_members()
    response_body = {}
    if member_id >= len(members):
        response_body['message'] = 'El miembro no existe'
        response_body['results'] = {}
    if request.method == 'GET':
        response_body['message'] = 'Se obtuvo un miembro'
        response_body['results'] = member_id
        return response_body, 200
    if request.method == 'PUT':
        response_body['message'] = 'Se modificó un miembro'
        response_body['results'] = member_id
        return response_body, 200
    if request.method == 'DELETE':
        response_body['message'] = 'Se borró un miembro'
        response_body['results'] = member_id
        return response_body, 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
