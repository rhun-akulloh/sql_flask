from flask import Flask, make_response
from flask_migrate import Migrate
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


# Routes

# Workouts 
@app.get("/workouts")
def get_all_workouts():
    # return all workouts
    return {}, 501

@app.get("/workouts/<int:id>")
def get_specific_workout(id):
    return {}, 501

@app.post("/workouts")
def create_workout():
    return {}, 501

@app.delete("/workouts/<int:id>")
def delete_workout(id):
    return {}, 501


# Exercises
@app.get("/exercises")
def get_all_exercises():
    # gets all exercises
    return {}, 501

@app.get("/exercises/<int:id>")
def get_specific_exercise(id):
    # returns a specific exercise
    return {}, 501

@app.post("/exercises")
def create_exercise():
    # creates an exercise
    return {}, 501

@app.delete("/exercises/<int:id>")
def delete_exercise(id):
    # delete specific WorkoutExercises
    return {}, 501


# WorkoutExercises
@app.post("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")
def create_workout_exercise(workout_id, exercise_id):
    # add an exercise to a workout with reps/sets/duration
    return {}, 501

if __name__ == '__main__':
    app.run(port=5555, debug=True)