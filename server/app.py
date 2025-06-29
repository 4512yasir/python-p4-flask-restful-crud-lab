# server/app.py

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Your existing routes here (GET, POST)

# New PATCH and DELETE Resource
class PlantByID(Resource):

    # GET route for retrieving a plant by id
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()

        if not plant:
            return make_response({"error": "Plant not found"}, 404)

        return make_response(plant.to_dict(), 200)

    # PATCH route (already correct)
    def patch(self, id):
        plant = Plant.query.filter_by(id=id).first()

        if not plant:
            return make_response({"error": "Plant not found"}, 404)

        data = request.get_json()

        if "is_in_stock" in data:
            plant.is_in_stock = data["is_in_stock"]
            db.session.add(plant)
            db.session.commit()

        return make_response(plant.to_dict(), 200)

    # DELETE route (already correct)
    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first()

        if not plant:
            return make_response({"error": "Plant not found"}, 404)

        db.session.delete(plant)
        db.session.commit()

        return '', 204

api.add_resource(PlantByID, '/plants/<int:id>')
if __name__ == '__main__':
    app.run(port=5555, debug=True)
