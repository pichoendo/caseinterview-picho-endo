"""HTTP Error Handlers."""

import logging
import traceback
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPInternalServerError, HTTPBadRequest
from pyramid_app_caseinterview.utils.utils import find_closest_route

log = logging.getLogger(__name__)

# Custom error handler for HTTP 404 (Not Found)
@view_config(context=HTTPNotFound)
def not_found_error(request):

    # Find the closest route that might match the user's request
    closest_route = find_closest_route(request)

    # Prepare the error response message
    message = message = f"The endpoint you requested could not be found. {'Did you mean ' + closest_route + '?' if closest_route else ''} Please check our documentation for more details."
    response = {"status": "error", "message": message}
        
    # Return the response with status 404 (Not Found)
    return Response(json_body=response, status=404)


# Custom error handler for HTTP 500 (Internal Server Error)
@view_config(context=HTTPInternalServerError)
def internal_server_error(request):

    # Log the real error message for debugging purposes
    log.error("Internal Server Error")
    log.error(traceback.format_exc())

    response = {
        "status": "error",
        "message": "An unexpected error occurred on the server. Please try again later or contact support if the issue persists.",
    }

    # Return the response with status 500 (Internal Server Error)
    return Response(
        json_body=response,
        status=500,
    )


# Custom error handler for HTTP 400 (Bad request)
@view_config(context=HTTPBadRequest)
def bad_request_error(request):

    # Log the real error message for debugging purposes
    error_message = str(request.exception)

    response = {
        "status": "error",
        "message": f"One or more fields in the request failed validation. Please review and correct your input: {error_message}.",
    }

    # Return the response with status 400 (Bad Request)
    return Response(
        json_body=response,
        status=400,
    )


# Custom error handler for general error exception
@view_config(context=Exception)
def general_error(request):

    # Log the real error message for debugging purposes
    log.error("General Error: An unexpected error occurred.")
    log.error("Error details: %s", traceback.format_exc())

    response = {
        "status": "error",
        "message": "An unexpected error occurred. Please try again later.",
    }

    # Return the response with status 500 (Internal Server Error)
    return Response(
        json_body=response,
        status=500,
    )
