#!/usr/bin/python3
"""creates a flask Blueprint and imports all views which use Blueprint"""

from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.user import *
from api.v1.views.conversation import *
from api.v1.views.article import *
from api.v1.views.participants import *
from api.v1.views.message import *
from api.v1.views.comment import *