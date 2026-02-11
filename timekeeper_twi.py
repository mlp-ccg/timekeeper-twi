import urllib
import urllib.request
import urllib.parse
import datetime
import json
import sys
import time
import traceback

# this is a script to help manage time limits for rounds in a tournament via a Discord server. it doesn't need anything
# outside of the Python standard library, and will make a settings file in the current directory which keeps track
# of the configuration for the servers you use it in.
#
# you'll need an admin from the server who can make webhooks and roles, and you are expected to know how to get role
# IDs from the server. for each server, you can pick a different name for each server via the variable below
# 
# the first time you run the script for a server, it will help you do setup and send the test message by default
# you should uncomment the appropriate function afterwards and then you can just run the script to start

serverName = "onlinecon"
def main():
    # uncomment whichever kind of clock you want and comment everything else
    
    #onlineBuildClock() # ~25 minutes to build a limited deck
    #onlineEliminationPlayClock() # 45 + 6.5 soft time minutes for tier 2ish rounds
    #onlineSwissPlayClock() # 35 + 5 soft time minutes for normal play

    # comment this once you know everything works
    sendTimekeeperTwiMessage("Booky book") # testing


environment = None
def ensureEnvironment():
    global environment
    needsSave = False
    webhooksFile = "timekeeper_webhook.json"
    
    try:
        with open(webhooksFile, "r", encoding="utf-8", newline='\n') as f:
            environments = json.loads(f.read())
    except FileNotFoundError:
        print("Missing webhooks, making a new file.")
        environments = dict()
        environments[serverName] = dict()
        needsSave = True
    except:
        print(f"Some other failure to load the webhooks, refusing to do anything. {traceback.format_exc()}")
        raise
    
    if not serverName in environments:
        print(f"Don't have '{serverName}' in environments. Adding a blank one.")
        environments[serverName] = dict()
    environment = environments[serverName]
    
    hasFields = "webHook" in environment and "judgeRole" in environment and "playerRole" in environment
    if not hasFields:
        print(f"Environment '{serverName}' does not have required settings. Configuring this for you...")
        print("Get a server admin to make a webhook for you and paste the URL:")
        webHook = input().strip()
        print("Paste your user id (or an &roleid) as the judge/TO (hint: 12345):")
        judgeRole = input().strip()
        if ("&" in judgeRole):
            print("\t NOTE: Judge role is actually a role; this will probably ping a lot of people.")
        print("Is this the MLP:CCG Discord server? (y/n)")
        if ("y" in input().strip()):
            print("Using @Participant role")
            playerRole = "&528704126234656778"
        else:
            print("Paste the role ID for players (hint: &24567837):")
            playerRole = "&" + input().strip().strip("&")
        environment["reminder"] = "Do NOT paste the contents of this file to anypony who is not an admin in the server. These are SECRETS."
        environment["webHook"] = webHook
        environment["judgeRole"] = judgeRole
        environment["playerRole"] = playerRole
        needsSave = True

    if needsSave:
        with open(webhooksFile, "w", encoding="utf-8", newline='\n') as f:
            f.write(json.dumps(environments, indent=4))
        print("Saved webhooks file")

def cheapTimeFormat(seconds):
    if (seconds < 0):
        return "{0:0>2}:{1:0>2} beyond".format(int(-seconds/60), int(-seconds % 60))
    return "{0:0>2}:{1:0>2} to".format(int(seconds/60), int(seconds % 60))

