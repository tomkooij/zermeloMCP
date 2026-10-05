import pytest
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from zermelo_mcp.client import ZermeloClient, ZermeloAPIError
from zermelo_mcp.models import parse_to_timestamp, AppointmentCreate, AnnouncementCreate


AMS = ZoneInfo("Europe/Amsterdam")


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
    expected = int(datetime(2026, 1, 1, tzinfo=AMS).timestamp())
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


@pytest.mark.parametrize(
    "value, expected",
    [
        ("05-10-2026", datetime(2026, 10, 5, tzinfo=AMS)),
        ("2026-10-05 09:30:00", datetime(2026, 10, 5, 9, 30, tzinfo=AMS)),
        ("2026-10-05T09:30:00+0000", datetime(2026, 10, 5, 9, 30, tzinfo=timezone.utc)),
        ("  2026-10-05  ", datetime(2026, 10, 5, tzinfo=AMS)),
    ],
)
def test_parse_to_timestamp_formats(value, expected):
    assert parse_to_timestamp(value) == int(expected.timestamp())


def test_parse_to_timestamp_relative_words():
    today = parse_to_timestamp("today")
    assert datetime.fromtimestamp(today, AMS).hour == 0
    assert 23 * 3600 <= parse_to_timestamp("tomorrow") - today <= 25 * 3600  # zomer-/wintertijd
    assert 23 * 3600 <= today - parse_to_timestamp("yesterday") <= 25 * 3600
    assert today <= parse_to_timestamp("now") < today + 25 * 3600


def test_parse_to_timestamp_naive_times_are_dutch_local_time():
    # 09:00 zonder offset betekent 09:00 Nederlandse tijd (oktober: 07:00 UTC, januari: 08:00 UTC)
    assert parse_to_timestamp("2026-10-06T09:00:00") == int(datetime(2026, 10, 6, 7, tzinfo=timezone.utc).timestamp())
    assert parse_to_timestamp("2026-01-06T09:00:00") == int(datetime(2026, 1, 6, 8, tzinfo=timezone.utc).timestamp())
    assert parse_to_timestamp(datetime(2026, 10, 6, 9)) == parse_to_timestamp("2026-10-06T09:00:00")


@pytest.mark.parametrize("value", ["volgende week", "2026/10/05", ""])
def test_parse_to_timestamp_invalid(value):
    with pytest.raises(ValueError):
        parse_to_timestamp(value)
