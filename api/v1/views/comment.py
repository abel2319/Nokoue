#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Comment """
from models.user import User
from models.article import Article
from models.comment import Comment
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request

@app_views.route('/articles/<article_id>/comments', methods=['GET'], strict_slashes=False)
def get_convesation(article_id):
    """
    Retrieves the list of all convesation objects
    of a specific State, or a specific city
    """
    list_comment = []
    article = storage.get(Article, article_id)
    if not article:
        abort(404)
    for convesation in article.comments:
        list_comment.append(convesation.to_dict())

    return jsonify(list_comment)


@app_views.route('/comments/<comment_id>', methods=['GET'], strict_slashes=False)
def get_comment(comment_id):
    """ Retrieves a specific Comment"""
    comment = storage.get(Comment, comment_id)
    if not comment:
        abort(404)

    return jsonify(comment.to_dict())


@app_views.route('/comments/<comment_id>', methods=['DELETE'], strict_slashes=False)
def delete_comment(comment_id):
    """
    Deletes a Comment Object
    """

    comment = storage.get(Comment, comment_id)

    if not comment:
        abort(404)

    storage.delete(comment)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/article/<article_id>/comment', methods=['POST'], strict_slashes=False)
def post_comment(article_id):
    """
    Creates a Comment
    """
    article = storage.get(Article, article_id)

    if not article:
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
        abort(400, description="Missing comment content")
    
    data['article_id'] = article_id
    instance = Comment(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/comment/<comment_id>', methods=['PUT'], strict_slashes=False)
def put_comment(comment_id):
    """
    Updates a Comment
    """
    comment = storage.get(Comment, comment_id)

    if not comment:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'comment_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(comment, key, value)
    storage.save()
    return make_response(jsonify(comment.to_dict()), 200)
