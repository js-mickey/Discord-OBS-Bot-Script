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

# WSS Connection Behavior
boot_sock = bool(PREFS["open_WSS_at_run"])
maintain_sock = bool(PREFS["maintain_WSS"])

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

def close_OBS_Connection():
    global WSSINIT
    WSS_OBS.disconnect()
    WSSINIT = False
    return WSS_OBS

def activate_OBS_Scene(scene):
    global WSS_OBS
    if WSSINIT == False:
        WSS_OBS = start_OBS_Connection()
    WSS_OBS.call(requests.SetCurrentProgramScene(sceneName=scene))

def activate_OBS_Source(scene, source, visibility, reset):
    global WSS_OBS
    if WSSINIT == False:
        WSS_OBS = start_OBS_Connection()
    # Call the scene and set item status
    if visibility == "toggle":
        visibility = not GetItemStatus(source)

    # If Reset is true, test status and toggle
    if reset:
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

def TestPermissions(message, min_role_name):
    #Return True if no defined role
    if min_role_name == False:
        return True

    # Find minimum role in Discord Guild
    min_role = discord.utils.get(message.guild.roles, name=min_role_name)
    if min_role == None:
        return False
    
    # Get user's max role
    user_role = message.author.roles[-1]

    # Test role against permission
    if user_role  >= min_role:
        return True
    else:
        return False
    
## Listen for Discord Events
@client.event
async def on_message(message):
    #Prevent bot self-reply
    if message.author == client.user:
        return
    
    #Get first message key
    TEXT = message.content.split(" ")[0]

    # Check if key exists in command list, proceed if so.
    MYCOMMAND = KEYS.get(TEXT, False)
    if MYCOMMAND != False: 
        # Test Permissions
        PERMITTED = TestPermissions(message, MYCOMMAND.get("min_user_role", False))
        if not PERMITTED:
            return
        
        #Load dictionary commands
        MESSAGE = MYCOMMAND.get("message", False)
        COMMAND = COMMAND_DICT.get(MYCOMMAND.get("command", "activate"), True)
        SCENE = MYCOMMAND.get("scene")
        SOURCE = MYCOMMAND.get("id", False)
        RESET = MYCOMMAND.get("reset", False)

        # Send Discord reply, if one is defined.
        if MESSAGE:
            await message.channel.send(MESSAGE)

        # Determine whether it is a Scene or Source command.
        if not SOURCE:
            activate_OBS_Scene(SCENE)
        else:
            activate_OBS_Source(SCENE, SOURCE, COMMAND, RESET)
        
        #If set to disconnect, disconnect.    
        if not maintain_sock:
            close_OBS_Connection()

if boot_sock:
    WSS_OBS = start_OBS_Connection() 
client.run(key)

