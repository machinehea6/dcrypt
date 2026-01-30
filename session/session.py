from chat import chat
from chat import render
from chat import messages
from session import setup
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
        self.last_message_seen = ''
        self.setup_tool = setup.SetupUtils()

    def start_session(self):
        if self._confirm_connection():
            pass
        else:
            sys.exit()

        backlog = self.chat.get_messages('',10,True)
        self.artist.print_messages(backlog)
        self.last_message_seen = backlog[0].msg_id

        main_thread = threading.Thread(name='update_chat', target=self._update_chat, daemon=True)

        main_thread.start()

        while True:
            self._take_input()
            time.sleep(.1)

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

    def _update_chat(self):
        while True:
            if self.is_updating:
                pass
            else:
                self.is_updating = True
                new_batch = self.chat.get_messages(self.last_message_seen,10, False,self.recipient.disc_id)
                if new_batch:
                    self.artist.print_messages(new_batch)
                    self.last_message_seen = new_batch[0].msg_id
                    print(">  ")
                    self.is_updating = False
                    time.sleep(.3)
                else:
                    self.is_updating = False
                    time.sleep(.3)


    #no suspicion here
    def _take_input(self):
        global is_updating
        global last_message_seen

        text = input(">  ")
        if text:
            new_message = chat.OutMessage(text, self.recipient.pub_key)
            while True:
                if  self.is_updating:
                    pass
                else:
                    break
            self.is_updating = True
            new_batch = self.chat.get_messages(self.last_message_seen,10, False,self.recipient.disc_id)
            if new_batch:
                self.artist.print_messages(new_batch)
                self.last_message_seen = new_batch[0].msg_id
                self.chat.send_message(new_message)
                print(f"{self.artist._pad_name(self.client.username)} [{new_message.is_encrypted}]: {text}\n")
                print(">  ")
                self.is_updating = False
            else:
                self.chat.send_message(new_message)
                print(f"{self.artist._pad_name(self.client.username)} [{new_message.is_encrypted}]: {text}\n")
                print(">  ")                    
                self.is_updating = False

        

