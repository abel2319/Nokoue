#!/usr/bin/python3
""" objects that handles all default RestFul API actions for cities """
from models.user import User
from models.article import Article
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/users/<user_id>/articles', methods=['GET'], strict_slashes=False)
def get_articles(user_id):
    """
    Retrieves the list of all articles objects
    of a specific State, or a specific city
    """
    list_cities = []
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    for article  in user.articles:
        list_cities.append(article.to_dict())

    return jsonify(list_cities)


@app_views.route('/articles/<article_id>/', methods=['GET'], strict_slashes=False)
def get_article(article_id):
    """
    Retrieves a specific article based on id
    """
    article = storage.get(Article, article_id)
    if not article:
        abort(404)
    return jsonify(article.to_dict())


@app_views.route('/articles/<article_id>', methods=['DELETE'], strict_slashes=False)
def delete_article(city_id):
    """
    Deletes a article based on id provided
    """
    article = storage.get(Article, city_id)

    if not article:
        abort(404)
    storage.delete(article)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users/<user_id>/articles', methods=['POST'], strict_slashes=False)
def post_article(user_id):
    """
    Creates an Article
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'content' not in request.get_json():
        abort(400, description="Missing article content")

    data = request.get_json()
    instance = Article(**data)
    instance.user_id = user.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/articles/<article_id>', methods=['PUT'], strict_slashes=False)
def put_article(article_id):
    """
    Updates a Article
    """
    article = storage.get(Article, article_id)
    if not article:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(article, key, value)
    storage.save()
    return make_response(jsonify(article.to_dict()), 200)
