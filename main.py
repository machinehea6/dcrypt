import requests
import json
import sys
import threading 
import time 
from chat.chat import Chat
from chat.artist import Artist
from chat.chat import Message 

#################
def query(first_message_id):
    ls_message_id = first_message_id
    while True:
        chat = Chat(channel_id, other_user_id)
        artist = Artist()

        last_messages = chat.get_messages(ls_message_id, 5, False, chat.other_user_id)
        if last_messages:
            artist.print_messages(last_messages)
            ls_message_id = last_messages[0].msg_id
            print("> ")
        time.sleep(1.0)
######################

"""
def main():
    chat = Chat(channel_id, other_user_id)
    artist = Artist()

    first_message_id:str = chat.get_messages('',1,True,'')[0].msg_id

    artist.print_messages(chat.get_messages('',10, True,''))
    
    main_thread = threading.Thread(name='update_chat',
                               target=query, daemon=True, kwargs={'first_message_id':first_message_id})
    main_thread.start()


    while True:
        new_message = Message('','',input("> "))
        if new_message:
            chat.send_message(new_message)

main()
"""

def main():
    #parse args 

    #if setup -> setup

    #if open -> open

    #if new ->
    return