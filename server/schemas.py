from marshmallow import Schema, fields, validate

from models import ALLOWED_CATEGORIES


class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(dump_only=True)
    exercise_id = fields.Integer(dump_only=True)
    reps = fields.Integer(allow_none=True, validate=validate.Range(min=0, error='reps must not be negative.'))
    sets = fields.Integer(allow_none=True, validate=validate.Range(min=0, error='sets must not be negative.'))
    duration_seconds = fields.Integer(
        allow_none=True,
        validate=validate.Range(min=0, error='duration_seconds must not be negative.'),
    )

    exercise = fields.Nested(
        'ExerciseSchema',
        only=('id', 'name', 'category', 'equipment_needed'),
        dump_only=True,
    )


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, error='name must not be empty.'))
    category = fields.String(
        allow_none=True,
        validate=validate.OneOf(ALLOWED_CATEGORIES, error='category must be one of {choices}.'),
    )
    equipment_needed = fields.Boolean()

    workouts = fields.Nested(
        'WorkoutSchema',
        only=('id', 'date', 'duration_minutes', 'notes'),
        many=True,
        dump_only=True,
    )


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(
        required=True,
        validate=validate.Range(min=1, error='duration_minutes must be a positive integer.'),
    )
    notes = fields.String(allow_none=True)

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True,
        exclude=('workout_id',),
    )


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)
