from flask_restful import Resource
from flask import jsonify, make_response, request
from datetime import datetime
from flask_security import current_user, roles_accepted

from database.models import db, Category

class CategoryResource(Resource):
    @roles_accepted('admin', 'manager', 'customer')
    def get(self):
        categories = Category.query.all()
        data = []
        for category in categories:
            cate = {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'status': category.status,
                'created_at': category.created_at,
                'created_by': category.created_by,
                'updated_at': category.updated_at,
                'updated_by': category.updated_by,
                'delete': category.delete
            }
            data.append(cate)
        return make_response(jsonify({'data': data}), 200)
    
    @roles_accepted('admin', 'manager')
    def post(self):
        data = request.get_json()
        name=data['name']
        if not name:
            return make_response(jsonify({'message': 'Name is required'}), 400)
        description=data['description']
        if not description:
            return make_response(jsonify({'message': 'Description is required'}), 400)
        print(name, description)
        if current_user.has_role('admin'):
            cate = Category(name=name, description=description, status=True, created_at=datetime.now(), created_by=current_user.id)
        else:
            cate = Category(name=name, description=description, status=False, created_at=datetime.now(), created_by=current_user.id)
        db.session.add(cate)
        db.session.commit()
        return make_response(jsonify({'message': 'Category added', 'id': cate.id, 'name': cate.name}), 201)



class CategorySpecific(Resource):
    def get(self, id):
        cate = Category.query.get(id)
        if not cate:
            return make_response(jsonify({'message': 'Category not found'}), 404)
        data = {
            'id': cate.id,
            'name': cate.name,
            'description': cate.description,
            'status': cate.status,
            'created_at': cate.created_at,
            'created_by': cate.created_by,
            'updated_at': cate.updated_at,
            'updated_by': cate.updated_by,
            'delete': cate.delete
        }
        return make_response(jsonify({'data': data}), 200)
    @roles_accepted('admin', 'manager')
    def put(self, id):
        data = request.get_json()
        cate = Category.query.get(id)
        if not cate:
            return make_response(jsonify({'message': 'Category not found'}), 404)
        name=data['name']
        if not name:
            return make_response(jsonify({'message': 'Name is required'}), 400)
        description=data['description']
        if not description:
            return make_response(jsonify({'message': 'Description is required'}), 400)
        cate.name = name
        cate.description = description
        cate.updated_at = datetime.now()
        cate.updated_by = current_user.id
        if current_user.has_role('admin'):
            cate.status = True
        else:
            cate.status = False
        db.session.commit()
        return make_response(jsonify({'message': 'Category updated', 'cate_id': id}), 201)
    
    @roles_accepted('admin')
    def patch(self, id ):
        cate = Category.query.get(id)
        if not cate:
            return make_response(jsonify({'message': 'Category not found'}), 404)
        cate.status = True
        cate.updated_at = datetime.now()
        cate.updated_by = current_user.id
        db.session.commit()
        return make_response(jsonify({'message': 'Category activated', 'name': cate.name}), 201)

    @roles_accepted('admin')
    def delete(self, id):
        cate = Category.query.get(id)
        if not cate:
            return make_response(jsonify({'message': 'Category not found'}), 404)
        cate.delete = True
        cate.updated_at = datetime.now()
        cate.updated_by = current_user.id
        db.session.commit()
        return make_response(jsonify({'message': 'Category deleted', 'name': cate.name}), 201)
