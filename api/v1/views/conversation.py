#!/usr/bin/python3
""" objects that handles all default RestFul API actions for cities """
from models.user import User
from models.conversation import Conversation
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/users/<user_id>/convesations', methods=['GET'], strict_slashes=False)
def get_convesation(user_id):
    """
    Retrieves the list of all convesation objects
    of a specific State, or a specific city
    """
    list_convesation = []
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    for convesation in user.convesations:
        list_convesation.append(convesation.to_dict())

    return jsonify(list_convesation)


@app_views.route('/conversations/<conversation_id>/', methods=['GET'], strict_slashes=False)
def get_conversation(conversation_id):
    """
    Retrieves a specific conversation based on id
    """
    conversation = storage.get(Conversation, conversation_id)
    if not conversation:
        abort(404)
    return jsonify(conversation.to_dict())


# @app_views.route('/conversation/<conversation_id>', methods=['DELETE'], strict_slashes=False)
# def delete_city(conversation_id):
#     """
#     Deletes a conversation based on id provided
#     """
#     conversation = storage.get(Conversation, conversation_id)

#     if not conversation:
#         abort(404)
#     storage.delete(conversation)
#     storage.save()

#     return make_response(jsonify({}), 200)


@app_views.route('/users/<user_id>/conversations', methods=['POST'], strict_slashes=False)
def post_conversation(user_id):
    """
    Creates a Conversation
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    # if 'name' not in request.get_json():
    #     abort(400, description="Missing name")

    data = request.get_json()
    instance = Conversation(**data)
    instance.user_id = user.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

