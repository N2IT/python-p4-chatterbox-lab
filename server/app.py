from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>CHATTERBOX API LAB</h1>'

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    # array of all messages as json
    # order_by created_at.asc()
    messages = [message.to_dict() for message in Message.query.order_by(Message.created_at.asc()).all()]

    if request.method == 'GET':
    
        response = make_response(
            messages,
            200
        )

        return response

    elif request.method == 'POST':

        data = request.get_json()
        
        new_message = Message(
            body = data.get("body"),
            username = data.get("username"),
        )

        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict()

        response = make_response(
            new_message_dict,
            201
        )

        return response


@app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    data = request.get_json()
    message = Message.query.filter_by(id=id).first()

    if request.method == 'GET':
        message_to_dict = message.to_dict()

        response = make_response(
            message_to_dict,
            200
        )

        return response
    
    elif request.method == 'PATCH':

        for attr in data:
            setattr(message, attr, data[attr])
        
        db.session.add(message)
        db.session.commit()

        message_to_dict = message.to_dict()

        response = make_response(
            message_to_dict,
            200
        )

        return response

    elif request.method == 'DELETE':
        breakpoint()
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Review deleted."
        }

        response = make_response(
            response_body,
            200
        )

        return response



if __name__ == '__main__':
    app.run(port=5555)
