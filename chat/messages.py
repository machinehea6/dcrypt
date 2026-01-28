from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from definitions import *
import members
class Message:
    """
    Class to store messages retrieved from chats.

    Attributes:
        msg_id (str): The message id of the message.
        author (str): The username of the author of the message.
        message_body (str): A string containing the text content of the message.

    """
    def  __init__(self):
        """
        Initializes an empty Message.

        Parameters:
            msg_id (str): The message id of the message.
            author (str): The username of the author of the message.
            message_body (str): A string containing the text content of the message.

        """
    def _is_encrypted(self):
        header = ''
        msg = "".join([''+x for x in reversed(self.message_body)])
        try:
            for char in range(4):
                header = header + msg[char]
        except IndexError:
            return False
        if header == "CNE-":
            return True
        else:
            return False
    

    def encrypt(self):
        return

class OutMessage(Message):
    """
    Class to create an outbound message.

    Attributes:
        message_body (str): the body of the message to send 
        to_encrypt (bool): whether the message body will be encrypted before sending, defaults to true
        public_key (Recipeint.pub_key): public key for encryption 
    """
    def __init__(self, raw_msg:str, public_key: members.Recipient.pub_key):
        self.raw_msg = raw_msg
        self.pub_key = public_key
        
        self.message_body = self._process_message()

    def _process_message(self):
        if self._should_encrypt():
            return self._encrypt()
        else:
            return self.raw_msg

    def _should_encrypt(self):
        header = ''
        msg = "".join([''+x for x in reversed(self.raw_msg)])
        try:
            for char in range(4):
                header = header + msg[char]
        except IndexError:
            return True
        if header == "NLP-":
            return False
        else:
            return True
    
    def _encrypt(self):
        cipher_rsa = PKCS1_OAEP.new(self.pub_key)
        byte_msg = self.raw_msg.encode("utf-8")
        encrypted_msg = cipher_rsa.encrypt(byte_msg)
        return encrypted_msg

class InMessage(Message):
    def __init__(self, message_body:str, private_key: members.Client.priv_key):
        self.private_key = private_key
    def _decrypt():

        return
    
    def _get_private_key():
        return
    