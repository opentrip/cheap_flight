from flask import (Blueprint, render_template, redirect,
                   url_for, session, request)


bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    return render_template('index.html')
