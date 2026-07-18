from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Category

bp = Blueprint('categories', __name__)


@bp.route('/', methods=['GET'])
@jwt_required()
def list_categories():
    user_id = get_jwt_identity()
    cats = Category.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': c.id, 'name': c.name, 'color': c.color} for c in cats])


@bp.route('/', methods=['POST'])
@jwt_required()
def create_category():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({'msg': 'name required'}), 400
    c = Category(user_id=user_id, name=name, color=data.get('color'))
    db.session.add(c)
    db.session.commit()
    return jsonify({'id': c.id}), 201


@bp.route('/<int:cat_id>', methods=['PUT'])
@jwt_required()
def update_category(cat_id):
    user_id = get_jwt_identity()
    c = Category.query.get(cat_id)
    if not c or c.user_id != user_id:
        return jsonify({'msg': 'not found or unauthorized'}), 404
    data = request.get_json() or {}
    if 'name' in data:
        c.name = data.get('name')
    if 'color' in data:
        c.color = data.get('color')
    db.session.commit()
    return jsonify({'msg': 'updated'})


@bp.route('/<int:cat_id>', methods=['DELETE'])
@jwt_required()
def delete_category(cat_id):
    user_id = get_jwt_identity()
    c = Category.query.get(cat_id)
    if not c or c.user_id != user_id:
        return jsonify({'msg': 'not found or unauthorized'}), 404
    db.session.delete(c)
    db.session.commit()
    return jsonify({'msg': 'deleted'})
