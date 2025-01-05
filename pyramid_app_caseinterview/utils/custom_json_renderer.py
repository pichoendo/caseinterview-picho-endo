"""Custom JSON Renderer to handle python objects serialization in Pyramid."""

from pyramid.renderers import JSON
from datetime import datetime


class CustomJSONRenderer(JSON):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add adapter to convert datetime to string format
        self.add_adapter(datetime, self.datetime_adapter)

    @staticmethod
    def datetime_adapter(obj, request=None):
        # Convert datetime to ISO 8601 format
        return obj.isoformat()  #
