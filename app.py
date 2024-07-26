# author : @prajwal.p
# CreatedAt: Fri 26 Jul 2024 17:03:33 IST
import os
from aiohttp import web
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError

token = os.getenv('SLACK_BOT_TOKEN')

client = AsyncWebClient(token=token)

focus_modes = {
    "personal": {
        "active": False,
        "status": "",
        "notification": False,
        "status_emoji": ""
    },
    "work": {
        "active": True,
        "status": "Available",
        "notification": True,
        "status_emoji": ""
    },
    "dnd": {
        "active": True,
        "status": "Focusing",
        "notification": False,
        "status_emoji": ":technologist:"
    },
    "commuting": {
        "active": True,
        "status": "Commuting",
        "notification": True,
        "status_emoji": ":bus:"
    }
}

# def build_userPreference(focus_mode):    

def build_profile(focus_mode):
    if focus_mode == "clear":
        return {"status_text": "", "status_emoji": ""}
    profile = {"status_text": focus_modes[focus_mode]["status"]}
    if "status_emoji" in focus_modes[focus_mode]:
        profile["status_emoji"] = focus_modes[focus_mode]["status_emoji"]
    return profile

async def handle_update_status(request: web.Request) -> web.Response:
    focus_mode = request.query.get("focus_mode")
    profile = build_profile(focus_mode)
    print(f'Setting {focus_mode} {profile} mode')
    # the following can be abstracted to a method
    try:
        response = await client.users_profile_set(profile=profile)
        assert response["ok"]
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert not e.response["ok"]
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")
        # Also receive a corresponding status_code
        assert isinstance(e.response.status_code, int)
        print(f"Received a response status_code: {e.response.status_code}")
        return web.json_response(data={"success": False, "error": e.response['error']}, status=500)
    return web.json_response(data={"success": True})

async def handle_success(request: web.Request) -> web.Response:
    return web.json_response(data={"ok": True})

app = web.Application()
app.add_routes([
    web.get("/", handle_success),
    web.get("/update", handle_update_status)
])

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=3000)


