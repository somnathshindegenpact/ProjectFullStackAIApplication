from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Document

bp = Blueprint('documents', __name__)


@bp.route('/', methods=['GET'])
@jwt_required()
def list_documents():
    user_id = get_jwt_identity()
    docs = Document.query.filter((Document.user_id == user_id) | (Document.user_id == None)).all()
    return jsonify([{'id': d.id, 'title': d.title, 'source_url': d.source_url} for d in docs])


@bp.route('/', methods=['POST'])
@jwt_required()
def create_document():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    content = data.get('content')
    if not content:
        return jsonify({'msg': 'content required'}), 400
    d = Document(user_id=user_id, title=data.get('title'), content=content, source_url=data.get('source_url'))
    db.session.add(d)
    db.session.commit()
    return jsonify({'id': d.id}), 201


@bp.route('/<int:doc_id>', methods=['GET'])
@jwt_required()
def get_document(doc_id):
    user_id = get_jwt_identity()
    d = Document.query.get(doc_id)
    if not d or (d.user_id is not None and d.user_id != user_id):
        return jsonify({'msg': 'not found or unauthorized'}), 404
    return jsonify({'id': d.id, 'title': d.title, 'content': d.content, 'source_url': d.source_url})


@bp.route('/<int:doc_id>', methods=['DELETE'])
@jwt_required()
def delete_document(doc_id):
    user_id = get_jwt_identity()
    d = Document.query.get(doc_id)
    if not d or (d.user_id is not None and d.user_id != user_id):
        return jsonify({'msg': 'not found or unauthorized'}), 404
    db.session.delete(d)
    db.session.commit()
    return jsonify({'msg': 'deleted'})
