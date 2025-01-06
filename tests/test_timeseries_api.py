"""Class for testing Timeseries API"""

from datetime import date, datetime
from faker import Faker


class TestTimeseriesAPI:
    def test_success_fetch_timeseries_data(
        self, testapp, seed_time_series_data
    ) -> None:
        res = testapp.get("/api/v1/timeseries", status=200)

        assert (
            res.status_code == 200
        ), f"Expected status code 200 but got {res.status_code}"
        assert (
            res.content_type == "application/json"
        ), "Response content type is not JSON"

        json_data = res.json

        assert isinstance(json_data, list), "Response should be a list"

    def test_response_schema_validation(self, testapp) -> None:
        res = testapp.get("/api/v1/timeseries", status=200)

        assert (
            res.status_code == 200
        ), f"Expected status code 200 but got {res.status_code}"
        assert (
            res.content_type == "application/json"
        ), "Response content type is not JSON"

        json_data = res.json

        for item in json_data:
            assert all(
                key in item for key in ["datetime", "value"]
            ), "Each item should contain 'datetime' and 'value'"

    def test_notfound_response_on_unexist_timeseries_endpoint(self, testapp) -> None:
        res = testapp.get("/api/v1/timeserie", status=404)

        assert (
            res.status_code == 404
        ), f"Expected status code 404 but got {res.status_code}"
        assert (
            res.content_type == "application/json"
        ), "Response content type is not JSON"

        json_data = res.json
        assert json_data.get("status") == "error", "Status should be 'error'"
        assert "message" in json_data, "Error message should be provided"

    def test_success_fetch_filtered_timeseries_data_with_start_date_only(
        self, testapp
    ) -> None:
        fake = Faker()
        random_date = fake.date_time_between_dates(date(2000, 1, 1), date(2024, 12, 31))
        res = testapp.get(f"/api/v1/timeseries?start_date={random_date}", status=200)

        assert (
            res.status_code == 200
        ), f"Expected status code 200 but got {res.status_code}"
        assert (
            res.content_type == "application/json"
        ), "Response content type is not JSON"

        json_data = res.json
        assert isinstance(json_data, list), "Response should be a list"
        assert all(
            datetime.fromisoformat(item["datetime"]) >= random_date
            for item in json_data
        ), f"Response contains data before {random_date}"

    def test_success_fetch_filtered_timeseries_data_with_end_date_only(
        self, testapp
    ) -> None:
        fake = Faker()
        random_date = fake.date_time_between_dates(date(2000, 1, 1), date(2024, 12, 31))
        res = testapp.get(f"/api/v1/timeseries?end_date={random_date}", status=200)

        assert (
            res.status_code == 200
        ), f"Expected status code 200 but got {res.status_code}"
        assert (
            res.content_type == "application/json"
        ), "Response content type is not JSON"

        json_data = res.json

        assert isinstance(json_data, list), "Response should be a list"
        assert all(
            datetime.fromisoformat(item["datetime"]) <= random_date
            for item in json_data
        ), f"Response contains data after {random_date}"

    def test_success_fetch_filtered_timeseries_data_between_start_date_and_end_date(
        self, testapp
    ) -> None:

        fake = Faker()

        random_start_date = fake.date_time_between_dates(
            date(2000, 1, 1), date(2011, 12, 31)
        )
        random_end_date = fake.date_time_between_dates(
            date(2015, 1, 1), date(2024, 12, 31)
        )

        res = testapp.get(
            f"/api/v1/timeseries?start_date={random_start_date}&end_date={random_end_date}",
            status=200,
        )

        assert (
            res.status_code == 200
        ), f"Expected status code 200 but got {res.status_code}"
        assert (
            res.content_type == "application/json"
        ), "Response content type is not JSON"

        json_data = res.json

        assert isinstance(json_data, list), "Response should be a list"
        assert all(
            random_start_date
            <= datetime.fromisoformat(item["datetime"])
            <= random_end_date
            for item in json_data
        ), f"Response contains data outside the range {random_start_date} - {random_end_date}"

    def test_fail_when_try_fetch_filtered_timeseries_data_with_wrong_format_date(
        self, testapp
    ) -> None:

        res = testapp.get(
            "/api/v1/timeseries?start_date=2002-03-0d&end_date=wrong", status=400
        )

        assert res.status_code == 400, f"Expected status 400 but got {res.status_code}"
        assert (
            res.content_type == "application/json"
        ), "Response content type is not JSON"

        json_data = res.json

        assert json_data.get("status") == "error", "Status should be 'error'"
        assert "message" in json_data, "Error message should be provided"

    def test_fail_when_start_date_is_later_than_end_date(self, testapp) -> None:
        fake = Faker()

        random_start_date = fake.date_between_dates(
            date(2015, 1, 1), date(2024, 12, 31)
        )
        random_end_date = fake.date_between_dates(date(2000, 1, 1), date(2014, 12, 31))

        res = testapp.get(
            f"/api/v1/timeseries?start_date={random_start_date}&end_date={random_end_date}",
            status=400,
        )

        assert (
            res.status_code == 400
        ), f"Expected status code 400 but got {res.status_code}"
        assert (
            res.content_type == "application/json"
        ), "Response content type is not JSON"

        json_data = res.json

        assert json_data.get("status") == "error", "Status should be 'error'"
        assert "message" in json_data, "Error message should be provided"

    def test_empty_response_for_non_matching_filter(self, testapp) -> None:

        res = testapp.get(
            "/api/v1/timeseries?start_date=3000-01-01&end_date=3000-12-31", status=200
        )

        assert (
            res.status_code == 200
        ), f"Expected status code 200 but got {res.status_code}"
        assert (
            res.content_type == "application/json"
        ), "Response content type is not JSON"

        json_data = res.json

        assert isinstance(json_data, list), "Response should be a list"
        assert len(json_data) == 0, "Response should be empty for non-matching filters"
