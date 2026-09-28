"""Zermelo MCP Server implementation."""

import json
from typing import Any, Dict, List, Optional, Union
from mcp.server.mcpserver import MCPServer
from zermelo_mcp.client import ZermeloClient, ZermeloAPIError
from zermelo_mcp.models import parse_to_timestamp

# Create MCPServer instance
app = MCPServer("zermelo-mcp")
client = ZermeloClient()


@app.tool()
async def get_appointments(
    user: str = "~me",
    start: Union[str, int] = "today",
    end: Union[str, int] = "tomorrow",
    valid_only: bool = True,
    school_in_school_year: Optional[int] = None,
    fields: Optional[List[str]] = None,
    school: Optional[str] = None,
    token: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Ophalen van roosterafspraken voor een gebruiker (~me, leerlingcode of docentcode) tussen twee tijdstippen.

    Args:
        user: Gebruikerscode of '~me' (standaard: '~me').
        start: Begintijd (bijv. 'today', '2026-09-28', '2026-09-28T08:00:00' of UNIX timestamp).
        end: Eindtijd (bijv. 'tomorrow', '2026-09-29', of UNIX timestamp).
        valid_only: Alleen geldige afspraken ophalen (standaard: True).
        school_in_school_year: Optioneel schoolInSchoolYear ID.
        fields: Lijst van gewenste velden (standaard: id, start, end, subjects, teachers, groups, locations, type, remark, valid, cancelled, changeDescription).
        school: Optionele schoolnaam (overschrijft ZERMELO_SCHOOL).
        token: Optioneel token (overschrijft ZERMELO_TOKEN).
    """
    start_ts = parse_to_timestamp(start)
    end_ts = parse_to_timestamp(end)

    default_fields = [
        "id", "start", "end", "startTimeSlot", "endTimeSlot",
        "subjects", "teachers", "groups", "locations", "type",
        "remark", "valid", "cancelled", "changeDescription", "appointmentInstance"
    ]
    query_fields = fields or default_fields

    params: Dict[str, Any] = {
        "user": user,
        "start": start_ts,
        "end": end_ts,
        "fields": query_fields,
    }
    if valid_only:
        params["valid"] = True
    if school_in_school_year is not None:
        params["schoolInSchoolYear"] = school_in_school_year

    return await client.get("appointments", params=params, custom_school=school, custom_token=token)


@app.tool()
async def get_users(
    code: Optional[str] = None,
    role: Optional[str] = None,
    is_active: bool = True,
    school_in_school_year: Optional[int] = None,
    fields: Optional[List[str]] = None,
    school: Optional[str] = None,
    token: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Opvragen en zoeken van gebruikers (leerlingen, docenten, medewerkers) in Zermelo.

    Args:
        code: Zoeken op specifieke gebruikerscode.
        role: Filteren op rol ('student', 'employee', enz.).
        is_active: Alleen actieve gebruikers (standaard: True).
        school_in_school_year: Optioneel schoolInSchoolYear ID.
        fields: Lijst van velden om op te vragen.
        school: Optionele schoolnaam.
        token: Optioneel token.
    """
    default_fields = ["id", "code", "firstName", "prefix", "lastName", "roles", "archived"]
    params: Dict[str, Any] = {
        "fields": fields or default_fields,
    }
    if code:
        params["code"] = code
    if role:
        params["role"] = role
    if is_active:
        params["archived"] = False
    if school_in_school_year is not None:
        params["schoolInSchoolYear"] = school_in_school_year

    return await client.get("users", params=params, custom_school=school, custom_token=token)


@app.tool()
async def get_groups(
    extended_name: Optional[str] = None,
    school_in_school_year: Optional[int] = None,
    fields: Optional[List[str]] = None,
    school: Optional[str] = None,
    token: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Opvragen van klas- en lesgroepen.

    Args:
        extended_name: Zoeken op de naam van de groep.
        school_in_school_year: Optioneel schoolInSchoolYear ID.
        fields: Gewenste velden.
        school: Optionele schoolnaam.
        token: Optioneel token.
    """
    default_fields = ["id", "name", "extendedName", "schoolInSchoolYear"]
    params: Dict[str, Any] = {
        "fields": fields or default_fields,
    }
    if extended_name:
        params["extendedName"] = extended_name
    if school_in_school_year is not None:
        params["schoolInSchoolYear"] = school_in_school_year

    return await client.get("groups", params=params, custom_school=school, custom_token=token)


@app.tool()
async def get_locations(
    name: Optional[str] = None,
    school_in_school_year: Optional[int] = None,
    fields: Optional[List[str]] = None,
    school: Optional[str] = None,
    token: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Opvragen van lokalen en ruimtes.

    Args:
        name: Zoeken op lokaalnaam (bijv. '101').
        school_in_school_year: Optioneel schoolInSchoolYear ID.
        fields: Gewenste velden.
        school: Optionele schoolnaam.
        token: Optioneel token.
    """
    default_fields = ["id", "name", "building"]
    params: Dict[str, Any] = {
        "fields": fields or default_fields,
    }
    if name:
        params["name"] = name
    if school_in_school_year is not None:
        params["schoolInSchoolYear"] = school_in_school_year

    return await client.get("locations", params=params, custom_school=school, custom_token=token)


@app.tool()
async def get_subjects(
    name: Optional[str] = None,
    fields: Optional[List[str]] = None,
    school: Optional[str] = None,
    token: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Opvragen van schoolvakken.

    Args:
        name: Vakcode of naam (bijv. 'wisa').
        fields: Gewenste velden.
        school: Optionele schoolnaam.
        token: Optioneel token.
    """
    default_fields = ["id", "name"]
    params: Dict[str, Any] = {
        "fields": fields or default_fields,
    }
    if name:
        params["name"] = name

    return await client.get("subjects", params=params, custom_school=school, custom_token=token)


@app.tool()
async def get_announcements(
    user: str = "~me",
    current_only: bool = True,
    fields: Optional[List[str]] = None,
    school: Optional[str] = None,
    token: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Opvragen van schoolmededelingen.

    Args:
        user: Gebruikerscode of '~me'.
        current_only: Alleen actieve mededelingen ophalen (standaard: True).
        fields: Gewenste velden.
        school: Optionele schoolnaam.
        token: Optioneel token.
    """
    default_fields = ["id", "title", "text", "start", "end", "forStudents", "forEmployees"]
    params: Dict[str, Any] = {
        "user": user,
        "fields": fields or default_fields,
    }
    if current_only:
        params["current"] = True

    return await client.get("announcements", params=params, custom_school=school, custom_token=token)


@app.tool()
async def get_participations(
    appointment_id: Optional[int] = None,
    user: Optional[str] = None,
    fields: Optional[List[str]] = None,
    school: Optional[str] = None,
    token: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Opvragen van afspraakdeelnames (welke personen/groepen nemen deel aan welke les).

    Args:
        appointment_id: Filter op afspraak ID.
        user: Filter op gebruikerscode.
        fields: Gewenste velden.
        school: Optionele schoolnaam.
        token: Optioneel token.
    """
    default_fields = ["id", "appointment", "user", "optional", "student", "employee"]
    params: Dict[str, Any] = {
        "fields": fields or default_fields,
    }
    if appointment_id is not None:
        params["appointment"] = appointment_id
    if user:
        params["user"] = user

    return await client.get("appointmentparticipations", params=params, custom_school=school, custom_token=token)


@app.tool()
async def get_school_in_school_years(
    school_year: Optional[int] = None,
    fields: Optional[List[str]] = None,
    school: Optional[str] = None,
    token: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Opvragen van school-in-schooljaar informatie.

    Args:
        school_year: Filter op specifiek schooljaar ID.
        fields: Gewenste velden.
        school: Optionele schoolnaam.
        token: Optioneel token.
    """
    default_fields = ["id", "schoolYear", "school"]
    params: Dict[str, Any] = {
        "fields": fields or default_fields,
    }
    if school_year is not None:
        params["schoolYear"] = school_year

    return await client.get("schoolinschoolyears", params=params, custom_school=school, custom_token=token)


@app.tool()
async def get_partner_me(
    school: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """Inzien van de toegangsrechten van de partner / API token (/partners/~me).

    Args:
        school: Optionele schoolnaam.
        token: Optioneel token.
    """
    return await client.get("partners/~me", custom_school=school, custom_token=token)


@app.tool()
async def create_appointment(
    start: Union[str, int],
    end: Union[str, int],
    subjects: Optional[List[str]] = None,
    teachers: Optional[List[str]] = None,
    groups: Optional[List[str]] = None,
    locations: Optional[List[str]] = None,
    type: str = "lesson",
    remark: str = "",
    valid: bool = True,
    start_time_slot: Optional[int] = None,
    end_time_slot: Optional[int] = None,
    school_in_school_year: Optional[int] = None,
    school: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """Aanmaken van een nieuwe afspraak / roosterles in Zermelo.

    Args:
        start: Begintijd (bijv. '2026-09-28T09:00:00' of UNIX timestamp).
        end: Eindtijd (bijv. '2026-09-28T10:00:00' of UNIX timestamp).
        subjects: Lijst van vakcodes (bijv. ['wisa']).
        teachers: Lijst van docentcodes (bijv. ['abc']).
        groups: Lijst van groepcodes (bijv. ['h4a']).
        locations: Lijst van lokaalcodes (bijv. ['101']).
        type: Type afspraak ('lesson', 'exam', 'activity', etc.).
        remark: Opmerking bij de afspraak.
        valid: Of de afspraak geldig is.
        start_time_slot: Optioneel uur/tijdslot.
        end_time_slot: Optioneel eind uur/tijdslot.
        school_in_school_year: Optioneel schoolInSchoolYear ID.
        school: Optionele schoolnaam.
        token: Optioneel token.
    """
    start_ts = parse_to_timestamp(start)
    end_ts = parse_to_timestamp(end)

    payload: Dict[str, Any] = {
        "start": start_ts,
        "end": end_ts,
        "subjects": subjects or [],
        "teachers": teachers or [],
        "groups": groups or [],
        "locations": locations or [],
        "type": type,
        "remark": remark,
        "valid": valid,
    }
    if start_time_slot is not None:
        payload["startTimeSlot"] = start_time_slot
    if end_time_slot is not None:
        payload["endTimeSlot"] = end_time_slot
    if school_in_school_year is not None:
        payload["schoolInSchoolYear"] = school_in_school_year

    return await client.post("appointments", json_data=payload, custom_school=school, custom_token=token)


@app.tool()
async def update_appointment(
    appointment_id: int,
    start: Optional[Union[str, int]] = None,
    end: Optional[Union[str, int]] = None,
    subjects: Optional[List[str]] = None,
    teachers: Optional[List[str]] = None,
    groups: Optional[List[str]] = None,
    locations: Optional[List[str]] = None,
    type: Optional[str] = None,
    remark: Optional[str] = None,
    valid: Optional[bool] = None,
    cancelled: Optional[bool] = None,
    change_description: Optional[str] = None,
    school: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """Bewerken / aanpassen van een bestaande roosterafspraak.

    Args:
        appointment_id: Het unieke ID van de afspraak.
        start: Optionele nieuwe begintijd.
        end: Optionele nieuwe eindtijd.
        subjects: Optionele lijst van vakcodes.
        teachers: Optionele lijst van docentcodes.
        groups: Optionele lijst van groepcodes.
        locations: Optionele lijst van lokaalcodes.
        type: Optioneel nieuw type.
        remark: Optionele opmerking.
        valid: Optionele status geldigheid.
        cancelled: Of de afspraak geannuleerd is.
        change_description: Reden of omschrijving van de wijziging.
        school: Optionele schoolnaam.
        token: Optioneel token.
    """
    payload: Dict[str, Any] = {}
    if start is not None:
        payload["start"] = parse_to_timestamp(start)
    if end is not None:
        payload["end"] = parse_to_timestamp(end)
    if subjects is not None:
        payload["subjects"] = subjects
    if teachers is not None:
        payload["teachers"] = teachers
    if groups is not None:
        payload["groups"] = groups
    if locations is not None:
        payload["locations"] = locations
    if type is not None:
        payload["type"] = type
    if remark is not None:
        payload["remark"] = remark
    if valid is not None:
        payload["valid"] = valid
    if cancelled is not None:
        payload["cancelled"] = cancelled
    if change_description is not None:
        payload["changeDescription"] = change_description

    endpoint = f"appointments/{appointment_id}"
    return await client.put(endpoint, json_data=payload, custom_school=school, custom_token=token)


@app.tool()
async def delete_appointment(
    appointment_id: int,
    school: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """Verwijderen of annuleren van een afspraak.

    Args:
        appointment_id: ID van de te verwijderen afspraak.
        school: Optionele schoolnaam.
        token: Optioneel token.
    """
    endpoint = f"appointments/{appointment_id}"
    return await client.delete(endpoint, custom_school=school, custom_token=token)


@app.tool()
async def create_announcement(
    title: str,
    text: str,
    start: Union[str, int] = "today",
    end: Union[str, int] = "tomorrow",
    for_students: bool = True,
    for_employees: bool = True,
    school: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """Plaatsen van een nieuwe schoolmededeling.

    Args:
        title: Titel van de mededeling.
        text: Inhoud/tekst van de mededeling.
        start: Begintijd.
        end: Eindtijd.
        for_students: Zichtbaar voor leerlingen.
        for_employees: Zichtbaar voor medewerkers.
        school: Optionele schoolnaam.
        token: Optioneel token.
    """
    start_ts = parse_to_timestamp(start)
    end_ts = parse_to_timestamp(end)

    payload = {
        "title": title,
        "text": text,
        "start": start_ts,
        "end": end_ts,
        "forStudents": for_students,
        "forEmployees": for_employees,
    }
    return await client.post("announcements", json_data=payload, custom_school=school, custom_token=token)


@app.tool()
async def update_announcement(
    announcement_id: int,
    title: Optional[str] = None,
    text: Optional[str] = None,
    start: Optional[Union[str, int]] = None,
    end: Optional[Union[str, int]] = None,
    for_students: Optional[bool] = None,
    for_employees: Optional[bool] = None,
    school: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """Bewerken van een bestaande schoolmededeling.

    Args:
        announcement_id: ID van de mededeling.
        title: Optionele nieuwe titel.
        text: Optionele nieuwe tekst.
        start: Optionele nieuwe begintijd.
        end: Optionele nieuwe eindtijd.
        for_students: Zichtbaarheid voor leerlingen.
        for_employees: Zichtbaarheid voor medewerkers.
        school: Optionele schoolnaam.
        token: Optioneel token.
    """
    payload: Dict[str, Any] = {}
    if title is not None:
        payload["title"] = title
    if text is not None:
        payload["text"] = text
    if start is not None:
        payload["start"] = parse_to_timestamp(start)
    if end is not None:
        payload["end"] = parse_to_timestamp(end)
    if for_students is not None:
        payload["forStudents"] = for_students
    if for_employees is not None:
        payload["forEmployees"] = for_employees

    endpoint = f"announcements/{announcement_id}"
    return await client.put(endpoint, json_data=payload, custom_school=school, custom_token=token)


@app.tool()
async def delete_announcement(
    announcement_id: int,
    school: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """Verwijderen van een schoolmededeling.

    Args:
        announcement_id: ID van de mededeling.
        school: Optionele schoolnaam.
        token: Optioneel token.
    """
    endpoint = f"announcements/{announcement_id}"
    return await client.delete(endpoint, custom_school=school, custom_token=token)


@app.tool()
async def add_participation(
    appointment_id: int,
    user: str,
    school: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """Toevoegen van een deelnemer (gebruikerscode) aan een afspraak.

    Args:
        appointment_id: ID van de afspraak.
        user: Gebruikerscode van de deelnemer.
        school: Optionele schoolnaam.
        token: Optioneel token.
    """
    payload = {
        "appointment": appointment_id,
        "user": user,
    }
    return await client.post("appointmentparticipations", json_data=payload, custom_school=school, custom_token=token)


@app.tool()
async def remove_participation(
    participation_id: int,
    school: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """Verwijderen van een afspraakdeelname.

    Args:
        participation_id: ID van de deelname record.
        school: Optionele schoolnaam.
        token: Optioneel token.
    """
    endpoint = f"appointmentparticipations/{participation_id}"
    return await client.delete(endpoint, custom_school=school, custom_token=token)


@app.tool()
async def exchange_auth_code(
    school: str,
    auth_code: str,
) -> Dict[str, Any]:
    """Omwisselen van een eenmalige 12-cijferige Koppelcode / Authcode voor een Zermelo access token.

    Args:
        school: Naam van de school (bijv. 'mijnschool').
        auth_code: De 12-cijferige koppelcode uit het Zermelo Portal.
    """
    return await client.exchange_auth_code(school=school, auth_code=auth_code)


@app.resource("zermelo://config")
def get_config_resource() -> str:
    """Geeft de huidige MCP server configuratie weer."""
    info = {
        "server": "zermelo-mcp",
        "version": "0.1.0",
        "school": client.school or "Niet ingesteld (gebruik ZERMELO_SCHOOL omgevingsvariabele of meegeven per tool)",
        "token_configured": bool(client.token),
        "api_version": client.api_version,
    }
    return json.dumps(info, indent=2)


@app.prompt("daily_schedule")
def daily_schedule_prompt(user: str = "~me", date: str = "today") -> str:
    """Genereert een prompt om het dagrooster en eventuele lesuitval op te vragen."""
    return f"Haal het rooster op van gebruiker '{user}' voor de datum '{date}' via get_appointments en geef een overzichtelijk chronologisch overzicht inclusief vakken, docenten, lokalen en eventuele roosterwijzigingen of uitval."
