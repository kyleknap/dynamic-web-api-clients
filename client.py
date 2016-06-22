import json

from dynamicclient import create_client


def get_model(model_name):
    """Helper method to load an API model"""
    with open(model_name, 'r') as f:
        return json.loads(f.read())
