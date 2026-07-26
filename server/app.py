from flask import Flask, make_response
from flask_migrate import Migrate
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


# Routes
@app.get("/workouts")
def get_all_workouts():
    return

@app.get("/workouts/<id>")
def get_specific_workout(id):
    return


@app.get("/exercises")
def get_all_exercises():
    return

@app.get("/exercises/<id>")
def get_specific_exercise(id):
    return


@app.post("/workouts")
def create_workout():
    return

@app.post("/exercises")
def create_exercise():
    return

@app.delete("/workouts/<id>")
def delete_workout(id):
    return

@app.delete("/exercises/<id>")
def delete_exercise(id):
    return

if __name__ == '__main__':
    app.run(port=5555, debug=True)