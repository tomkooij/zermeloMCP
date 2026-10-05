"""Functionele tests van de MCP-tools, in-process aangeroepen via de MCP-client met gemockte Zermelo HTTP."""

import json

import httpx
import pytest
import respx
from mcp import Client

from zermelo_mcp.models import parse_to_timestamp
from zermelo_mcp.server import app

BASE = "https://coornhert-gymnasium.zportal.nl/api/v3"


def envelope(data, status=200, message="OK", details=""):
    return {"response": {"status": status, "message": message, "details": details, "data": data}}


@pytest.fixture(autouse=True)
def zermelo_env(monkeypatch):
    monkeypatch.setenv("ZERMELO_SCHOOL", "coornhert-gymnasium.nl")
    monkeypatch.setenv("ZERMELO_TOKEN", "testtoken")
    monkeypatch.delenv("ZERMELO_API_VERSION", raising=False)


@pytest.fixture
def api():
    with respx.mock(assert_all_called=False) as mock:
        yield mock


class _InProcessMCP:
    """Opent per aanroep een in-process MCP-sessie (een async fixture-generator geeft anyio cancel-scope fouten)."""

    async def call_tool(self, name, arguments):
        async with Client(app) as client:
            return await client.call_tool(name, arguments)

    async def read_resource(self, uri):
        async with Client(app) as client:
            return await client.read_resource(uri)

    async def get_prompt(self, name, arguments):
        async with Client(app) as client:
            return await client.get_prompt(name, arguments)


@pytest.fixture
def mcp():
    return _InProcessMCP()


def params_of(route):
    return dict(route.calls.last.request.url.params)


def body_of(route):
    return json.loads(route.calls.last.request.content)


# --- Lezen -------------------------------------------------------------------

async def test_get_appointments_defaults(api, mcp):
    route = api.get(f"{BASE}/appointments").mock(
        return_value=httpx.Response(200, json=envelope([{"id": 1, "subjects": ["wisa"]}]))
    )

    result = await mcp.call_tool("get_appointments", {})

    assert not result.is_error
    assert result.structured_content == {"result": [{"id": 1, "subjects": ["wisa"]}]}
    p = params_of(route)
    assert p["user"] == "~me"
    assert p["valid"] == "true"
    assert p["start"] == str(parse_to_timestamp("today"))
    assert p["end"] == str(parse_to_timestamp("tomorrow"))
    assert "changeDescription" in p["fields"].split(",")
    assert p["access_token"] == "testtoken"


async def test_get_appointments_custom_args(api, mcp):
    route = api.get(f"{BASE}/appointments").mock(return_value=httpx.Response(200, json=envelope([])))

    await mcp.call_tool(
        "get_appointments",
        {
            "user": "abc",
            "start": "2026-10-05",
            "end": 1791504000,
            "valid_only": False,
            "school_in_school_year": 42,
            "fields": ["id", "start"],
        },
    )

    p = params_of(route)
    assert p["user"] == "abc"
    assert p["start"] == str(parse_to_timestamp("2026-10-05"))
    assert p["end"] == "1791504000"
    assert "valid" not in p
    assert p["schoolInSchoolYear"] == "42"
    assert p["fields"] == "id,start"


@pytest.mark.parametrize(
    "tool, args, endpoint, expected_params",
    [
        ("get_users", {"code": "~me", "role": "employee"}, "users", {"code": "~me", "role": "employee"}),
        ("get_users", {"is_active": True}, "users", {"archived": "false"}),
        ("get_users", {"is_active": False}, "users", {"archived": "true"}),
        ("get_groups", {"extended_name": "h4a", "school_in_school_year": 7}, "groupindepartments",
         {"extendedName": "h4a", "schoolInSchoolYear": "7"}),
        ("get_locations", {"name": "101"}, "locationofbranches", {"name": "101"}),
        ("get_subjects", {"name": "wisa"}, "subjectselectionsubjects", {"code": "wisa"}),
        ("get_announcements", {}, "announcements", {"user": "~me", "current": "true"}),
        ("get_announcements", {"current_only": False}, "announcements", {"user": "~me"}),
        ("get_participations", {"appointment_id": 99, "user": "abc"}, "appointmentparticipations",
         {"appointment": "99", "user": "abc"}),
        ("get_school_in_school_years", {"school_year": 2026}, "schoolsinschoolyears", {"year": "2026"}),
    ],
)
async def test_read_tools_query(api, mcp, tool, args, endpoint, expected_params):
    route = api.get(f"{BASE}/{endpoint}").mock(return_value=httpx.Response(200, json=envelope([{"id": 1}])))

    result = await mcp.call_tool(tool, args)

    assert not result.is_error, result.content
    assert result.structured_content == {"result": [{"id": 1}]}
    p = params_of(route)
    assert "fields" in p
    # Velden waarop een docent geen leesrecht heeft horen niet in de standaardvelden
    forbidden = {"get_users": {"id"}, "get_announcements": {"forStudents", "forEmployees"}}.get(tool, set())
    assert not forbidden & set(p["fields"].split(","))
    for key in ("archived", "current", "valid"):
        if key not in expected_params:
            assert key not in p
    for key, value in expected_params.items():
        assert p[key] == value


