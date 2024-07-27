# author : @prajwal.p
# created_at: Fri 26 Jul 2024 17:03:33 IST
import os
import logging
from aiohttp import web
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

token = os.getenv('SLACK_BOT_TOKEN')
if not token:
    raise EnvironmentError("SLACK_BOT_TOKEN is not set")

client = AsyncWebClient(token=token)

# Focus modes (refer README for more details) 
focus_modes: Dict[str, Dict[str, Any]] = {
    "personal": {
        "active": False,
        "status": "",
        "notification": False,
        "status_emoji": "",
        "presence": "Away"
    },
    "work": {
        "active": True,
        "status": "Available",
        "notification": True,
        "status_emoji": "",
        "presence": "Active"
    },
    "dnd": {
        "active": True,
        "status": "Focusing",
        "notification": False,
        "status_emoji": ":technologist:",
        "presence": "Active"
    },
    "commuting": {
        "active": True,
        "status": "Commuting",
        "notification": True,
        "status_emoji": ":bus:",
        "presence": "Active"
    }
}

def build_profile(focus_mode: str) -> Dict[str, Any]:
    """Build the profile dictionary based on the focus mode."""
    if focus_mode == "clear":
        return {"status_text": "", "status_emoji": ""}
    mode = focus_modes.get(focus_mode, {})
    return {
        "status_text": mode.get("status", ""),
        "status_emoji": mode.get("status_emoji", "")
    }

async def send_slack_profile(client: AsyncWebClient, profile: Dict[str, Any]) -> None:
    """Send the updated profile status to Slack."""
    try:
        response = await client.users_profile_set(profile=profile)
        response.validate()
    except SlackApiError as e:
        logger.error(f"Error setting profile: {e.response['error']}")
        raise

async def send_slack_user_presence(client: AsyncWebClient, presence: str) -> None:
    """Set the user's presence status on Slack."""
    try:
        response = await client.users_setPresence(presence=presence)
        response.validate()
    except SlackApiError as e:
        logger.error(f"Error setting presence: {e.response['error']}")
        raise

async def send_slack_user_snooze(client: AsyncWebClient, notifications: bool) -> None:
    """Control the user's Do Not Disturb settings on Slack."""
    try:
        if notifications:
            response = await client.dnd_endSnooze()
        else:
            response = await client.dnd_setSnooze()
        response.validate()
    except SlackApiError as e:
        logger.error(f"Error setting snooze: {e.response['error']}")
        raise

async def handle_update_status(request: web.Request) -> web.Response:
    """Handle requests to update the user's Slack status."""
    focus_mode = request.query.get("focus_mode")
    if focus_mode and focus_mode in focus_modes:
        profile = build_profile(focus_mode)
        logger.info(f'Setting {focus_mode} mode with profile: {profile}')
        await send_slack_profile(client, profile)
        await send_slack_user_presence(client, focus_modes[focus_mode]["presence"])
        await send_slack_user_snooze(client, focus_modes[focus_mode]["notification"])
        return web.json_response(data={"success": True})
    return web.json_response(data={"success": False, "error": "Invalid or missing focus_mode"})

async def handle_success(request: web.Request) -> web.Response:
    """Health check route."""
    return web.json_response(data={"ok": True})

app = web.Application()

app.add_routes([
    web.get("/", handle_success),
    web.get("/update", handle_update_status)
])

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=3000)