from flask import Blueprint, render_template
from flask_login import login_required

home = Blueprint(
    name='home',
    import_name=__name__,
    url_prefix='/home',
    template_folder='templates'
)

@home.route(rule='/signup', methods=['GET', 'POST'])
@login_required
def homepage():
    return render_template('home/home.html')

