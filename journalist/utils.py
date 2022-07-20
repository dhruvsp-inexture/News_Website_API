from functools import wraps
from flask import jsonify
from flask_api import status
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import verify_jwt_in_request
from users.models import User


def journalist_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user = User.query.filter_by(id=get_jwt_identity()).first()
            if user.user_type_id == 2:
                return fn(*args, **kwargs)
            else:
                return jsonify(data=[], msg="Journalists only!", status="false"), status.HTTP_403_FORBIDDEN

        return decorator

    return wrapper
