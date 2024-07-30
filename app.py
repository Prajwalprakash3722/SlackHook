# author : @prajwal.p
# created_at: Fri 26 Jul 2024 17:03:33 IST
# updated_at: Mon Jul 29 2024 14:37:55 IST 
import os
import logging
import time
from aiohttp import web
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

token = os.getenv("SLACK_BOT_TOKEN")
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
        "presence": "away",
        "status_expiration": None,
    },
    "work": {
        "active": True,
        "status": "Available",
        "notification": True,
        "status_emoji": "",
        "presence": "auto",
        "status_expiration": None,
    },
    "dnd": {
        "active": True,
        "status": "Focusing",
        "notification": False,
        "status_emoji": ":technologist:",
        "presence": "auto",
        "status_expiration": 30,
    },
    "commuting": {
        "active": True,
        "status": "Commuting",
        "notification": True,
        "status_emoji": ":bus:",
        "presence": "auto",
        "status_expiration": 60,
    },
    "clear": {},
    "lunch": {
        "active": True,
        "status": "Lunch",
        "notification": True,
        "status_emoji": ":lunch-:",
        "presence": "auto",
        "status_expiration": 60,
    },
    "cncall`": {
        "active": True,
        "status": "Oncall",
        "notification": True,
        "status_emoji": ":alert:",
        "presence": "auto",
        "status_expiration": 60*7,
    },
}

async def update_slack(update_func, **kwargs) -> None:
    """General function to handle Slack updates."""
    try:
        response = await update_func(**kwargs)
        response.validate()
    except SlackApiError as e:
        logger.error(f"Slack API error: {e.response['error']}")
        raise

def build_profile(focus_mode: str) -> Dict[str, Any]:
    """Build the profile based on the focus mode."""
    if focus_mode == "clear":
        return {"status_text": "", "status_emoji": ""}
    
    mode = focus_modes.get(focus_mode, {})
    status_text = mode.get("status", "")
    status_emoji = mode.get("status_emoji", "")
    status_expiration = mode.get("status_expiration", None)
    
    profile = {
        "status_text": status_text,
        "status_emoji": status_emoji,
    }
    
    if status_expiration is not None:
        current_time = int(time.time())
        expiration_timestamp = current_time + (status_expiration * 60)
        profile["status_expiration"] = expiration_timestamp
    
    return profile

async def handle_update_status(request: web.Request) -> web.Response:
    """Handle requests to update the user's Slack status."""
    focus_mode = request.query.get("focus_mode")
    if not focus_mode or focus_mode not in focus_modes:
        return web.json_response(data={"success": False, "error": "Invalid or missing focus_mode"}, status=400)
    
    profile = build_profile(focus_mode)
    presence = focus_modes[focus_mode]["presence"]
    notifications = focus_modes[focus_mode]["notification"]

    try:
        # Update user profile
        logger.info(f"Setting {focus_mode} mode with profile: {profile}")
        await update_slack(client.users_profile_set, profile=profile)

        # Update presence
        logger.info(f"Setting user presence to {presence}")
        await update_slack(client.users_setPresence, presence=presence)

        # Update snooze notifications
        logger.info(f"Setting user snooze notifications to {notifications}")
        if notifications:
            await update_slack(client.dnd_endSnooze)
        else:
            time_till_snooze = 12 * 60  # default is 12 hour snooze
            await update_slack(client.dnd_setSnooze, num_minutes=time_till_snooze)

        return web.json_response(data={"success": True})

    except SlackApiError as e:

        logger.error(f"Failed to update Slack: {e}")
        return web.json_response(data={"success": False, "error": str(e)}, status=500)

async def handle_success(request: web.Request) -> web.Response:
    """Health check route."""
    return web.json_response(data={"ok": True}, status=200)

app = web.Application()
app.add_routes([web.get("/", handle_success), web.get("/update", handle_update_status)])

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=3000)
