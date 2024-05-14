"""
Module for generating UUID
"""
import uuid
import logging

def generate_uuid():
    """
    Generate a random UUID (Universally Unique Identifier).

    Returns:
        str: A string representation of the generated UUID.
    """
    try:
        random_uuid = uuid.uuid4()
        return str(random_uuid)
    except Exception as e:
        logging.error(str(e))
        raise
