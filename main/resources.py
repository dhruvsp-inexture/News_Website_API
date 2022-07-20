from flask_api import status
from flask_restful import Resource


class HomePage(Resource):
    def get(self):
        return {"data": "Hello World!",
                "message": "Home Page",
                "status": "true"
                }, status.HTTP_200_OK
