"""Sel value API"""

from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config

from pyramid_app_caseinterview.models.depthseries import Depthseries
from pyramid_app_caseinterview.models.timeseries import Timeseries
from pyramid.httpexceptions import HTTPBadRequest

from pyramid_app_caseinterview.utils.query_param_validator import QueryParamValidator
from pyramid_app_caseinterview.utils.utils import generate_csv
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

        # Using DISTINCT on 'depth' to avoid duplicate entries in the Depthseries query and filter null value on 'value' field
        query = (
            self.session.query(Depthseries)
            .distinct(Depthseries.depth)
            .filter(Depthseries.value.isnot(None))
        )

        return [
            {
                "id": str(q.id),
                "depth": q.depth,
                "value": q.value,
            }
            for q in query.all()
        ]

    @view_config(
        route_name="download_depthseries",
        permission=NO_PERMISSION_REQUIRED,
        request_method="GET",
    )
    def download_depthseries_api(self):
        # Initialize the query parameter validator for 'min_depth' and 'max_depth' with 'float' as the expected format
        params = QueryParamValidator(
            self.request, min_depth="float", max_depth="float"
        ).validate()

        # Ensure the min_depth is not higher than the max_depth
        if (
            params["min_depth"]
            and params["max_depth"]
            and params["min_depth"] > params["max_depth"]
        ):
            raise HTTPBadRequest("min_depth cannot be higher than max_depth")
        
        # Using DISTINCT on 'depth' to avoid duplicate entries in the Depthseries query and filter null value on 'value' field
        query = (
            self.session.query(Depthseries)
            .distinct(Depthseries.depth)
            .filter(Depthseries.value.isnot(None))
        )
      
        # Apply the 'min_depth' filter if provided
        if params["min_depth"]:
            query = query.filter(Depthseries.depth >= params["min_depth"])

        # Apply the 'max_depth' filter if provided
        if params["max_depth"]:
            query = query.filter(Depthseries.depth <= params["max_depth"])

        data = [
            {
                "id": str(q.id),
                "depth": q.depth,
                "value": q.value,
            }
            for q in query.all()
        ]

        return generate_csv(["id", "depth", "value"], data)
