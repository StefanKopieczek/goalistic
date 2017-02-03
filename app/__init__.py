from flask import Flask, render_template, jsonify
import database


app = Flask(__name__)
db = database.DatabaseContext()


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/api/users/<user_id>')
def get_user():
    user = db.User.query.filter(User.id=user_id).one()
    return jsonify({
        id: user.id,
        email: user.email,
        name: user.name,
    })