def onlineSwissPlayClock():
    events = [
        # {"name": "importer", "time": 51*60, "message": "3 minute pre-setup time for fighting with the importer.", "ping": False},
        {"name": "setup", "time": 48*60, "message": "Okay everypony! We've got three minutes to get everything set up."},
        {"name": "start", "time": 45*60, "message": "Three minutes have passed! Begin! Soft time <t:__ZERO_TIMESTAMP__:R>"},
        {"name": "warn1", "time": 10*60, "message": "Only ten minutes remain!"},
        {"name": "warn2", "time":  5*60, "message": "There's only five minutes left everypony!"},
        {"name": "soft", "time": 0, "message": "<@__JUDGE_ROLE__> And that's it! Finish your rounds. (Soft time: second player gets to _start_ another turn)"},
        {"name": "hard", "time": -6*60+30, "message": "Quills down and hoof in your papers everypony! (Hard time: stop playing and report with current scores)"},
    ]
    
    timerCore(events)

def onlineEliminationPlayClock():
    events = [
        {"name": "setup", "time": 68*60, "message": "Everyone seated? You have five minutes to review before the game. (Look at your opponent's deck list and *close the tab* afterwards)"},
        {"name": "setup", "time": 63*60, "message": "Okay everypony! We've got three minutes to get everything set up."},
        {"name": "start", "time": 60*60, "message": "Three minutes have passed! Begin! Soft time <t:__ZERO_TIMESTAMP__:R>"},
        {"name": "warn1", "time": 10*60, "message": "Only ten minutes remain!"},
        {"name": "warn2", "time":  5*60, "message": "There's only five minutes left everypony!"},
        {"name": "soft", "time": 0, "message": "<@__JUDGE_ROLE__> And that's it! Finish your rounds. (Soft time: second player gets to _start_ another turn)"},
        {"name": "hard", "time": -6*60+30, "message": "Quills down and hoof in your papers everypony! (Hard time: stop playing and report with current scores)"},
    ]
    
    timerCore(events)

def onlineBuildClock():
    events = [
        {"name": "setup", "time": 25*60, "message": "Okay everypony! Take your pools and begin. Building ends <t:__ZERO_TIMESTAMP__:R>"},
        {"name": "warn", "time":  5*60, "message": "Five minutes left everypony!"},
        {"name": "end", "time": 0, "message": "Building time is up! Time to take the test!"},
    ]
    
    timerCore(events)

def timerCore(events):
    minTime = events[-1]["time"]
    maxTime = events[0]["time"]
    eventIndex = 0
    startTime = time.time()
    zeroTime = startTime + maxTime
    
    print("Schedule of {0} events which will take {1} to complete.".format(len(events), cheapTimeFormat(maxTime-minTime)))

    while True:
        secondsElapsed = maxTime - (time.time() - startTime)
        currentEvent = events[eventIndex]
        if (currentEvent["time"] > secondsElapsed):
            eventIndex += 1
            ping = True
            message = currentEvent["message"]
            if "ping" in currentEvent:
                ping = currentEvent["ping"]
            print("Transition to {0} at {1}".format(currentEvent["name"], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            sendTimekeeperTwiMessage(message, ping, zeroTime)
        print("{0} soft time".format(cheapTimeFormat(secondsElapsed)), end="\r")
        time.sleep(1)
        
        if (eventIndex == len(events)):
            break
    
    print("No more events, exiting.")

def sendTimekeeperTwiMessage(message, pingParticipantRole = False, zeroTimestamp = None):
    webhook = environment["webHook"]
    discordMessage = ""
    
    if pingParticipantRole:
        discordMessage += "<@{0}> ".format(environment["playerRole"])
    
    discordMessage += message.replace("__JUDGE_ROLE__", environment["judgeRole"])
    
    if (zeroTimestamp != None):
        discordMessage = discordMessage.replace("__ZERO_TIMESTAMP__", str(int(zeroTimestamp)))
    
    content = json.dumps({"content": discordMessage})
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "test script (http://www.example.com, 0)",
    }
    
    request = urllib.request.Request(webhook, data = content.encode("utf-8"), headers = headers, method = "POST")
    response = urllib.request.urlopen(request,timeout=5).read().decode("utf-8")

if __name__ == "__main__":
    ensureEnvironment()
    main()
    print("Exiting. Press enter to close/continue.")
    input()
