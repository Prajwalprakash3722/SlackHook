# SlackHook [WIP]

This is mainly a script to run on GET request from any component with a valid token to update slack status. Hint : Component being used is iPhone Shortcuts, can build and trigger shortcuts on specific time and so on the imaginations are endless.

PS: one of my usecase;

- I use iPhone focus modes heavily, I have multiple focus modes: for learning, working, reading, etc. There is also one I use for deep work. When doing deep work, I want to avoid being distracted by anything, and therefore I mute almost every app, including Slack.

at the end of the day, it's just a overengineered product :)

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

![automation](https://www.milner.com/images/default-source/articles/buzz.png?sfvrsn=e0080dd3_2)