"""Class to validate query parameters in incoming requests"""

from datetime import datetime
from pyramid.httpexceptions import HTTPBadRequest


class QueryParamValidator:

    def __init__(self, request=None, **query_params):
        self.request = request
        self.invalid = []
        self.validated = {}
        self.query_params = query_params or {}

    def validate_date_format(self, param_name):
        """Validate if the date is in ISO format."""
        date_str = self.request.GET.get(param_name)
        try:
            # If the date exists, attempt to parse it
            self.validated[param_name] = (
                datetime.fromisoformat(date_str) if date_str else None
            )
        except ValueError:
            # If parsing fails, add an error message
            self.invalid.append(
                f"Invalid date format for {param_name}. Please use (YYYY-MM-DD) format."
            )

    def validate(self):
        if self.query_params:
            for key, rules in self.query_params.items():
                for rule in rules.split(","):
                    if rule == "date":
                        self.validate_date_format(key)

            if self.invalid:
                raise HTTPBadRequest(
                    f"Validation fields error: {' '.join(self.invalid)}"
                )

        return self.validated
