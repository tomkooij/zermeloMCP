import pytest
from zermelo_mcp.server import app


@pytest.mark.asyncio
async def test_list_tools():
    tools = await app.list_tools()
    tool_names = [t.name for t in tools]
    
    # Check Read Tools
    assert "get_appointments" in tool_names
    assert "get_users" in tool_names
    assert "get_groups" in tool_names
    assert "get_locations" in tool_names
    assert "get_subjects" in tool_names
    assert "get_announcements" in tool_names
    assert "get_participations" in tool_names
    assert "get_school_in_school_years" in tool_names
    assert "get_partner_me" in tool_names

    # Check Write Tools
    assert "create_appointment" in tool_names
    assert "update_appointment" in tool_names
    assert "delete_appointment" in tool_names
    assert "create_announcement" in tool_names
    assert "update_announcement" in tool_names
    assert "delete_announcement" in tool_names
    assert "add_participation" in tool_names
    assert "remove_participation" in tool_names
    assert "exchange_auth_code" in tool_names


@pytest.mark.asyncio
async def test_resources():
    resources = await app.list_resources()
    resource_uris = [str(r.uri) for r in resources]
    assert "zermelo://config" in resource_uris
