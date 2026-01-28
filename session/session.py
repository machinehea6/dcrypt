from chat import chat
from chat import render
import threading
import time 

class Session():
    def __init__(self, chat:chat.chat.Chat):
        self.curr_chat = chat
        self.client = self.curr_chat.client
        self.recipient = self.curr_chat.recipient
        self.artist = render.Artist()
        self.first_message_id = self.curr_chat.get_messages('',1,True,'')[0].msg_id 
        self.backlog = self.curr_chat.get_messages('',10, True,'')
        self.artist.print_messages(self.backlog)
        
    def main_loop(self):
        main_thread = threading.Thread(name='update_chat',
                                        target=self.query, daemon=True, 
                                        kwargs={'first_message_id':self.first_message_id})
        main_thread.start()

        while True:
            self._take_input()

    def _take_input(self):
        new_message = chat.Message('','',input("> "))
        if new_message:
            self.curr_chat.send_message(new_message)

    def query(self, first_message_id):
        ls_message_id = first_message_id
        while True:
            chat = self.curr_chat
            artist = render.Artist()

            last_messages = self.curr_chat.get_messages(ls_message_id, 5, False, self.curr_chat.recipient.disc_id)
            if last_messages:
                artist.print_messages(last_messages)
                ls_message_id = last_messages[0].msg_id
                print("> ")
            time.sleep(1.0)