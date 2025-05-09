"""
title: Kvadrat Intranet
author: Johannes Lindén
author_url: https://github.com/jolin1337
description: Tools that can tell you inside information about what is happening in kvadrat.
requirements: git+https://github.com/jolin1337/_duck_chat.git
version: 0.0.1
license: Apache 2.0
"""

import requests
from pydantic import BaseModel, Field
import json


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

    async def call_api(self, path, params={}):
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


class Tools:
    class Valves(BaseModel):
        KVADRAT_URL: str = Field(
            description="The url to intranet of kvadrat (base url of where you access your profile)"
        )
        USER_NAME: str = Field(description="Your email address")
        PASSWORD: str = Field(
            description="The password you can set in profile/Account -> Konto -> Lokal Inloggning"
        )

    def __init__(self):
        self.valves = self.Valves(
            **{
                "KVADRAT_URL": "",
                "USER_NAME": "",
                "PASSWORD": "",
            }
        )

    # Add your custom tools using pure Python code here, make sure to add type hints and descriptions

    async def get_user_name_and_email_and_id(
        self, __user__: dict = {}, __event_emitter__={}
    ) -> str:
        """
        Get the user's personal information such as name, phone number, E-post/E-mail and external user ID from the user object on intranet application.
        Hämtar användarens personliga information så som namn, telefonnummer, e-post/email och användarens AnvId som går att använda i andra funktioner.
        """
        util = ToolHelper(
            self.valves.KVADRAT_URL,
            self.valves.USER_NAME,
            self.valves.PASSWORD,
            __event_emitter__,
        )
        await util.emit_status("Calling get_user_name_and_email_and_id")
        resp = await util.call_api("/rest/InloggningsInformation/get")
        if "error" in resp:
            return
        result = ""
        for key, value in resp.get("System", {}).get("AktivAnvandare", {}).items():
            result += f"{key}: {value}\n"
        # await __event_emitter__(
        #    {
        #        "type": "message",
        #        "data": {"content": f"```json\n{json.dumps(resp)}\n```\n"},
        #    }
        # )
        await util.emit_status("", done=True)
        return result

    async def get_my_assignments(
        self,
        AnvId: int = None,
        __event_emitter__=None,
    ) -> str:
        """
        Hämtar alla nuvarande uppdrag för en användare givet dens externa användaid (AnvId som man kan hämta från `kvadrat_intranet/get_user_name_and_email_and_id`)
        Get the current assignments/uppdrag for a given extern user id
        param: AnvId -  kan hämtas ifrån `kvadrat_intranet/get_user_name_and_email_and_id`
        """
        util = ToolHelper(
            self.valves.KVADRAT_URL,
            self.valves.USER_NAME,
            self.valves.PASSWORD,
            __event_emitter__,
        )
        if AnvId is None:
            await util.emit_status(
                "Okänt AnvId, vi gör ett extra uppslag för att kika vilket detta är."
            )
            user_info = await util.call_api("/rest/InloggningsInformation/get")
            AnvId = user_info["System"]["AktivAnvandare"]["AnvId"]

        await util.emit_status("Calling uppdrag tool")
        resp = await util.call_api(f"/rest/UppdragFörAnvändare/get?id={AnvId}")
        if "error" in resp:
            return
        resp = {**resp, "AnvId": AnvId}
        await util.emit_message(f"```json\n{json.dumps(resp)}\n```\n")
        result = ""
        # return json.dumps(resp)
        for i, uppdrag in enumerate(resp.get("AktivaUppdrag", [])):
            result += f"\nUppdrag {i}: {uppdrag['Beskrivning']}\n"
            for key, value in uppdrag.items():
                result += f"{key}: {value}\n"
        await util.emit_status("", done=True)
        return result

    async def get_my_events(
        self,
        __event_emitter__=None,
    ) -> str:
        """
        Hämtar event/händelser som är inplanerade för användaren inom kvadrat.
        """
        util = ToolHelper(
            self.valves.KVADRAT_URL,
            self.valves.USER_NAME,
            self.valves.PASSWORD,
            __event_emitter__,
        )
        await util.emit_status("Calling myevent tool")
        resp = await util.call_api(f"/rest/EventOchNyheterFörAnvändare/get")
        if "error" in resp:
            return
        await util.emit_message(f"```json\n{json.dumps(resp['MinKalender'])}\n```\n")
        await util.emit_status("", done=True)
        return json.dumps(resp["MinKalender"])

    async def get_my_news(
        self,
        __event_emitter__=None,
    ) -> str:
        """
        Hämtar nyheter som är specifikt för användaren inom kvadrat.
        """
        util = ToolHelper(
            self.valves.KVADRAT_URL,
            self.valves.USER_NAME,
            self.valves.PASSWORD,
            __event_emitter__,
        )
        await util.emit_status("Calling mynews tool")
        resp = await util.call_api(f"/rest/EventOchNyheterFörAnvändare/get")
        if "error" in resp:
            return
        await util.emit_message(f"```json\n{json.dumps(resp['SenasteNytt'])}\n```\n")
        await util.emit_status("", done=True)
        return json.dumps(resp["SenasteNytt"])
        result = ""
        # return json.dumps(resp)
        for i, (kalender, items) in enumerate(resp.items()):
            result += f"\nKalender {i}: {kalender}\n"
            for item in items:
                for key, value in item.items():
                    result += f"{key}: {value}\n"
        return result

    async def get_all_events(
        self,
        AnvId: int = None,
        __event_emitter__=None,
    ) -> str:
        """
        Hämtar nyheter som skrivits om inom kvadrat.
        param: AnvId -  kan hämtas ifrån `kvadrat_intranet/get_user_name_and_email_and_id`
        """
        util = ToolHelper(
            self.valves.KVADRAT_URL,
            self.valves.USER_NAME,
            self.valves.PASSWORD,
            __event_emitter__,
        )
        if AnvId is None:
            await util.emit_status(
                "Okänt AnvId, vi gör ett extra uppslag för att kika vilket detta är."
            )
            user_info = await util.call_api("/rest/InloggningsInformation/get")
            AnvId = user_info["System"]["AktivAnvandare"]["AnvId"]

        await util.emit_status("Calling mynews tool")
        resp = await util.call_api(f"/rest/KonsultNyheter/get?id={AnvId}")
        if "error" in resp:
            return
        await util.emit_message(f"```json\n{json.dumps(resp)}\n```\n")
        await util.emit_status("", done=True)
        return json.dumps(resp)
        result = ""
        # return json.dumps(resp)
        for i, (kalender, items) in enumerate(resp.items()):
            result += f"\nKalender {i}: {kalender}\n"
            for item in items:
                for key, value in item.items():
                    result += f"{key}: {value}\n"
        return result
