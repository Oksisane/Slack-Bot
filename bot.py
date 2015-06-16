from slacker import Slacker
from glob import glob
import time
import importlib
import os

API_KEY=''
NAME='Bot Ehsan'
chanids = []
slack = Slacker(API_KEY)
hooks = {}
#setup channels
def setup_channel():
    for channel in slack.channels.list().body['channels']:
        if not channel['is_archived']:
            chanids.append(channel['id'])
def setup_channel_debug():
    chanids.append('C03HL6YRL')
def setup_hooks():
    plugindir = "plugins"
    for plugin in glob(os.path.join(plugindir, "[!_]*.py")):
        try:
            mod = importlib.import_module(plugindir + '.' + os.path.basename(plugin)[:-3])
            modname = mod.__name__
            print "Loaded: " + modname
            reponse_def = getattr(mod, "on_message")
            hooks.setdefault("on_message", []).append(reponse_def)
        except:
           print "Error"
def run_hooks(newmessage):
    response = ""
    for hook in hooks["on_message"]:
        try:
            temp = hook(newmessage)
            print temp
            if temp and isinstance(temp, basestring) and temp != None:
                response = response + temp
        except Exception,e:
            return str(e)
    return response
def main():
    #setup_channel()
    setup_channel_debug()
    setup_hooks()
    slack.rtm.start()
    latestpost = {}
    while True:
        for id in chanids:
            messagesub = None
            try:
                messagesub = slack.channels.history(id,None,None,1).body['messages'][0]['subtype']
            except:
                pass
            if latestpost.get(id) != slack.channels.history(id,None,None,1).body and (not messagesub or messagesub != "bot_message"):
                newmessage = slack.channels.history(id,None,None,1).body
                latestpost[id] = newmessage
                out = run_hooks(newmessage['messages'][0]['text']) + " "
                if len(out) > 1:
                    slack.chat.post_message(id,out,NAME)
        time.sleep(.25)
if __name__ == "__main__":
    main()
