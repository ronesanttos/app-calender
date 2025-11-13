import jwt #type:ignore
from datetime import datetime, timedelta
from django.conf import settings

def generate_jwt_token(user):
    payload = {
        "user_id": str(user.id),
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
