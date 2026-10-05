"""Async HTTP Client for interacting with the Zermelo API."""

import os
import logging
from typing import Any, Dict, List, Optional, Union
import httpx

logger = logging.getLogger("zermelo_mcp.client")


class ZermeloAPIError(Exception):
    """Raised when the Zermelo API returns an error."""
    def __init__(self, status: int, message: str, details: str = ""):
        self.status = status
        self.message = message
        self.details = details
        super().__init__(f"Zermelo API Error [{status}]: {message} {f'({details})' if details else ''}")


class ZermeloClient:
    """Async Client for Zermelo REST API."""
    
    def __init__(
        self,
        school: Optional[str] = None,
        token: Optional[str] = None,
        api_version: Optional[str] = None,
        timeout: float = 30.0,
    ):
        self._school = school
        self._token = token
        self._api_version = api_version
        self.timeout = timeout

    @property
    def school(self) -> Optional[str]:
        return self._school or os.getenv("ZERMELO_SCHOOL")

    @property
    def token(self) -> Optional[str]:
        return self._token or os.getenv("ZERMELO_TOKEN")

    @property
    def api_version(self) -> str:
        return self._api_version or os.getenv("ZERMELO_API_VERSION", "v3")

    def get_base_url(self, custom_school: Optional[str] = None, custom_api_version: Optional[str] = None) -> str:
        """Construct the base API URL for the specified school and API version."""
        school = custom_school or self.school
        if not school:
            raise ValueError(
                "School identifier is missing. Provide 'school' in request or set ZERMELO_SCHOOL environment variable."
            )
        
        school = school.strip().lower()
        if school.startswith("http://") or school.startswith("https://"):
            base = school.rstrip("/")
        elif "zportal.nl" in school:
            base = f"https://{school}"
        else:
            subdomain = school.split(".")[0]
            base = f"https://{subdomain}.zportal.nl"

        version = custom_api_version if custom_api_version is not None else self.api_version
        if version and not base.endswith(f"/api/{version}"):
            if not base.endswith("/api"):
                base = f"{base}/api/{version.lstrip('/')}"
            else:
                base = f"{base}/{version.lstrip('/')}"
                
        return base.rstrip("/")

    def get_headers(self, custom_token: Optional[str] = None) -> Dict[str, str]:
        """Get HTTP headers for authentication."""
        token = custom_token or self.token
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "ZermeloMCP/0.1.0 (Python)",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Union[Dict[str, Any], List[Any]]] = None,
        data: Optional[Dict[str, Any]] = None,
        custom_school: Optional[str] = None,
        custom_token: Optional[str] = None,
    ) -> Any:
        """Send HTTP request to Zermelo API and parse response."""
        base_url = self.get_base_url(custom_school=custom_school)
        endpoint_clean = endpoint.lstrip("/")
        url = f"{base_url}/{endpoint_clean}"

        token = custom_token or self.token
        headers = self.get_headers(custom_token=token)

        request_params: Dict[str, Any] = {}
        if params:
            for k, v in params.items():
                if v is not None:
                    if isinstance(v, bool):
                        request_params[k] = "true" if v else "false"
                    elif isinstance(v, (list, tuple)):
                        request_params[k] = ",".join(str(item) for item in v)
                    else:
                        request_params[k] = str(v)

        # Attach access_token parameter as fallback
        if token and "access_token" not in request_params:
            request_params["access_token"] = token

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.request(
                    method=method.upper(),
                    url=url,
                    headers=headers,
                    params=request_params,
                    json=json_data,
                    data=data,
                )
                response.raise_for_status()
                # PUT/DELETE may answer with an empty body (e.g. 204 No Content)
                res_json = response.json() if response.content.strip() else []
            except httpx.HTTPStatusError as e:
                try:
                    res_json = e.response.json()
                except Exception:
                    raise ZermeloAPIError(e.response.status_code, f"HTTP Error {e.response.status_code}: {e.response.text}") from e
            except Exception as e:
                raise ZermeloAPIError(500, f"Request failed: {str(e)}") from e

        # Handle Zermelo JSON response format: {"response": {"status": 200, "message": "OK", "data": [...]}}
        if isinstance(res_json, dict) and "response" in res_json:
            api_resp = res_json["response"]
            status = api_resp.get("status", 200)
            message = api_resp.get("message", "OK")
            details = api_resp.get("details", "")
            
            if status != 200:
                raise ZermeloAPIError(status, message, details)
            
            return api_resp.get("data", [])
        
        return res_json

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        custom_school: Optional[str] = None,
        custom_token: Optional[str] = None,
    ) -> Any:
        """GET request."""
        return await self.request("GET", endpoint, params=params, custom_school=custom_school, custom_token=custom_token)

    async def post(
        self,
        endpoint: str,
        json_data: Optional[Union[Dict[str, Any], List[Any]]] = None,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        custom_school: Optional[str] = None,
        custom_token: Optional[str] = None,
    ) -> Any:
        """POST request."""
        return await self.request(
            "POST", endpoint, params=params, json_data=json_data, data=data, custom_school=custom_school, custom_token=custom_token
        )

    async def put(
        self,
        endpoint: str,
        json_data: Optional[Union[Dict[str, Any], List[Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        custom_school: Optional[str] = None,
        custom_token: Optional[str] = None,
    ) -> Any:
        """PUT request."""
        return await self.request(
            "PUT", endpoint, params=params, json_data=json_data, custom_school=custom_school, custom_token=custom_token
        )

    async def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        custom_school: Optional[str] = None,
        custom_token: Optional[str] = None,
    ) -> Any:
        """DELETE request."""
        return await self.request("DELETE", endpoint, params=params, custom_school=custom_school, custom_token=custom_token)

    async def exchange_auth_code(self, school: str, auth_code: str) -> Dict[str, Any]:
        """Exchange an authentication code for an OAuth access token."""
        clean_code = auth_code.replace(" ", "").strip()
        data = {
            "grant_type": "authorization_code",
            "code": clean_code,
        }
        
        base_url = self.get_base_url(custom_school=school)
        token_url = f"{base_url}/oauth/token"
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(token_url, data=data)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                raise ZermeloAPIError(400, f"Failed to exchange auth code: {str(e)}") from e
