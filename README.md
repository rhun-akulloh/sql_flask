# Workout Tracker API

A simple Flask + SQLAlchemy API for tracking workouts and the exercises performed in each one.

## Description

The API manages three resources: Exercises (e.g. Push-up, Squat), Workouts (a logged session with a date and duration), and WorkoutExercises, a join table linking an exercise to a workout along with the reps, sets, and duration for that exercise.

## Installation

1. Install dependencies: pipenv install
2. Activate the virtual environment: pipenv shell
3. Move into the server folder: cd server
4. Create the database and tables: flask db upgrade head
5. Seed the database with sample data: python seed.py (safe to rerun anytime to reset the data)

## Run Instructions

From the server folder, run: python app.py

The API will be available at http://localhost:5555

## Endpoints

GET /workouts - List all workouts

GET /workouts/id - Get a single workout, including its exercises and reps/sets/duration

POST /workouts - Create a workout (date, duration_minutes, notes)

DELETE /workouts/id - Delete a workout and its associated workout-exercise records

GET /exercises - List all exercises

GET /exercises/id - Get a single exercise, including the workouts it's used in

POST /exercises - Create an exercise (name, category, equipment_needed)

DELETE /exercises/id - Delete an exercise and its associated workout-exercise records

POST /workouts/workout_id/exercises/exercise_id/workout_exercises - Add an exercise to a workout with reps, sets, and duration_seconds
