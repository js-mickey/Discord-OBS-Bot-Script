# Discord-OBS Bot Interface

This is a simple python script to interface a discord chat bot with OBS via a local websocket (WSS). It can control scenes and sources, test user roles, activate or deactivate sources, and send Discord messages.

## Caveats

This script is meant for use with a small, private Discord group.

This script is meant to run locally. **Any security is your responsibility.**

## Use Cases

The bot monitors Discord chat and changes source activation based on the first word in messages.

Uses can include:

- Let RPG players roll dice by activating a Browser scene with [dice.bee.ac](http://dice.bee.ac)! 
- Let viewers toggle information like the currently playing song.
- Let a streamer switch scenes straight from Discord.

This script is intended to run locally in a terminal. Essentially, OBS websocket will never touch the internet. There's no reason you couldn't extend this to run on a server if you wanted to set that all up.

## Setup

### Requirements

Requires Python and the [discordpy](https://discordpy.readthedocs.io/en/stable/index.html) and [obs-web-socket-py](https://github.com/Elektordi/obs-websocket-py) python libraries.

Bring your own [Discord Bot](https://discordpy.readthedocs.io/en/stable/discord.html#discord-intro) and invite it into a server with text chat.

The Discord bot requires message read and write permissions ***(a.k.a. Message Content Intent)***.

### Connect to OBS and Discord

Add OBS WSS info and Discord bot key to **settings.json**. This information should remain SECURE.

#### Add Triggers

Add any text commands you want to monitor to **triggers.json**.

**Required Parameters**
- **key**: The text that will trigger a command (one word).
- **scene**: The scene name to control.

**Source Control Parameters**
These are required to control Sources. Remove them to switch scenes instead.
- **id**: The ItemID for the source you want to control (see below).
- **command**: Choose one of three options:
    - activate (turn on)
    - deactivate (turn off)
    - toggle (switch state)
    ***Defaults to "Activate" if left blank.***

**Optional Parameters**
- **reset**: If True, the script will toggle the source before activation. (Adds a slight delay to activation)
- **min_user_role**: The name (in text) of the minimum user roll permitted to perform this action. If blank, defaults to all users.
- **message**: If you want the bot to state a message, add it here. Leave blank for no message.

#### Run

Make sure your bot is in Discord and you have OBS up with WSS enabled.

Run ***obs_discord_bot.py*** in terminal.

```bash
python3 obs_discord_bot.py
```

## More Help

### How to Find Item IDs

Run the script. Once it establishes a WSS connection, you'll begin to get OBS debug updates in the terminal.

Click the source you want to control.

Then, look in the debug messages for sceneItemID.

```python
DEBUG:obswebsocket.core:Got event: {'d': {'eventData': {'sceneItemId': <<THIS ONE>>, 'sceneName': '...', 'sceneUuid': '...'}, 'eventIntent': ..., 'eventType': 'SceneItemSelected'}, 'op': ...}
```

### Example Triggers

#### Anyone Sends a Pie

This trigger activates a Source when anyone types "/pie" in Discord chat.

```json
{
    "/pie": {
        "scene": "Scene",
        "id": 42,
        "command": "activate"
    }
}
```

#### Admin Switches Scenes

This trigger switches to "New_Scene" when a "Server Admin" or higher types "/switch" in Discord chat.

```json
{
    "/switch": {
        "scene": "New_Scene"
    }
}
```

## Advanced Settings

**settings.json** includes these other settings.

- **open_WSS_at_run**: If true, boots WSS on script boot. If false, WSS connects when first command runs. ***Default: True***
- **maintain_WSS**: If true, keeps WSS connected. If false, WSS disconnects after each command (may increase latency). ***Default: True***

## Disclaimers

This script is provided completely without license, warranty, or guarantee. You are solely responsible for reviewing and understanding any software or code downloaded or run on any machine or service that you control.
