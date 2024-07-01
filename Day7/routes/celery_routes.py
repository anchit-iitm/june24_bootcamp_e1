from flask_restful import Resource
from flask import jsonify, request, make_response
import celery_tasks as tasks

class celeryHello(Resource):
    def get(self):
        var1 = tasks.helloWorld.delay()
        while not var1.ready():
            pass
        return jsonify({"message": "static from route", "task_id": var1.id, "task_status": var1.status, "task_result": var1.result})
    
    def post(self):
        c = 45
        d = 45
        var1 = tasks.add.delay(c, d)
        while not var1.ready():
            pass
        return jsonify({"message": "static from route", "task_id": var1.id, "task_status": var1.status, "task_result": var1.result})
    
    def put(self, y):
        var1 = tasks.fetch_X_category.delay(y)
        while not var1.ready():
            pass
        return jsonify({"message": "static from route", "task_id": var1.id, "task_status": var1.status, "task_result": var1.result})