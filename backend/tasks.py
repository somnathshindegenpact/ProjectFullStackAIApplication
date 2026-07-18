from datetime import date, datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Task

bp = Blueprint('tasks', __name__)


def _parse_date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value).date()
        except ValueError:
            pass
    return None


def check_ownership(task, user_id):
    return task and task.user_id == user_id


@bp.route('/', methods=['GET'])
@jwt_required()
def list_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    out = []
    for t in tasks:
        out.append({
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'due_date': t.due_date.isoformat() if t.due_date else None,
            'priority': t.priority,
            'status': t.status,
            'progress': t.progress,
            'category_id': t.category_id,
        })
    return jsonify(out)


@bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    title = data.get('title')
    if not title:
        return jsonify({'msg': 'title required'}), 400
    t = Task(
        user_id=user_id,
        title=title,
        description=data.get('description'),
        due_date=_parse_date(data.get('due_date')),
        priority=data.get('priority', 3),
        status=data.get('status', 'todo'),
        progress=data.get('progress', 0),
        category_id=data.get('category_id')
    )
    db.session.add(t)
    db.session.commit()
    return jsonify({'id': t.id}), 201


@bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()
    t = Task.query.get(task_id)
    if not check_ownership(t, user_id):
        return jsonify({'msg': 'not found or unauthorized'}), 404
    return jsonify({'id': t.id, 'title': t.title, 'description': t.description, 'due_date': t.due_date.isoformat() if t.due_date else None, 'priority': t.priority, 'status': t.status, 'progress': t.progress, 'category_id': t.category_id})


@bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    t = Task.query.get(task_id)
    if not check_ownership(t, user_id):
        return jsonify({'msg': 'not found or unauthorized'}), 404
    data = request.get_json() or {}
    if 'title' in data:
        t.title = data.get('title')
    if 'description' in data:
        t.description = data.get('description')
    if 'due_date' in data:
        t.due_date = _parse_date(data.get('due_date'))
    if 'priority' in data:
        t.priority = data.get('priority')
    if 'status' in data:
        t.status = data.get('status')
    if 'progress' in data:
        t.progress = data.get('progress')
    if 'category_id' in data:
        t.category_id = data.get('category_id')
    db.session.commit()
    return jsonify({'msg': 'updated'})


@bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    t = Task.query.get(task_id)
    if not check_ownership(t, user_id):
        return jsonify({'msg': 'not found or unauthorized'}), 404
    db.session.delete(t)
    db.session.commit()
    return jsonify({'msg': 'deleted'})