async def test_school_and_token_per_call_override_env(api, mcp):
    route = api.get("https://andereschool.zportal.nl/api/v3/subjectselectionsubjects").mock(
        return_value=httpx.Response(200, json=envelope([]))
    )

    result = await mcp.call_tool("get_subjects", {"school": "andereschool", "token": "calltoken"})

    assert not result.is_error
    request = route.calls.last.request
    assert request.headers["Authorization"] == "Bearer calltoken"
    assert request.url.params["access_token"] == "calltoken"


async def test_api_error_is_tool_error(api, mcp):
    api.get(f"{BASE}/users").mock(
        return_value=httpx.Response(403, json=envelope([], status=403, message="Geen rechten"))
    )
    result = await mcp.call_tool("get_users", {})
    assert result.is_error


async def test_api_error_message_reaches_model(api, mcp):
    api.get(f"{BASE}/users").mock(
        return_value=httpx.Response(403, json=envelope([], status=403, message="Geen rechten"))
    )
    result = await mcp.call_tool("get_users", {})
    assert result.is_error
    assert "403" in result.content[0].text and "Geen rechten" in result.content[0].text


async def test_invalid_date_reaches_model(api, mcp):
    result = await mcp.call_tool("get_appointments", {"start": "volgende week"})
    assert result.is_error
    assert "volgende week" in result.content[0].text


async def test_invalid_argument_rejected_without_http(api, mcp):
    route = api.delete(url__regex=r".*").mock(return_value=httpx.Response(200, json=envelope([])))
    result = await mcp.call_tool("delete_appointment", {"appointment_id": "abc"})
    assert result.is_error
    assert not route.called


# --- Schrijven: request-opbouw ----------------------------------------------
# Deze tests controleren alleen wat naar Zermelo gestuurd wordt; het resultaat van de tool
# wordt apart getest (zie test_dict_tools_handle_list_response).

async def test_create_appointment_payload(api, mcp):
    route = api.post(f"{BASE}/appointments").mock(return_value=httpx.Response(200, json=envelope([{"id": 5}])))

    await mcp.call_tool(
        "create_appointment",
        {
            "start": "2026-10-06T09:00:00",
            "end": "2026-10-06T10:00:00",
            "subjects": ["wisa"],
            "teachers": ["abc"],
            "start_time_slot": 2,
            "school_in_school_year": 42,
        },
    )

    assert body_of(route) == {
        "start": parse_to_timestamp("2026-10-06T09:00:00"),
        "end": parse_to_timestamp("2026-10-06T10:00:00"),
        "subjects": ["wisa"],
        "teachers": ["abc"],
        "groups": [],
        "locations": [],
        "type": "lesson",
        "remark": "",
        "valid": True,
        "startTimeSlot": 2,
        "schoolInSchoolYear": 42,
    }


async def test_update_appointment_sends_only_given_fields(api, mcp):
    route = api.put(f"{BASE}/appointments/123").mock(return_value=httpx.Response(200, json=envelope([])))

    await mcp.call_tool(
        "update_appointment",
        {"appointment_id": 123, "cancelled": True, "change_description": "Docent ziek", "locations": []},
    )

    assert body_of(route) == {"cancelled": True, "changeDescription": "Docent ziek", "locations": []}


async def test_delete_appointment(api, mcp):
    route = api.delete(f"{BASE}/appointments/123").mock(return_value=httpx.Response(200, json=envelope([])))
    await mcp.call_tool("delete_appointment", {"appointment_id": 123})
    assert route.called


