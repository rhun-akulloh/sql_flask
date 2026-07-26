from flask import Flask, request
from flask_migrate import Migrate
from marshmallow import ValidationError, EXCLUDE
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercises
from schemas import (
    exercise_schema,
    exercises_schema,
    workout_schema,
    workouts_schema,
    workout_exercise_schema,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


def save(instance):
    # add + commit an instance
    db.session.add(instance)
    try:
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return None, ({'errors': [str(err)]}, 400)
    except IntegrityError as err:
        db.session.rollback()
        return None, ({'errors': [str(err.orig)]}, 400)
    return instance, None


# Routes

# Workouts 
@app.get("/workouts")
def get_all_workouts():
    # return all workouts
    return workouts_schema.dump(Workout.query.all()), 200

@app.get("/workouts/<int:id>")
def get_specific_workout(id):
    workout = db.session.get(Workout, id)
    if workout is None:
        return {'error': 'Workout not found'}, 404
    return workout_schema.dump(workout), 200

@app.post("/workouts")
def create_workout():
    try:
        data = workout_schema.load(request.get_json(silent=True) or {}, unknown=EXCLUDE)
    except ValidationError as err:
        return {'errors': err.messages}, 400

    workout, error = save(Workout(**data))
    if error:
        return error

    return workout_schema.dump(workout), 200

@app.delete("/workouts/<int:id>")
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if workout is None:
        return {'error': 'Workout not found'}, 404

    db.session.delete(workout)  # cascades to delete associated WorkoutExercises
    db.session.commit()
    return {}, 200


# Exercises
@app.get("/exercises")
def get_all_exercises():
    # gets all exercises
    return exercises_schema.dump(Exercise.query.all()), 200

@app.get("/exercises/<int:id>")
def get_specific_exercise(id):
    # returns a specific exercise
    exercise = db.session.get(Exercise, id)
    if exercise is None:
        return {'error': 'Exercise not found'}, 404
    return exercise_schema.dump(exercise), 200

@app.post("/exercises")
def create_exercise():
    # creates an exercise
    try:
        data = exercise_schema.load(request.get_json(silent=True) or {}, unknown=EXCLUDE)
    except ValidationError as err:
        return {'errors': err.messages}, 400

    exercise, error = save(Exercise(**data))
    if error:
        return error

    return exercise_schema.dump(exercise), 200

@app.delete("/exercises/<int:id>")
def delete_exercise(id):
    # delete specific WorkoutExercises
    exercise = db.session.get(Exercise, id)
    if exercise is None:
        return {'error': 'Exercise not found'}, 404

    db.session.delete(exercise)  # cascades to delete associated WorkoutExercises
    db.session.commit()
    return {}, 200


# WorkoutExercises
@app.post("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")
def create_workout_exercise(workout_id, exercise_id):
    # add an exercise to a workout with reps/sets/duration
    workout = db.session.get(Workout, workout_id)
    if workout is None:
        return {'error': 'Workout not found'}, 404

    exercise = db.session.get(Exercise, exercise_id)
    if exercise is None:
        return {'error': 'Exercise not found'}, 404

    try:
        data = workout_exercise_schema.load(request.get_json(silent=True) or {}, unknown=EXCLUDE)
    except ValidationError as err:
        return {'errors': err.messages}, 400

    workout_exercise, error = save(WorkoutExercises(workout=workout, exercise=exercise, **data))
    if error:
        return error

    return workout_exercise_schema.dump(workout_exercise), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)