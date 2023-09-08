from flask import (
    render_template, 
    g,
    request,
    session,
    redirect,
    url_for
)
from app import app

@app.route('/404', methods = ['GET'])
def handler404():
    return render_template('handler/404.html', title="404 - rocket.saas")