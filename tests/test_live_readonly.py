"""Live smoke tests tegen de echte Zermelo API — uitsluitend lezende tools.

Draaien met:
    ZERMELO_LIVE=1 ZERMELO_SCHOOL=coornhert-gymnasium.nl ZERMELO_TOKEN=... pytest -m live -v
"""

import os

import pytest
from mcp import Client

from zermelo_mcp.server import app

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(
        not (os.getenv("ZERMELO_LIVE") == "1" and os.getenv("ZERMELO_SCHOOL") and os.getenv("ZERMELO_TOKEN")),
        reason="Zet ZERMELO_LIVE=1, ZERMELO_SCHOOL en ZERMELO_TOKEN om live tests te draaien",
    ),
]

# Alleen GET-tools. Schrijvende tools worden hier bewust nooit aangeroepen.
READ_ONLY_CALLS = [
    ("get_appointments", {"start": "today", "end": "tomorrow"}, {"id", "start", "end"}),
    ("get_users", {"code": "~me"}, {"code"}),
    ("get_school_in_school_years", {}, {"id", "year"}),
    ("get_groups", {}, {"id", "name"}),
    ("get_locations", {}, {"id", "name"}),
    ("get_subjects", {}, {"id", "code"}),
    ("get_announcements", {}, {"id", "title"}),
]


async def call(name, args):
    async with Client(app) as client:
        return await client.call_tool(name, args)


def skip_if_forbidden(result):
    text = " ".join(getattr(b, "text", "") for b in result.content)
    if result.is_error and ("403" in text or "rechten" in text.lower()):
        pytest.skip(f"Geen rechten voor deze tool met dit token: {text}")


@pytest.mark.parametrize("tool, args, expected_keys", READ_ONLY_CALLS, ids=[c[0] for c in READ_ONLY_CALLS])
async def test_read_tool_live(tool, args, expected_keys):
    result = await call(tool, args)
    skip_if_forbidden(result)
    assert not result.is_error, result.content

    rows = result.structured_content["result"]
    assert isinstance(rows, list)
    for row in rows:
        assert expected_keys <= row.keys(), f"{tool}: ontbrekende velden in {row}"


async def test_my_appointments_this_week_live():
    result = await call("get_appointments", {"start": "today", "end": parse_week_end()})
    assert not result.is_error, result.content
    print(f"\n{len(result.structured_content['result'])} afspraken tot over 7 dagen")


async def test_partner_me_live():
    # Alleen partner-tokens mogen dit endpoint gebruiken; voor een gewoon token wordt de 403 als skip gemeld.
    result = await call("get_partner_me", {})
    skip_if_forbidden(result)
    assert not result.is_error, result.content


def parse_week_end():
    from zermelo_mcp.models import parse_to_timestamp

    return parse_to_timestamp("today") + 7 * 86400
