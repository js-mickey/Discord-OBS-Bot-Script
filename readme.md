# Discord-OBS Bot Interface
This is a simple python script to interface a discord chat bot with OBS via a local websocket (WSS). Currently it can activate or deactivate sources.

## Caveats
This script is meant for use with a small, private Discord group. There's no role handling, so it shouldn't be deployed when there is the opportunity for public mischief.

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

### Connect to OBS and Discord
Add OBS WSS info and Discord bot key to **settings.json**. This information should remain SECURE.

### Add Triggers
Add any text commands you want to monitor to the triggers.json file.
- **key**: The text that will trigger a command (one word).
- **scene**: The scene name
- **id**: The ItemID for the source you want to control.
- **message**: If you want the bot to state a message, add it here.
- **command**: Choose one of three options:
    - activate (turn on)
    - deactivate (turn off) 
    - toggle (switch state)
- **reset**: If True, the script will toggle the source before activation. (Adds a slight delay to activation)

## Disclaimers
This script is provided completely without license, warranty, or guarantee. You are solely responsible for reviewing and understanding any software or code downloaded or run on any machine or service that you control.
