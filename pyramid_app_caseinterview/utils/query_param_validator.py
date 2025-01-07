"""Class to validate query parameters in incoming requests"""

from datetime import datetime
from pyramid.httpexceptions import HTTPBadRequest


class QueryParamValidator:

    def __init__(self, request=None, **query_params):
        self.request = request
        self.invalid = []
        self.validated = {}
        self.query_params = query_params or {}

    def validate_float(self, param_name):
        """Validate if the field is a float."""
        value = self.request.GET.get(param_name)
        
        if value:
            try:
                # Try to convert the value to a float 
                self.validated[param_name] = float(value)
            except ValueError:
                self.invalid.append(f"{param_name} must be a valid number.")
        else:
            self.validated[param_name] = None

    def validate(self):
        if self.query_params:
            for key, rules in self.query_params.items():
                for rule in rules.split(","):
                    if rule == "float":
                        self.validate_float(key)

            if self.invalid:
                raise HTTPBadRequest(
                    f"Validation fields error: {' '.join(self.invalid)}"
                )

        return self.validated
