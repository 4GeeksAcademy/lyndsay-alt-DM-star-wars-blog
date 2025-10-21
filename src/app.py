"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Favorites
from sqlalchemy import select
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False


db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def get_user():
    users = db.session.scalars(select(User)).all()
    user_dictionaries = []
    for user in users:
        user_dictionaries.append(
            user.serialize()
        )
    return jsonify(user_dictionaries), 200


@app.route('/character', methods=['GET'])
def get_character():
    character = db.session.scalars(select(Character)).all()
    character_dictionaries = []
    for character in character:
        character_dictionaries.append(
            character.serialize()
        )
    return jsonify(character_dictionaries), 200


@app.route('/planet', methods=['GET'])
def get_planet():
    planet = db.session.scalars(select(Planet)).all()
    planet_dictionaries = []
    for planet in planet:
        planet_dictionaries.append(
            planet.serialize()
        )
    return jsonify(planet_dictionaries), 200


@app.route('/vehicle', methods=['GET'])
def get_vehicle():
    vehicle = db.session.scalars(select(Vehicle)).all()
    vehicle_dictionaries = []
    for vehicle in vehicle:
        vehicle_dictionaries.append(
            vehicle.serialize()
        )
    return jsonify(vehicle_dictionaries), 200


@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def create_favorite_planet(planet_id):
    user_id = request.json.get("user_id", None)
    if user_id is None:
        return jsonify({"message": "User ID is required to create favorite"}), 400
    favorite = Favorites(
        planet_id=planet_id,
        user_id=user_id
    )
    db.session.add(favorite)
    db.session.commit()
    return jsonify(
        favorite.serialize()
    ), 201


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
