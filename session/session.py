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
        setup_tool (setup.SetupUtils): Object to manage altering credentials and configuration files.
        last_message_seen (str): Stores the id of the last message retrieved from the chat

    Private Methods:
        _confirm_connection(self):
            Checks the connection to the chat, tries to resolve api related failures, returns bool. True if successful connection, else False.
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
        """
        Public method to start a new chat session.

        Confirms connection, get's backlogged messages, prints backlog, sets the earliest message, 
        then starts the main thread and checks for input. If it can't make a connection calls sys.exit().

        Parameters:
            None
        
        Returns:
            None
        """

        # confirms connection with chat
        if self._confirm_connection():
            pass
        else:
            sys.exit()

        # gets the last ten messages from the chat and prints them
        backlog = self.chat.get_messages('',10,True)
        self.artist.print_messages(backlog)

        # sets the last message seen to the most recent message
        self.last_message_seen = backlog[0].msg_id

        # creates and starts a new thread to look for new messages in the chat
        main_thread = threading.Thread(name='update_chat', target=self._update_chat, daemon=True)

        main_thread.start()

        # loops waiting for user input
        while True:
            self._take_input()
            time.sleep(.1)

    def _confirm_connection(self):
        """
        Private method to confirm connection with chat.

        Parameters:
            None
        
        Returns: 
            succesful (bool): True if status 200, else False
        
        """

        if self.chat.ping:
            print("Connection successful.")
        else:
            # If there's a failure to connect, prompts the user for a new api key
            if setup_tool.set_api_key():
                print("Trying again")
                pass
            else:
                sys.exit()

            # Retries the connection with the new api key
            if self.chat.ping():
                print("Connection successful.")
                return True
            else:
                print("Connection still unsuccessful. Check your config and network and try again.")
                return False
        return True

    def _update_chat(self):
        """
        Private method to check for new messages in the chat

        Parameters:
            None
        
        Returns:
            None
        """

        while True:
            # Checks to see if another process is updating the chat
            if self.is_updating:
                pass
            else:
                # Sets the updating status to true to prevent duplicate message retrieval and race conditions
                self.is_updating = True

                # Queries the chat for up to ten new messages from the recipient
                new_batch = self.chat.get_messages(self.last_message_seen,10, False,self.recipient.disc_id)
                if new_batch:
                    # Prints messages from new batch
                    self.artist.print_messages(new_batch)
                    # Updates the last message seen to the most recent message id
                    self.last_message_seen = new_batch[0].msg_id

                    # Allows other process to update the chat
                    self.is_updating = False
                    time.sleep(.3)
                else:
                    # Allows other process to update the chat
                    self.is_updating = False
                    time.sleep(.3)

    def _take_input(self):
        """
        Private method to handle user input to the chat

        Parameters:
            None
        
        Returns:
            None
        """

        text = input(">  ")
        if text:
            # Stores the user input in a new outgoing chat message
            new_message = chat.OutMessage(text, self.recipient.pub_key)
            while True:
                # Checks if another process is updating the chat
                if  self.is_updating:
                    pass
                else:
                    break
            
            # Blocks other process from updating the chat 
            self.is_updating = True

            # Checks for new messages from the recipient 
            new_batch = self.chat.get_messages(self.last_message_seen,10, False,self.recipient.disc_id)
            if new_batch:
                # If there are new messages prints them to the screen
                self.artist.print_messages(new_batch)

                # Sets last message seen id to most recent message
                self.last_message_seen = new_batch[0].msg_id

                # Sends the input from the client
                self.chat.send_message(new_message)

                # Prints the client's input in the standard format
                print(f"{self.artist._pad_name(self.client.username)} [{new_message.is_encrypted}]: {text}\n")
                print(">  ")

                # Unblocks other processes from updating the chat
                self.is_updating = False
            else:
                # If no new messages, sends and prints the client message
                self.chat.send_message(new_message)
                print(f"{self.artist._pad_name(self.client.username)} [{new_message.is_encrypted}]: {text}\n")
                print(">  ")        
                # Unblocks other processes from updating the chat            
                self.is_updating = False

        

