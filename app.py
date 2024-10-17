from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Episode, Appearance, Guest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lateshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db, render_as_batch=True)
db.init_app(app)

api = Api(app)

class Index(Resource):
    def get(self):

        """Index page"""

        response_body = {
            "message" : "Welcome to the lateshow."
        }
        return make_response(jsonify(response_body), 200)

class Episodes(Resource):
    def get(self):

        """Get all episodes"""

        episodes = [episode.to_dict(rules=('-appearances',)) for episode in Episode.query.all()]

        response = make_response(
            episodes,
            200
        )

        return response



class EpisodesById(Resource):
    def get(self, id):

        """Get an episode by its id"""

        episode = Episode.query.filter_by(id = id).first()

        if episode == None:
            response_body = {
                "error": "Episode not found."
            }
            response = make_response(response_body, 404)

            return response

        else:

            episode_dict= episode.to_dict()

            response = make_response(
                episode_dict,
                200
            )

            return response


class Guests(Resource):
    def get(self):

        """Get all guests"""

        guests = [guest.to_dict(rules=('-appearances',)) for guest in Guest.query.all()]

        response = make_response(
            guests,
            200
        )

        return response

class Appearances(Resource):
    def post(self):
        """Post a new appearance"""
        data = request.json
        rating = data.get('rating')
        episode_id = data.get('episode_id')
        guest_id = data.get('guest_id')

        # Check if episode and guest exist
        episode = Episode.query.filter_by(id=episode_id).first()
        guest = Guest.query.filter_by(id=guest_id).first()

        if not episode or not guest:
            return make_response(jsonify({"errors": ["Episode or guest not found."]}), 404)
        
        # Validate rating
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            return make_response(jsonify({"errors": ["Rating must be between 1 and 5."]}), 422)

        # Create a new appearance
        try:
            new_appearance = Appearance(
                rating=rating,
                episode_id=episode_id,
                guest_id=guest_id
            )
            db.session.add(new_appearance)
            db.session.commit()

            # Prepare response data, including associated episode and guest details
            response_data = new_appearance.to_dict()
            response_data['episode'] = episode.to_dict(rules=('-appearances',))
            response_data['guest'] = guest.to_dict(rules=('-appearances',))

            return make_response(jsonify(response_data), 201)
        
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"errors": [str(e)]}), 500)



api.add_resource(Index, '/')
api.add_resource(Episodes, '/episodes')
api.add_resource(EpisodesById, '/episodes/<int:id>')
api.add_resource(Guests, '/guests')
api.add_resource(Appearances, '/appearances')

if __name__ == '__main__':
    app.run(port=5555, debug=True)