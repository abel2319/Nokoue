#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Comment """
from models.user import User
from models.article import Conversation
from models.message import Message
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request

@app_views.route('/messages', methods=['GET'], strict_slashes=False)
def get_messages():
    """
    Retrieves the list of all messages objects
    """
    all_message = storage.all(Message).values()
    list_message = []
    for message in all_message:
        list_message.append(message.to_dict())
    return jsonify(list_message)


@app_views.route('/messages/<message_id>', methods=['GET'], strict_slashes=False)
def get_message(message_id):
    """ Retrieves a specific Message """
    message = storage.get(Message, message_id)
    if not message:
        abort(404)

    return jsonify(message.to_dict())


@app_views.route('/messages/<message_id>', methods=['DELETE'], strict_slashes=False)
def delete_message(message_id):
    """
    Deletes a message Object
    """

    message = storage.get(Message, message_id)

    if not message:
        abort(404)

    storage.delete(message)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/conversations/<conversation_id>/messages', methods=['POST'], strict_slashes=False)
def post_message(conversation_id):
    """
    Creates a Message
    """
    conversation = storage.get(Conversation, conversation_id)

    if not conversation:
        abort(404)
    
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get_user(User, data['user_id'])

    if not user:
        abort(404)

    if 'content' not in request.get_json():
        abort(400, description="Missing message content")
    
    data['conversation_id'] = conversation_id
    instance = Message(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


# @app_views.route('/comment/<comment_id>', methods=['PUT'], strict_slashes=False)
# def put_comment(comment_id):
#     """
#     Updates a Comment
#     """
#     comment = storage.get(Comment, comment_id)

#     if not comment:
#         abort(404)

#     if not request.get_json():
#         abort(400, description="Not a JSON")

#     ignore = ['id', 'user_id', 'comment_id', 'created_at', 'updated_at']

#     data = request.get_json()
#     for key, value in data.items():
#         if key not in ignore:
#             setattr(comment, key, value)
#     storage.save()
#     return make_response(jsonify(comment.to_dict()), 200)
