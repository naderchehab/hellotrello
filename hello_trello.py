# Your key for the Google Speech API which is used to transcribe your speech to text. See this for more info: https://developers.google.com/api-client-library/python/guide/aaa_apikeys
GOOGLE_SPEECH_API_KEY = ""

# Your key for the Trello API: https://trello.com/app-key
TRELLO_API_KEY = ""

# You also need a Trello API token. You can get the token URL by running this function:
#tokenUrl = trello.get_token_url('Hello Trello', expires='30days', write_access=True)
# Once you have a URL, paste it in your browser and approve. It will return a token for you.
TRELLO_API_TOKEN = ""

# This is the ID of the Trello list where you want your card to be added. To get it, follow these steps:
# 1. Use this URL to retrieve the Board ID where your list is located. Replace <your_username>, <your_trello_api_key> and <your_trello_token> with the values you got above.
# https://api.trello.com/1/members/<your_username>/boards?key=<your_trello_api_key>&token=<your_trello_token>
# 2. Use this function to get all the lists from your board, the ID is included there:
# lists = trello.boards.get_list('<your_board_ID>')
TRELLO_LIST_ID = ""

# This is the command that will make the computer prepare to send a note to Trello. Anything you say after this command will be sent to Trello.
INIT_COMMAND = "add to trello"


import speech_recognition as sr
from trello import TrelloApi
r = sr.Recognizer(key = GOOGLE_SPEECH_API_KEY)
r.pause_threshold = 0.5

from dragonfly.all import Grammar, CompoundRule
import pythoncom
import time

# Voice command rule combining spoken form and recognition processing.
class ExampleRule(CompoundRule):
    spec = INIT_COMMAND                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
		# use the default microphone as the audio source
		with sr.Microphone() as source:
			# listen for the first phrase and extract it into audio data
			audio = r.listen(source)

		try:
			# recognize speech using Google Speech Recognition then send to Trello
			text = r.recognize(audio)
			print(text)
			trello = TrelloApi(apikey=TRELLO_API_KEY, token=TRELLO_API_TOKEN)
			a = trello.lists.new_card(TRELLO_LIST_ID, text, '')
		except LookupError:
			print("Could not understand audio")

			
# Create a grammar which contains and loads the command rule.
grammar = Grammar("example grammar")                # Create a grammar to contain the command rule.
grammar.add_rule(ExampleRule())                     # Add the command rule to the grammar.
grammar.load()                                      # Load the grammar.

while True:
    pythoncom.PumpWaitingMessages()
    time.sleep(.1)

