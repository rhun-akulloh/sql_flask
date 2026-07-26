#!/usr/bin/env python3
from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercises


with app.app_context():
    print('Clearing db')
    WorkoutExercises.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print('Seeding exercises')
    push_up = Exercise(name='Push-up', category='strength', equipment_needed=False)
    squat = Exercise(name='Squat', category='strength', equipment_needed=False)
    running = Exercise(name='Running', category='cardio', equipment_needed=False)
    plank = Exercise(name='Plank', category='strength', equipment_needed=False)
    yoga_stretch = Exercise(name='Yoga Stretch', category='flexibility', equipment_needed=True)
    single_leg_stand = Exercise(name='Single-leg Stand', category='balance', equipment_needed=False)
    db.session.add_all([push_up, squat, running, plank, yoga_stretch, single_leg_stand])

    print('Seeding workouts')
    strength_session = Workout(date=date(2026, 7, 20), duration_minutes=30, notes='Morning strength session')
    cardio_and_core = Workout(date=date(2026, 7, 22), duration_minutes=45, notes='Cardio and core')
    recovery_and_balance = Workout(date=date(2026, 7, 24), duration_minutes=20, notes='Recovery and balance work')
    db.session.add_all([strength_session, cardio_and_core, recovery_and_balance])

    db.session.commit()

    print('Seeding workout_exercises')
    workout_exercises = [
        WorkoutExercises(workout=strength_session, exercise=push_up, reps=15, sets=3),
        WorkoutExercises(workout=strength_session, exercise=squat, reps=12, sets=3),
        WorkoutExercises(workout=cardio_and_core, exercise=running, duration_seconds=1200),
        WorkoutExercises(workout=cardio_and_core, exercise=plank, sets=3, duration_seconds=60),
        WorkoutExercises(workout=recovery_and_balance, exercise=yoga_stretch, duration_seconds=600),
        WorkoutExercises(workout=recovery_and_balance, exercise=single_leg_stand, sets=3, duration_seconds=30),
    ]
    db.session.add_all(workout_exercises)
    db.session.commit()

    print('Done seeding')
