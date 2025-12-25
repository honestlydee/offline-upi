import hashlib
import uuid
import time

def generate_tx_id():
    return str(uuid.uuid4())

def hash_id(value: str):
    return hashlib.sha256(value.encode()).hexdigest()

def current_timestamp():
    return int(time.time())
