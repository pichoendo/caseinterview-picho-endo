"""Sel value API"""

from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config

from pyramid_app_caseinterview.models.depthseries import Depthseries
from pyramid_app_caseinterview.models.timeseries import Timeseries

from . import View


class API(View):
    """API endpoints"""

    @view_config(
        route_name="timeseries",
        permission=NO_PERMISSION_REQUIRED,
        renderer="json",
        request_method="GET",
    )
    def timeseries_api(self):
        query = self.session.query(Timeseries)
        return [
            {
                "id": str(q.id),
                "datetime": q.datetime,
                "value": q.value,
            }
            for q in query.all()
        ]

    @view_config(
        route_name="depthseries",
        permission=NO_PERMISSION_REQUIRED,
        renderer="json",
        request_method="GET",
    )
    def depthseries_api(self):
        query = self.session.query(Depthseries)
        return [
            {
                "id": str(q.id),
                "depth": q.depth,
                "value": q.value,
            }
            for q in query.all()
        ]
"""Sel value API"""

from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config

from pyramid_app_caseinterview.models.depthseries import Depthseries
from pyramid_app_caseinterview.models.timeseries import Timeseries
from pyramid_app_caseinterview.utils.query_param_validator import QueryParamValidator
from pyramid.httpexceptions import HTTPBadRequest

from . import View


class API(View):
    """API endpoints"""

    @view_config(
        route_name="timeseries",
        permission=NO_PERMISSION_REQUIRED,
        renderer="json",
        request_method="GET",
    )
    def timeseries_api(self):
        # Initialize the query parameter validator for 'start_date' and 'end_date' with 'date' as the expected format
        params = QueryParamValidator(
            self.request, start_date="date", end_date="date"
        ).validate()

        # Ensure the start_date is not later than the end_date
        if (
            params["start_date"]
            and params["end_date"]
            and params["start_date"] > params["end_date"]
        ):
            raise HTTPBadRequest("start_date cannot be later than end_date")

        # Start building the query for the Timeseries model
        query = self.session.query(Timeseries)

        # Apply the 'start_date' filter if provided
        if params["start_date"]:
            query = query.filter(Timeseries.datetime >= params["start_date"])
            
        # Apply the 'end_date' filter if provided
        if params["end_date"]:
            query = query.filter(Timeseries.datetime <= params["end_date"])

        return [
            {
                "id": str(q.id),
                "datetime": q.datetime,
                "value": q.value,
            }
            for q in query.all()
        ]

    @view_config(
        route_name="depthseries",
        permission=NO_PERMISSION_REQUIRED,
        renderer="json",
        request_method="GET",
    )
    def depthseries_api(self):
        query = self.session.query(Depthseries)
        return [
            {
                "id": str(q.id),
                "depth": q.depth,
                "value": q.value,
            }
            for q in query.all()
        ]
