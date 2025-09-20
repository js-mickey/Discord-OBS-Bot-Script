# Discord-OBS Bot Interface

This is a simple python script to interface a discord chat bot with OBS via a local websocket (WSS). Currently it can test user roles, activate or deactivate sources, and send Discord messages.

## Caveats

This script is meant for use with a small, private Discord group.

This script is meant to run locally. **Any security is your responsibility.**

## Use Cases

The bot monitors Discord chat and changes scene activation based on the first word in messages.

Uses can include:

- Let RPG players roll dice by activating a Browser scene with [dice.bee.ac](http://dice.bee.ac)! 
- Let viewers toggle information like the currently playing song. 
- Anything else supported by OBS web socket. 

This script is intended to run locally in a terminal. Essentially, OBS websocket will never touch the internet. There's no reason you couldn't extend this to run on a server if you wanted to set that all up.

## Setup
You'll need the [discordpy](https://discordpy.readthedocs.io/en/stable/index.html) and [obs-web-socket-py](https://github.com/Elektordi/obs-websocket-py) python libraries.

You'll also need a [Discord bot](https://discordpy.readthedocs.io/en/stable/discord.html#discord-intro) in a text server.

The Discord bot requires message read and write permissions (Message Content Intent). Note that reading messages is a privileged intent.

### Connect to OBS and Discord

Add OBS WSS info and Discord bot key to **settings.json**. This information should remain SECURE.

### Add Triggers

Add any text commands you want to monitor to the triggers.json file.

**Required Parameters**
- **key**: The text that will trigger a command (one word).
- **scene**: The scene name
- **id**: The ItemID for the source you want to control (see below).
- **command**: Choose one of three options:
    - activate (turn on)
    - deactivate (turn off) 
    - toggle (switch state)

**Optional Parameters**
- **reset**: If True, the script will toggle the source before activation. (Adds a slight delay to activation)
- **min_user_role**: The name (in text) of the minimum user roll permitted to perform this action. If blank, defaults to all users.
- **message**: If you want the bot to state a message, add it here. Leave blank for no message.

### How to Find Item IDs

Run the script. Once it establishes a WSS connection, you'll begin to get OBS debug updates in the terminal.

Click the source you want to control.

Then, look in the debug messages for sceneItemID.

```
DEBUG:obswebsocket.core:Got event: {'d': {'eventData': {'sceneItemId': <<THIS ONE>>, 'sceneName': '...', 'sceneUuid': '...'}, 'eventIntent': ..., 'eventType': 'SceneItemSelected'}, 'op': ...}
```

### Settings.json

- **open_WSS_at_run**: If true, boots WSS on script boot. If false, WSS connects when first command runs.
- **maintain_WSS**: If true, keeps WSS connected. If false, WSS disconnects after each command. (May increase latency)

## Disclaimers

This script is provided completely without license, warranty, or guarantee. You are solely responsible for reviewing and understanding any software or code downloaded or run on any machine or service that you control.
