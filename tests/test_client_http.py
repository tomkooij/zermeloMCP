import json

import httpx
import pytest
import respx

from zermelo_mcp.client import ZermeloAPIError, ZermeloClient

BASE = "https://coornhert-gymnasium.zportal.nl/api/v3"


def envelope(data, status=200, message="OK", details=""):
    return {"response": {"status": status, "message": message, "details": details, "data": data}}


@pytest.mark.parametrize(
    "school, expected",
    [
        ("coornhert-gymnasium.nl", BASE),
        ("Coornhert-Gymnasium", BASE),
        ("  coornhert-gymnasium  ", BASE),
        ("coornhert-gymnasium.zportal.nl", BASE),
        ("coornhert-gymnasium.zportal.nl/api", BASE),
        ("https://coornhert-gymnasium.zportal.nl/", BASE),
        ("https://coornhert-gymnasium.zportal.nl/api/v3", BASE),
    ],
)
def test_base_url_normalization(school, expected):
    assert ZermeloClient(school=school).get_base_url() == expected


def test_base_url_custom_api_version():
    client = ZermeloClient(school="coornhert-gymnasium", api_version="v2")
    assert client.get_base_url() == "https://coornhert-gymnasium.zportal.nl/api/v2"


def test_missing_school_raises(monkeypatch):
    monkeypatch.delenv("ZERMELO_SCHOOL", raising=False)
    with pytest.raises(ValueError):
        ZermeloClient().get_base_url()


def test_env_vars_resolved_lazily(monkeypatch):
    monkeypatch.delenv("ZERMELO_SCHOOL", raising=False)
    monkeypatch.delenv("ZERMELO_TOKEN", raising=False)
    client = ZermeloClient()
    monkeypatch.setenv("ZERMELO_SCHOOL", "coornhert-gymnasium.nl")
    monkeypatch.setenv("ZERMELO_TOKEN", "envtoken")
    assert client.get_base_url() == BASE
    assert client.get_headers()["Authorization"] == "Bearer envtoken"


def test_explicit_values_override_env(monkeypatch):
    monkeypatch.setenv("ZERMELO_SCHOOL", "andereschool")
    monkeypatch.setenv("ZERMELO_TOKEN", "envtoken")
    client = ZermeloClient(school="coornhert-gymnasium", token="explicit")
    assert client.get_base_url() == BASE
    assert client.get_headers()["Authorization"] == "Bearer explicit"


def test_no_token_no_auth_header(monkeypatch):
    monkeypatch.delenv("ZERMELO_TOKEN", raising=False)
    assert "Authorization" not in ZermeloClient(school="x").get_headers()


@respx.mock
async def test_get_serializes_params_and_unwraps_data():
    route = respx.get(f"{BASE}/appointments").mock(
        return_value=httpx.Response(200, json=envelope([{"id": 1}]))
    )
    client = ZermeloClient(school="coornhert-gymnasium", token="tok")

    result = await client.get(
        "/appointments",
        params={"valid": True, "archived": False, "fields": ["id", "start"], "skip": None, "start": 123},
    )

    assert result == [{"id": 1}]
    request = route.calls.last.request
    assert dict(request.url.params) == {
        "valid": "true",
        "archived": "false",
        "fields": "id,start",
        "start": "123",
        "access_token": "tok",
    }
    assert request.headers["Authorization"] == "Bearer tok"


@respx.mock
async def test_explicit_access_token_param_not_overwritten():
    route = respx.get(f"{BASE}/users").mock(return_value=httpx.Response(200, json=envelope([])))
    client = ZermeloClient(school="coornhert-gymnasium", token="tok")
    await client.get("users", params={"access_token": "other"})
    assert route.calls.last.request.url.params["access_token"] == "other"


