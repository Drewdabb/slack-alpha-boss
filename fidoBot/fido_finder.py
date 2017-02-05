import os
import time
from slackclient import SlackClient
from pymongo import MongoClient

# Fido's ID as an environment variable
BOT_ID = os .environ.get("FIDO_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "what is "

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_FIDO_TOKEN'))
# instantiate Mongo client & DB variable
mongo_client = MongoClient()
db = mongo_client['test-database']



def gather_acronym(acro):
    """
        Gets the requested acronym from the user and determines if it
        exists in the DB. If it does, then it returns the context.
    """



def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    acronym = ""
    context = ""
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        # determine what acronym to search for
        acronym = command[len(EXAMPLE_COMMAND):-1]
        response = "Sure let me look for that for you.."
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)
    # reach out to the DB
    context = gather_acronym(acronym)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

def check_slack_connection():
     READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
     if slack_client.rtm_connect():
         print("Fido awake and alert!")
         while True:
             command, channel = parse_slack_output(slack_client.rtm_read())
             if command and channel:
                 handle_command(command, channel)
             time.sleep(READ_WEBSOCKET_DELAY)
     else:
         print("Connection failed. Invalid Slack token or bot ID?")
         return -1

def check_mongo_connection():
     pass

if __name__ == "__main__":
    print('hello')
    check_slack_connection()
    # check_mongo_connection == -1):
