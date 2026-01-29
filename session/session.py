from chat import chat
from chat import render
from chat import messages
import threading
import time 
from getpass import getpass

class Session():
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
    
    

