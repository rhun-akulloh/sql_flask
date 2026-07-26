from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

# models

ALLOWED_CATEGORIES = ('cardio', 'strength', 'flexibility', 'balance')


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean, default=False)

    workout_exercises = db.relationship('WorkoutExercises', back_populates='exercise', cascade='all, delete-orphan')
    workouts = association_proxy('workout_exercises', 'workout')

    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError('Exercise name must not be empty.')
        return name.strip()

    @validates('category')
    def validate_category(self, key, category):
        if category is not None and category.lower() not in ALLOWED_CATEGORIES:
            raise ValueError(f'category must be one of {ALLOWED_CATEGORIES}.')
        return category


class Workout(db.Model):
    __tablename__ = 'workouts'
    __table_args__ = (
        db.CheckConstraint('duration_minutes > 0', name='check_duration_minutes_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship('WorkoutExercises', back_populates='workout', cascade='all, delete-orphan')
    exercises = association_proxy('workout_exercises', 'exercise')

    @validates('duration_minutes')
    def validate_duration_minutes(self, key, duration_minutes):
        if not isinstance(duration_minutes, int) or duration_minutes <= 0:
            raise ValueError('duration_minutes must be a positive integer.')
        return duration_minutes


class WorkoutExercises(db.Model):
    __tablename__ = 'workout_exercises'
    __table_args__ = (
        db.UniqueConstraint('workout_id', 'exercise_id', name='uq_workout_exercise'),
        db.CheckConstraint('reps >= 0', name='check_reps_non_negative'),
        db.CheckConstraint('sets >= 0', name='check_sets_non_negative'),
        db.CheckConstraint('duration_seconds >= 0', name='check_duration_seconds_non_negative'),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('reps', 'sets', 'duration_seconds')
    def validate_non_negative(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f'{key} must not be negative.')
        return value

