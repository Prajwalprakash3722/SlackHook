# SlackHook v0.1

This script allows you to update your Slack status via a GET request from any component with a valid token. It's particularly useful for integrating with iPhone Shortcuts, enabling you to automate status updates based on your custom routines and schedules.

# Practical Usecase:

- I use iPhone focus modes heavily, I have multiple focus modes: for learning, working, reading, etc. There is also one I use for deep work. When doing deep work, I want to avoid being distracted by anything, and therefore I mute almost every app, including Slack.

At the end of the day, it's just a **overengineered product** :)

![automation](https://www.milner.com/images/default-source/articles/buzz.png?sfvrsn=e0080dd3_2)



Here are Some Of my iPhone Modes

Focus Modes:
- Personal
- Work
- DND
- Commuting

Status Updates: 
1. Personal
     - active: False
    - status: Nil
    - Pause notification
2. Work
    - active: True
    - status: Available
    - Unpause notification
3. DND
    - active: True
    - status: Focusing :technologist:
    - Pause notification
4. Commuting
    - active: True
    - status: :bus: Commuting
    - Unpause notification

## TODO
1. Get the Estimated time to commute and send the status expiration only for commuting

## Running Locally

1. Export the `SLACK_BOT_TOKEN` to environment
2. Install all requirements `pip3 install -r requirements.txt`
3. Run
    - using python: `python3 app.py`
    - using gunicorn: `gunicorn app:app --bind localhost:3000 --worker-class aiohttp.GunicornWebWorker --workers=4`

## Getting Started

To use this script, you will need:

A valid Slack API token with the following Scopes:

- dnd:read
- dnd:write
- users.profile:read
- users.profile:write
- users:read
- users:write

The iPhone Shortcuts app configured to trigger the script.

## Example Workflow

- **Set Up Your Focus Modes:** Define your Focus modes on your iPhone for activities like deep work, learning, and reading.
- **Create Shortcuts:** Build iPhone Shortcuts to trigger the Slack status update script when activating a specific Focus mode.
- **Run the Script:** The script will receive a GET request with the valid token and update your Slack status based on the predefined conditions.