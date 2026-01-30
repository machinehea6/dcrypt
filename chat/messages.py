from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from definitions import *
import chat.members

class OutMessage():
    """
    Class to create an outbound message.

    Attributes:
        input_text (str): the raw message that will be processed
        output_text (str): the body of the message to send 
        to_encrypt (bool): whether the message body will be encrypted before sending, defaults to true
        public_key (Recipeint.pub_key): public key for encryption 
    
    Private Methods:
        _process_message():
            Determines whether the input message should be encrypted, if not, returns the string without the -PLN postfix.
        
        _should_encrypt():
            Determines whether the message has a -PLN postfix. If so, returns False and sets OutMessage.is_encrypted False, else returns True.

        _encrypt():
            Returns the encrypted version of the message body.
            
    """

    def __init__(self, input_text:str, public_key: members.Recipient.pub_key):
        """
        Method to construct an empty OutMessage

        Parameters:
            input_text (str): the body of the outbound message
            public_key (members.Recipient.pub_key): the public key of the recipient
            
        """

        self.input_text = input_text
        self.pub_key = public_key
        self.output_text = self._process_message()
        self.is_encrypted = True

    def _process_message(self):
        """
        Function to determine whether to encrypt the message.

        Returns: 
            plaintext message (str): returns the text of the input message without the -PLN postix
        """

        if self._should_encrypt():
            return self._encrypt()
        else:
            return self.input_text[:-4]

    def _should_encrypt(self):
        """
        Method to check for the -PLN postfix on an outbound message.

        Returns:
            bool: if the message has the -PLN postfix it returns false, else true
        """

        header = ''
        print(self.input_text)
        msg = "".join([''+x for x in reversed(self.input_text)])
        try:
            for char in range(4):
                header = header + msg[char]
        except IndexError:
            return True
        if header == "NLP-":
            return False
            self.is_encrypted = False
        else:
            return True
    
    def _encrypt(self):
        """
        Method to encrypt outbound messages.

        Returns: 
            encrypted message (str): a string of the message encoded with the recipient public key
        """
        cipher_rsa = PKCS1_OAEP.new(self.pub_key)
        byte_msg = self.input_text.encode("utf-8")
        encrypted_msg = cipher_rsa.encrypt(byte_msg)
        print(encrypted_msg)
        return str(encrypted_msg)

class InMessage():
    """
    Class to process incoming messages 

    Attributes:
        input_text (str): the text contained in the inbound message
        output_text (str): the text after processing
        author (str): the author of the message 
        is_encrypted (str): whether the message was encrypted on arrival
    
    Private Methods:
        _process_message():
            Parses incoming messages. Determines if they are encrypted, if not, sets InMessage.is_encrypted to False, then returns message body.
            Else, leaves InMessage.is_encrypted as True and returns decrypted message in utf-8 plaintext.
        
        _decrypt():
            Decrypts the message using the private key and returns the message in bytees.
        
        _byte_mark_remover():
            Removes the initial b' and trailing ' from bytes converted to a string and returns the clean string.
    
    Public Methods:
        None

    """

    def __init__(self, message_json:json, private_key: members.Client.priv_key):
        """
        Method to construct an empty InMessage

        Parameters:
            message_json (json): a single json from the discord api
            private_key (members.Client.priv_key): the private key of the client

        """
        self.is_encrypted = True
        self.priv_key = private_key
        self.input_text = message_json['content']
        self.output_text = self._process_message()
        self.author = message_json['author']['username']
        self.msg_id = message_json['id']
        self.author_id = message_json['author']['id'] 
    
    def _process_message(self):
        """
        Method to parse inbound messages.

        Will return a message in plaintext. If the message wasn't encrypted prior it will set the is_encrypted attribute to False

        Returns:
            output text (str): returns the output message either decrypted or, if plain input, plain
        """

        header = ''
        try:
            for char in range(2):
                header = header + self.input_text[char]
        except Exception as err:
            return '[EMPTY MESSAGE]'
        if header in ['b\'', 'b\"']:
            return self._byte_mark_remover(str(self._decrypt()))
        else:
            self.is_encrypted = False
            return self._byte_mark_remover(str(self.input_text.encode('utf=8')))

    def _decrypt(self)-> None:
        """
        Method to decrypt the inbound message

        Returns:
            output message (bytes): the output message encoded as bytes
        """

        rsa_cipher = PKCS1_OAEP.new(self.priv_key)
        message_as_bytes = eval(self.input_text)
        try:
            return rsa_cipher.decrypt(message_as_bytes)
        except ValueError:
            return '  [NO MATCHING KEY]  '
    
    def _byte_mark_remover(self, text:str):
        """
        Method to remove trailing quotation marks as well as the b to prefix bytes

        Returns:
            clean string (str): a string without the byte marks
        """
        return_string = ''
        no_bytes = [text[x] for x in range(2, len(text)-1)]
        for i in no_bytes:
            return_string = return_string + i
        return return_string

        
