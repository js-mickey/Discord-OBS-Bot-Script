import discord
import logging
import json
import time
from obswebsocket import obsws, events, requests

logging.basicConfig(level=logging.DEBUG)

# Load preferences and action triggers
PREF_FILE = open('settings.json', 'r').read()
KEY_FILE = open('triggers.json', 'r').read()
PREFS = json.loads(PREF_FILE)
KEYS = json.loads(KEY_FILE)

# OBS WSS Info
host = PREFS["ip"]
port = PREFS["port"]
password = PREFS["password"]

# Discord bot key
key = PREFS["auth"]

# Definitions
COMMAND_DICT = {"activate": True, "deactivate": False, "toggle": "toggle"}
WSS_OBS = {}
WSSINIT = False

## Discord Definitions
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def start_OBS_Connection():
    global WSSINIT
    WSS_OBS = obsws(host, port, password)
    WSS_OBS.connect()
    WSSINIT = True
    return WSS_OBS

def activate_OBS_Source(scene, source, visibility, reset):
    global WSS_OBS
    if WSSINIT == False:
        WSS_OBS = start_OBS_Connection()
    # Call the scene and set item status
    if visibility == "toggle":
        visibility = not GetItemStatus(source)

    # If Reset is true, test status and toggle
    if reset == "True":
        ResetItemStatus(scene, source, visibility)

    WSS_OBS.call(requests.SetSceneItemEnabled(sceneName=scene, sceneItemId=source, sceneItemEnabled=visibility))

def ResetItemStatus(scene, source, visibility):
    CURRSTATE = GetItemStatus(source)
    if CURRSTATE == visibility:
        WSS_OBS.call(requests.SetSceneItemEnabled(sceneName=scene, sceneItemId=source, sceneItemEnabled=not visibility))
        time.sleep(1)

def GetItemStatus(source):
    # Get the item status as a dictionary
    CALLRETURN = WSS_OBS.call(requests.GetSceneItemEnabled(sceneName="Scene", sceneItemId=source)).__dict__
    # Item true/false is a dictionary in a dictionary
    ITEMSTATUS = CALLRETURN.get("datain").get("sceneItemEnabled")
    return ITEMSTATUS

## Listen for Discord Events
@client.event
async def on_message(message):
    TEXT = message.content.split(" ")[0]
    MYCOMMAND = KEYS.get(TEXT, False)
    if MYCOMMAND != False: 
        await message.channel.send(MYCOMMAND.get("message"))
        COMMAND = COMMAND_DICT.get(MYCOMMAND.get("command", "activate"), True)
        SCENE = MYCOMMAND.get("scene")
        SOURCE = MYCOMMAND.get("id")
        RESET = MYCOMMAND.get("reset")
        print(SCENE, SOURCE, COMMAND, RESET)
        activate_OBS_Source(SCENE, SOURCE, COMMAND, RESET)

client.run(key)
