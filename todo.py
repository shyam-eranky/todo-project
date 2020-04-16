# Main web app entry point that handles the incoming routes to the different resources
# that are needed by the UI
# This can also be changed to return JSON if you want this as an API layer and have the front end
# built as a separate React/Angular app
from todoapp import create_app, print_config
import pprint as pp
import json
from flask import current_app, request, jsonify, render_template
from todoapp.models import User

app = create_app()

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
    return response


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


## Test methods -- START --
@app.route("/users")              
def users():              
    user_list = User.query.all()
    users = list(map(lambda user : user.serialize(), user_list))
    pp.pprint(users)
    return jsonify(users)

@app.route("/test")             
def test():              
    user_list = User.query.all()
    pp.pprint(user_list)
    for u in user_list:
        tasks = list(map(lambda task: task.serialize(),u.tasks))
        pp.pprint(tasks)
    
    return jsonify(tasks)
## Test methods -- END --

if __name__ =="__main":
    app.run(debug=True)