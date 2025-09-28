from flask import Blueprint, request, jsonify, make_response, current_app, abort
from .models import Person
from .db import db

bp = Blueprint('persons', __name__)

def get_person_or_404(person_id):
    p = Person.query.get(person_id)
    if p is None:
        abort(make_response(jsonify({"message": "Person not found"}), 404))
    return p

@bp.route('/persons', methods=['GET'])
def list_persons():
    persons = Person.query.all()
    return jsonify([p.to_dict() for p in persons]), 200

@bp.route('/persons/<int:person_id>', methods=['GET'])
def get_person(person_id):
    p = get_person_or_404(person_id)
    return jsonify(p.to_dict()), 200

@bp.route('/persons', methods=['POST'])
def create_person():
    if not request.is_json:
        return jsonify({"message":"Invalid data"}), 400
    data = request.get_json()
    if 'name' not in data or not data['name']:
        return jsonify({"message":"Invalid data", "errors": {"name": "required"}}), 400
    p = Person(
        name = data.get('name'),
        age = data.get('age'),
        address = data.get('address'),
        work = data.get('work')
    )
    db.session.add(p)
    db.session.commit()
    location = f"/api/v1/persons/{p.id}"
    resp = make_response('', 201)
    resp.headers['Location'] = location
    return resp

@bp.route('/persons/<int:person_id>', methods=['PATCH'])
def update_person(person_id):
    p = get_person_or_404(person_id)
    if not request.is_json:
        return jsonify({"message":"Invalid data"}), 400
    data = request.get_json()
    # only update provided fields
    for field in ('name','age','address','work'):
        if field in data:
            setattr(p, field, data[field])
    db.session.commit()
    return jsonify(p.to_dict()), 200

@bp.route('/persons/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    p = Person.query.get(person_id)
    if p is None:
        # per requirement, DELETE of missing resource should likely return 404 (spec described get missing -> 404).
        # Tests (Postman) expect 204 on successful delete only. For missing we return 404.
        return jsonify({"message":"Person not found"}), 404
    db.session.delete(p)
    db.session.commit()
    return '', 204