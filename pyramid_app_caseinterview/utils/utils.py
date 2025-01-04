"""Utility functions for project."""

import difflib

def list_all_routes(request):
    """Retrieve all available routes from the request's registry."""
    introspector = request.registry.introspector
    routes = introspector.get_category("routes")
    return [route["introspectable"]["pattern"] for route in routes]


def find_closest_route(request):
    """Find the closest matching route with a similarity threshold."""
    requested_url = request.path_info
    closest_matches = difflib.get_close_matches(
        requested_url, list_all_routes(request), n=1, cutoff=0.8
    )
    return closest_matches[0] if closest_matches else None
