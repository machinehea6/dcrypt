from chat import chat
from chat import render
from chat import messages
import threading
import time 
from getpass import getpass

class Session():
    """
    Class to create and manage a new chat session.

    Attributes:
        chat (chat.Chat): the chat object the session will manage.
        client (chat.Client): the client of the chat session
        recipient (chat.Recipient): the recipient of the chat session
        artist (render.Artist): the artist which will render all chat messages
        backlog (list[Message]): the last ten messages sent in the chat prior to start

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
        self.backlog = chat.get_messages('',10,True)
        self.artist.print_messages(self.backlog)

    def start_session(self):
        if self.chat.ping == True:
            print("Connection successful")
        else:
            api_key = (f"Connection failed, input new api key: ")

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


    def _update_chat(self):
        chat = self.chat
        last_message_id = chat.fetch_latest()
        artist = render.Artist()
        while True:
            while True:
                if chat.fetch_latest(last_message_id):
                    break
                else:
                    time.sleep(1.0)
            messages = self.chat.get_messages(last_message_id,5,False,self.recipient.disc_id)
            artist.print_messages(messages)
            last_message_id = messages[-1].msg_id

            time.sleep(1.0)
    
    