async def test_create_announcement_payload(api, mcp):
    route = api.post(f"{BASE}/announcements").mock(return_value=httpx.Response(200, json=envelope([{"id": 8}])))

    await mcp.call_tool(
        "create_announcement",
        {"title": "Studiedag", "text": "Geen lessen", "start": "2026-10-06", "end": "2026-10-07", "for_students": False},
    )

    assert body_of(route) == {
        "title": "Studiedag",
        "text": "Geen lessen",
        "start": parse_to_timestamp("2026-10-06"),
        "end": parse_to_timestamp("2026-10-07"),
        "forStudents": False,
        "forEmployees": True,
    }


async def test_update_and_delete_announcement(api, mcp):
    put = api.put(f"{BASE}/announcements/8").mock(return_value=httpx.Response(200, json=envelope([])))
    delete = api.delete(f"{BASE}/announcements/8").mock(return_value=httpx.Response(200, json=envelope([])))

    await mcp.call_tool("update_announcement", {"announcement_id": 8, "title": "Nieuw", "for_employees": False})
    await mcp.call_tool("delete_announcement", {"announcement_id": 8})

    assert body_of(put) == {"title": "Nieuw", "forEmployees": False}
    assert delete.called


async def test_participations_write(api, mcp):
    post = api.post(f"{BASE}/appointmentparticipations").mock(return_value=httpx.Response(200, json=envelope([])))
    delete = api.delete(f"{BASE}/appointmentparticipations/77").mock(
        return_value=httpx.Response(200, json=envelope([]))
    )

    await mcp.call_tool("add_participation", {"appointment_id": 5, "user": "12345"})
    await mcp.call_tool("remove_participation", {"participation_id": 77})

    assert body_of(post) == {"appointment": 5, "user": "12345"}
    assert delete.called


async def test_exchange_auth_code_tool(api, mcp):
    route = api.post(f"{BASE}/oauth/token").mock(
        return_value=httpx.Response(200, json={"access_token": "newtoken", "token_type": "bearer"})
    )

    result = await mcp.call_tool("exchange_auth_code", {"school": "coornhert-gymnasium.nl", "auth_code": "123 456 789 012"})

    assert not result.is_error, result.content
    assert result.structured_content["result"]["access_token"] == "newtoken"
    assert "code=123456789012" in route.calls.last.request.content.decode()


# --- Zermelo levert 'data' altijd als lijst, ook bij schrijfacties ------------------

@pytest.mark.parametrize(
    "tool, args, method, endpoint",
    [
        ("get_partner_me", {}, "GET", "partners/~me"),
        ("create_appointment", {"start": 1, "end": 2}, "POST", "appointments"),
        ("update_appointment", {"appointment_id": 1, "remark": "x"}, "PUT", "appointments/1"),
        ("delete_appointment", {"appointment_id": 1}, "DELETE", "appointments/1"),
        ("create_announcement", {"title": "t", "text": "x"}, "POST", "announcements"),
        ("add_participation", {"appointment_id": 1, "user": "u"}, "POST", "appointmentparticipations"),
    ],
)
async def test_dict_tools_handle_list_response(api, mcp, tool, args, method, endpoint):
    api.route(method=method, url=f"{BASE}/{endpoint}").mock(
        return_value=httpx.Response(200, json=envelope([{"id": 1}]))
    )
    result = await mcp.call_tool(tool, args)
    assert not result.is_error, result.content
    assert result.structured_content == {"result": [{"id": 1}]}


@pytest.mark.parametrize(
    "tool, args, method, endpoint",
    [
        ("update_appointment", {"appointment_id": 1, "cancelled": True}, "PUT", "appointments/1"),
        ("delete_announcement", {"announcement_id": 1}, "DELETE", "announcements/1"),
    ],
)
async def test_write_tools_accept_empty_response(api, mcp, tool, args, method, endpoint):
    api.route(method=method, url=f"{BASE}/{endpoint}").mock(return_value=httpx.Response(204))
    result = await mcp.call_tool(tool, args)
    assert not result.is_error, result.content
    assert result.structured_content == {"result": []}


# --- Resource & prompt -------------------------------------------------------

async def test_config_resource(mcp):
    result = await mcp.read_resource("zermelo://config")
    info = json.loads(result.contents[0].text)
    assert info["school"] == "coornhert-gymnasium.nl"
    assert info["token_configured"] is True
    assert info["api_version"] == "v3"
    assert "testtoken" not in result.contents[0].text


async def test_daily_schedule_prompt(mcp):
    result = await mcp.get_prompt("daily_schedule", {"user": "abc", "date": "2026-10-06"})
    text = result.messages[0].content.text
    assert "'abc'" in text and "'2026-10-06'" in text and "get_appointments" in text
