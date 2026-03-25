from flask import Blueprint, render_template

landing_bp = Blueprint("landing", __name__, template_folder="templates/landing")

@landing_bp.route('/')
def index():
    """Landing page - initial page before login"""
    return render_template('index.html', page_title='Tekscore - SMS Marketing Platform')