@respx.mock
async def test_post_and_put_send_json_body():
    post = respx.post(f"{BASE}/announcements").mock(return_value=httpx.Response(200, json=envelope([{"id": 9}])))
    put = respx.put(f"{BASE}/announcements/9").mock(return_value=httpx.Response(200, json=envelope([])))
    client = ZermeloClient(school="coornhert-gymnasium", token="tok")

    await client.post("announcements", json_data={"title": "x"})
    await client.put("announcements/9", json_data={"text": "y"})

    assert json.loads(post.calls.last.request.content) == {"title": "x"}
    assert json.loads(put.calls.last.request.content) == {"text": "y"}


@respx.mock
async def test_non_enveloped_json_returned_as_is():
    respx.get(f"{BASE}/raw").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
    assert await ZermeloClient(school="coornhert-gymnasium").get("raw") == {"foo": "bar"}


@respx.mock
async def test_empty_body_returns_empty_list():
    respx.delete(f"{BASE}/appointments/1").mock(return_value=httpx.Response(204))
    assert await ZermeloClient(school="coornhert-gymnasium").delete("appointments/1") == []


@respx.mock
async def test_envelope_error_status_raises():
    respx.get(f"{BASE}/users").mock(
        return_value=httpx.Response(200, json=envelope([], status=403, message="Forbidden", details="geen rechten"))
    )
    with pytest.raises(ZermeloAPIError) as exc:
        await ZermeloClient(school="coornhert-gymnasium").get("users")
    assert exc.value.status == 403
    assert exc.value.message == "Forbidden"
    assert exc.value.details == "geen rechten"


@pytest.mark.parametrize("status", [401, 404])
@respx.mock
async def test_http_error_with_envelope_raises_with_status(status):
    respx.get(f"{BASE}/users/~me").mock(
        return_value=httpx.Response(status, json=envelope([], status=status, message="Niet ingelogd"))
    )
    with pytest.raises(ZermeloAPIError) as exc:
        await ZermeloClient(school="coornhert-gymnasium").get("users/~me")
    assert exc.value.status == status


@respx.mock
async def test_http_error_without_json_raises():
    respx.get(f"{BASE}/users").mock(return_value=httpx.Response(502, text="Bad Gateway"))
    with pytest.raises(ZermeloAPIError) as exc:
        await ZermeloClient(school="coornhert-gymnasium").get("users")
    assert exc.value.status == 502
    assert "Bad Gateway" in exc.value.message


@respx.mock
async def test_http_error_with_non_enveloped_json_is_returned():
    # Documenteert huidig gedrag (kandidaat-bug): een HTTP-fout met JSON zonder
    # "response"-envelop wordt niet als fout gemeld maar als resultaat teruggegeven.
    respx.get(f"{BASE}/users").mock(return_value=httpx.Response(500, json={"error": "boom"}))
    assert await ZermeloClient(school="coornhert-gymnasium").get("users") == {"error": "boom"}


@respx.mock
async def test_network_error_raises_500():
    respx.get(f"{BASE}/users").mock(side_effect=httpx.ConnectError("unreachable"))
    with pytest.raises(ZermeloAPIError) as exc:
        await ZermeloClient(school="coornhert-gymnasium").get("users")
    assert exc.value.status == 500


@respx.mock
async def test_exchange_auth_code_posts_form_data():
    route = respx.post(f"{BASE}/oauth/token").mock(
        return_value=httpx.Response(200, json={"access_token": "newtoken", "token_type": "bearer"})
    )
    result = await ZermeloClient().exchange_auth_code("coornhert-gymnasium.nl", " 123 456 789 012 ")

    assert result["access_token"] == "newtoken"
    body = route.calls.last.request.content.decode()
    assert "grant_type=authorization_code" in body
    assert "code=123456789012" in body


@respx.mock
async def test_exchange_auth_code_failure_raises_400():
    respx.post(f"{BASE}/oauth/token").mock(return_value=httpx.Response(400, json={"error": "invalid_grant"}))
    with pytest.raises(ZermeloAPIError) as exc:
        await ZermeloClient().exchange_auth_code("coornhert-gymnasium", "000000000000")
    assert exc.value.status == 400
