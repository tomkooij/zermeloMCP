import pytest
from datetime import datetime, timezone
from zermelo_mcp.client import ZermeloClient, ZermeloAPIError
from zermelo_mcp.models import parse_to_timestamp, AppointmentCreate, AnnouncementCreate


def test_base_url_building():
    client = ZermeloClient(school="testschool")
    assert client.get_base_url() == "https://testschool.zportal.nl/api/v3"

    client2 = ZermeloClient(school="myschool.zportal.nl", api_version="v3")
    assert client2.get_base_url() == "https://myschool.zportal.nl/api/v3"

    client3 = ZermeloClient(school="https://custom.zportal.nl/api/v3")
    assert client3.get_base_url() == "https://custom.zportal.nl/api/v3"


def test_parse_to_timestamp():
    ts = parse_to_timestamp(1700000000)
    assert ts == 1700000000

    ts_str = parse_to_timestamp("1700000000")
    assert ts_str == 1700000000

    ts_date = parse_to_timestamp("2026-01-01")
    expected = int(datetime(2026, 1, 1, tzinfo=timezone.utc).timestamp())
    assert ts_date == expected

    ts_today = parse_to_timestamp("today")
    assert isinstance(ts_today, int)
    assert ts_today > 0


def test_appointment_model():
    appt = AppointmentCreate(
        start=1700000000,
        end=1700003600,
        subjects=["wisa"],
        teachers=["abc"],
        groups=["h4a"],
        locations=["101"],
    )
    d = appt.to_api_dict()
    assert d["start"] == 1700000000
    assert d["subjects"] == ["wisa"]
    assert d["type"] == "lesson"
