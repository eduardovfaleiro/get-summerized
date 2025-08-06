from flask_jwt_extended import create_access_token

def generate_token(email):
    return create_access_token(identity=email)