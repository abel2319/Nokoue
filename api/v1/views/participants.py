#!/usr/bin/python3
""" objects that handle all default RestFul API actions for User - Conversation """
from models.user import User
from models.conversation import Conversation
from models import storage
from api.v1.views import app_views
from os import environ
from flask import abort, jsonify, make_response, request


@app_views.route('conversations/<conversation_id>/participants', methods=['GET'], strict_slashes=False)
def get_conversation_participants(conversation_id):
    """
    Retrieves the list of all participants objects of a Conversation
    """
    conversation = storage.get(Conversation, conversation_id)

    if not conversation:
        abort(404)
    
    participants = [participant.to_dict() for participant in conversation.participants]
    
    return jsonify(participants)


@app_views.route('/conversations/<conversation_id>/participants/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_conversation_participant(conversation_id, user_id):
    """
    Deletes a User object of a conversation
    """
    conversation = storage.get(Conversation, conversation_id)

    if not conversation:
        abort(404)

    user = storage.get(User, user_id)

    if not user:
        abort(404)
    if user not in conversation.participants:
        abort(404)
    conversation.amenities.remove(user)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/conversations/<conversation_id>/participants/<user_id>', methods=['POST'],  strict_slashes=False)
def post_place_amenity(conversation_id, user_id):
    """
    Link an user object to a conversation
    """
    conversation = storage.get(Conversation, conversation_id)

    if not conversation:
        abort(404)

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if user in conversation.participants:
        return make_response(jsonify(user.to_dict()), 200)
    else:
        conversation.participants.append(user)

    storage.save()
    return make_response(jsonify(user.to_dict()), 201)
