from datetime import datetime, timedelta, timezone
import jwt
from functools import wraps
from flask import request, jsonify, current_app

# This file contains utility functions for the application.
# It includes a function to encode a JWT token for user authentication.
# The token includes expiration time, issued at time, and subject (user ID).
# The token is signed with a secret key to ensure its integrity and authenticity.
SECRET_KEY = "super secret secrets"

def encode_token(customer_id): #using unique pieces of info to make our tokens user specific
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0,hours=1), #Setting the expiration time to an hour past now
        'iat': datetime.now(timezone.utc), #Issued at
        'sub':  str(customer_id) #This needs to be a string or the token will be malformed and won't be able to be decoded.
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


# The token will expire after 0 days and 1 hour(exp).
# iat is the time the token is "issued at".
# the sub claim (subject)contains the user's ID which needs to be converted to a string.
# HS256 is a hashing algorith to encode th token.
# SECRET_KEY is a key specific to your application used to "sign" tokens.  This prevents forgery of tokens.

# DISCLAIMER:
# When creating the payload it is important to follow thesame naming convention for the dictionary keys "exp", "iat", "sub". Not only are these keys a part of standard token naming conventions, but some of the built-in token validators require thse as well and changing them can lead to errors.

# Token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            # decode the token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            customer_id = data['sub'] # Fetching the customer ID from the token

        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.JWTError:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(customer_id, *args, **kwargs)
        # Call the decorated function with the customer ID
        # This allows the decorated function to access the customer ID for further processing.
    return decorated
# This decorator checks for the presence of a token in the request headers.
# If the token is present, it decodes it and retrieves the customer ID.
# If the token is missing, expired, or invalid, it returns an error response.
