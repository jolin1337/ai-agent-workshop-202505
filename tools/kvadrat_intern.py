import requests
from pydantic import BaseModel, Field
import json
import os
from mcp.server.fastmcp import FastMCP


class ToolHelper:
    def __init__(self, url, user, password, event_emitter=None):
        self.event_emitter = event_emitter
        self.KVADRAT_URL = url
        self.USER_NAME = user
        self.PASSWORD = password

    async def emit_status(self, status_msg, done=False):
        if self.event_emitter:
            await self.event_emitter(
                {
                    "type": "status",
                    "data": {
                        "description": status_msg,
                        "done": done,
                    },
                }
            )

    async def emit_message(self, msg):
        if self.event_emitter:
            await self.event_emitter(
                {
                    "type": "message",
                    "data": {"content": msg},
                }
            )

    async def call_api(self, path, params={}) -> dict:
        # TODO: use params for modifying endpoints, and derive requests method by the path ending (e.g. path/endpoint/get -> get)
        try:
            resp = requests.get(
                f"{self.KVADRAT_URL}{path}",
                auth=(self.USER_NAME, self.PASSWORD),
            ).json()
            return resp
        except Exception as e:
            print("Error:", e)
            if self.event_emitter:
                await self.emit_message(
                    f"Error requestion intranet api, check the credentials, {str(e)}"
                )
            return {"error": str(e)}


util = ToolHelper(
    os.environ.get("KVADRAT_URL", "http://localhost:8080"),
    os.environ.get("USER_NAME", "foo"),
    os.environ.get("PASSWORD", "***"),
)

server = FastMCP("Kvadrat intranät")


@server.tool()
async def get_user_name_and_email_and_id() -> dict:
    """
    Get the user's personal information such as name, phone number, E-post/E-mail and external user ID from the user object on intranet application.
    Hämtar användarens personliga information så som namn, telefonnummer, e-post/email och användarens AnvId som går att använda i andra funktioner.
    """
    await util.emit_status("Calling get_user_name_and_email_and_id")
    resp = await util.call_api("/rest/InloggningsInformation/get")
    return resp


@server.tool()
async def get_my_assignments(
    AnvId: int | None = None, max_assignments: int = 3
) -> list:
    """
    Hämtar alla nuvarande uppdrag för en användare givet dens externa användaid (AnvId som man kan hämta från `kvadrat_intranet/get_user_name_and_email_and_id`)
    Get the current assignments/uppdrag for a given extern user id
    param: AnvId -  kan hämtas ifrån `kvadrat_intranet/get_user_name_and_email_and_id`
    param max_assignments - set this to 3
    """
    if AnvId is None:
        await util.emit_status(
            "Okänt AnvId, vi gör ett extra uppslag för att kika vilket detta är."
        )
        user_info: dict = await util.call_api("/rest/InloggningsInformation/get")
        AnvId = user_info["System"]["AktivAnvandare"]["AnvId"]

    await util.emit_status("Calling uppdrag tool")
    resp = await util.call_api(f"/rest/UppdragFörAnvändare/get?id={AnvId}")
    if "error" in resp:
        await util.emit_status(
            "Okänt AnvId, vi gör ett extra uppslag för att kika vilket detta är."
        )
        user_info: dict = await util.call_api("/rest/InloggningsInformation/get")
        AnvId = user_info["System"]["AktivAnvandare"]["AnvId"]
        await util.emit_status("Calling uppdrag tool")
        resp = await util.call_api(f"/rest/UppdragFörAnvändare/get?id={AnvId}")
    if not max_assignments or int(max_assignments) <= 0:
        max_assignments = 3
    return resp.get("AktivaUppdrag", [resp])[: int(max_assignments)]


@server.tool()
async def get_my_events(max_events: int = 3) -> list:
    """
    Hämtar event/händelser som är inplanerade för användaren inom kvadrat.
    @param max_events - set this to 3
    """
    await util.emit_status("Calling myevent tool")
    resp = await util.call_api("/rest/EventOchNyheterFörAnvändare/get")
    if not max_events or int(max_events) <= 0:
        max_events = 3
    return resp.get("MinKalender", [resp])[: int(max_events)]


@server.tool()
async def get_my_news(max_news: int = 3) -> list:
    """
    Hämtar nyheter som är specifikt för användaren inom kvadrat.
    @param max_news - set this to 3
    """
    await util.emit_status("Calling mynews tool")
    resp = await util.call_api("/rest/EventOchNyheterFörAnvändare/get")
    if not max_news or int(max_news) <= 0:
        max_news = 3
    return resp.get("SenasteNytt", [resp])[: int(max_news)]


@server.tool()
async def get_all_events(
    AnvId: int | None = None,
) -> dict:
    """
    Hämtar nyheter som skrivits om inom kvadrat.
    param: AnvId -  kan hämtas ifrån `kvadrat_intranet/get_user_name_and_email_and_id`
    """
    if AnvId is None:
        await util.emit_status(
            "Okänt AnvId, vi gör ett extra uppslag för att kika vilket detta är."
        )
        user_info = await util.call_api("/rest/InloggningsInformation/get")
        AnvId = user_info["System"]["AktivAnvandare"]["AnvId"]

    await util.emit_status("Calling mynews tool")
    resp = await util.call_api(f"/rest/KonsultNyheter/get?id={AnvId}")
    if "error" in resp:
        await util.emit_status(
            "Okänt AnvId, vi gör ett extra uppslag för att kika vilket detta är."
        )
        user_info: dict = await util.call_api("/rest/InloggningsInformation/get")
        AnvId = user_info["System"]["AktivAnvandare"]["AnvId"]
        await util.emit_status("Calling uppdrag tool")
        resp = await util.call_api(f"/rest/UppdragFörAnvändare/get?id={AnvId}")
    return resp
