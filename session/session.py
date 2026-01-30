from chat import chat
from chat import render
from chat import messages
import setup
import threading
import time 

class Session():
    """
    Class to create and manage a new chat session.

    Attributes:
        chat (chat.Chat): the chat object the session will manage.
        client (chat.Client): the client of the chat session
        recipient (chat.Recipient): the recipient of the chat session
        artist (render.Artist): the artist which will render all chat messages
        is_updating (bool): Variable to prevent race conditions across async.

    Private Methods:
        _main_loop():
            Creates a thread to check for new messages and begins a loop which takes user input.__annotations__

        _take_input():
            Prompts the user for input, if it finds it, sends it as a message to the chat.

        _update_chat():
            Checks for messages by the recipient newer than what it has seen. If it finds one, prints out up to ten of their messages.
    
    Public Methods():
        start_session():
            Begins a new chat session. Checks for connection, checks for older messages, and starts the main loop.

    """
    
    def __init__(self, chat:chat.Chat):
        self.chat = chat
        self.client = self.chat.client
        self.recipient = self.chat.recipient
        self.artist = render.Artist()
        self.is_updating = False
        self.setup_tool = setup.SetupUtils()

    def start_session(self):
        if self._confirm_connection():
            pass
        else:
            sys.exit()


    def _confirm_connection(self):
        if self.chat.ping:
            print("Connection successful.")
        else:
            if setup_tool.set_api_key():
                print("Trying again")
                pass
            else:
                sys.exit()

            if self.chat.ping():
                print("Connection successful.")
                return True
            else:
                print("Connection still unsuccessful. Check your config and network and try again.")
                return False
        return True

    def _main_loop(self):
        main_thread = threading.Thread(name='update_chat',
                                        target=self._update_chat, daemon=True,)
        main_thread.start()

        while True:
            self._take_input()

    #no suspicion here
    def _take_input(self):
        text = input(">  ")
        if text:
            new_message = chat.OutMessage(text, self.recipient.pub_key)
            self.chat.send_message(new_message)
            print(f"{self.artist._pad_name(self.client.username)} [{new_message.is_encrypted}]: {text}\n")


    

