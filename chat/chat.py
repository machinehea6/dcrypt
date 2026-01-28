# standard library modules
import requests
import json 
import sys
from dotenv import load_dotenv, dotenv_values
#external modules
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# local modules
from definitions import *
load_dotenv()

class Client():
    """
    Class to store client configuration data.

    Attributes:
        pub_key (str): client's public key
        priv_key (str): client's private key
        api_key (str): client's api key
    """

    def __init__(self):
        """
        Method to create an empty Client object

        Parameters: 
            None
        
        Returns:
            None
        
        """
        keys = self._get_keys()
        self.priv_key, self.pub_key = self._get_keys()
        
        self.api_key = os.getenv('api_key')

    def _get_keys(self):
        """
        Private method to retrieve credentials

        Parameters:
            None
        
        Returns:
            credentials (dict[str]): returns public key, private key, and api key.
        """
        try:
            with open(f"{ROOT_DIR}/data/secrets/priv_key.pem", "rb") as f:
                data = f.read()
                priv_key = RSA.import_key(data)
        except Exception as err:
            print("There was a problem retrieving client private key.\n")
            print("Make sure you have a private key file at /data/secrets/priv_key.pem.\n")
            print(f"Error: {err}")
            sys.exit()
        try:
            with open(f"{ROOT_DIR}/data/secrets/pub_key.pem", "rb") as f:
                data = f.read()
                pub_key = RSA.import_key(data)
        except Exception as err:
            print("There was a problem retrieving client public key.\n")
            print("Make sure you have a private key file at /data/secrets/pub_key.pem.\n")
            print(f"Error: {err}")
            sys.exit()

        return priv_key, pub_key

    def _gen_keys(self):
        priv_key = RSA.generate(3072)
        pub_key = priv_key.public_key()
        pwd = b'secret'
        with open(f"{ROOT_DIR}/data/secrets/priv_key.pem", "wb") as f:
            data = priv_key.export_key()
            f.write(data)
        with open(f"{ROOT_DIR}/data/secrets/pub_key.pem", "wb") as f:
            data = pub_key.export_key()
            f.write(data)


class Recipient():
    """
    Class to store recipient configuration data

    Attributes: 
        disc_id (str): the discord id of the recipient
        pub_key (str): the public key of the recipient
        channel_id (str): the channel id of the recipient
        nickname (str): the nickname of the recipient
    """
    def __init__(self, nickname:str):
        """
        Method to initialize an empty Recipient object

        Parameters:
            disc_id (str): discord id of recipient
            pub_key (str): public key of recipient
            channel_id (str): channel id of recipient
        
        Returns:
            None
        """
        
        self.nickname = nickname
        config_info = self._get_info()
        self.disc_id = config_info['disc_id']
        self.channel_id =config_info['channel_id']
        self.pub_key = self._get_pub_key()

    def _get_info(self)->dict:
        """
        Private method to retrieve the recipient discord id and channel id.

        Parameters:
            None
        
        Return:
            config data (dict): a dictionary containing channel id and discord id

        """
        
        with open(f"{ROOT_DIR}/data/{self.nickname}/channel.conf","r") as file:
            data = json.load(file)
            return data

    def _get_pub_key(self):
        """
        Private method to retrieve the recipient public key. 

        Parameters:
            None
        
        Return:
            public_key (RSA public key): the recipient rsa public key

        """

        try:
            with open(f"{ROOT_DIR}/data/{self.nickname}/pub_key.pem", "rb") as f:
                data = f.read()
                return RSA.import_key(data)
        except Exception as err:
            print("There was a problem retrieving recipient public key.\n")
            print(f"Make sure you have a public key file at {ROOT_DIR}/data/{self.nickname}/pub_key.pem.\n")
            print(f"Error: {err}")
            sys.exit()



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
    def __init__(self, raw_msg:str, public_key: Recipient.pub_key):
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
    def __init__(self, message_body:str, private_key: Client.priv_key):
        self.private_key = private_key
    def _decrypt():

        return
    
    def _get_private_key():
        return
    
class Chat:
    """
    A Superclass to create and manage chat sessions.

    Attributes:
        client (Client): a client
        nickname (str): nickname of the chat instance
    """

    def __init__(self, nickname:str):
        """
        Creates a new empty Chat object.

        Parameters:
            nickname (str): the nickname of the chat

        Attributes: 
            recipient (Recipient): a recipient object
            client (Client): a client object
        """
        self.nickname = nickname
        self.recipient = Recipient(self.nickname)
        self.client = Client()


    def send_message(self, message:Message):
        """
        Method to send a message to a channel.

        Parameters:
           message (Message): A Message object.
        
        Returns:
            None
        """

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Authorization': self.client.api_key
        }

        json_data = {
            'content':message.message_body
        }

        response = requests.post(f"https://discord.com/api/v10/channels/{self.recipient.channel_id}/messages", headers=headers, json=json_data)
        if response.status_code == 200:
            print("Message sent...")
            print("> ")
        else:
            print(f"Error sending message...Code {response.status_code}")
            sys.exit()

    def get_messages(self,last_message_id:str=None, number_of_messages:int=1, both_authors:bool=True, author_id:str='') -> list[dict]:
        """
        Method to get messages from a chat.

        Parameters:
            last_message_id (str): The message id of the message longest ago that the query will start at. If left blank, 
                the query will deliver messages starting from the present.
            
            number_of_messges (int): Specifies the number of results to return. This has a minimum value of one, and a maximum of one hundred.

            both_authors (bool): A truthy value means that the function will return all messages which meet the previous criteria.
                A false one will only return messages from a specific author.
                
            author_id (str): If the both_authors parameter is false, this parameter accepts the discord user id of the person you want to see messages
                from
            
        Returns: 
            List of Message objects.
                
        Attributes:
            'msg_id': <message id of the message>
            'author': <username of the author>
            'message_body': <text content of the message>
                

            """

        headers = {'authorization': self.client.api_key}
        base_url = 'https://discord.com/api/v10/channels/'
        endpoint = f'{self.recipient.channel_id}/messages'
        full_url = f'{base_url}{endpoint}?limit={number_of_messages}'
        if last_message_id:
            full_url += f"&after={last_message_id}"
        try:
            response = requests.get(full_url, headers = headers)
                
            response.raise_for_status()
                
        except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error has occurred: {http_err}")
                sys.exit()

        except Exception as err: 
                print(f"Other error occurred: {err}")
                sys.exit()

        if both_authors:
            return [Message(content['id'], content['author']['username'],content['content'])\
                for content in response.json()]
        else: 
            return [Message(content['id'], content['author']['username'],content['content'])\
                    for content in response.json() if content['author']['id'] == self.recipient.disc_id]


class NewChat(Chat):
        """
        Class to create and manage a chat with a new recipient

        Attributes:
            client (Client): A client object
            recipient (Recipient): A recipient object
            nickname (str): nickname of the chat instance
        """

        def __init__(self, nickname:str):
            """
            Method to initialize an empty NewChat object.

            Parameters:
                nickname (str): the nickname of the chat to be used 

            """

            self.nickname = nickname
            print(self.nickname)
            self._setup()
            self.recipient = Recipient(self.nickname)
            self.client = Client()

        def _get_init_data(self) -> dict:
            """
            Method to prompt user for details about recipient.

            Parameters:
                None
            
            Return: 
                returns (dict): 'disc_id' and 'channel_id' for the new recipient
            """

            returns  = {
                'disc_id': 'discord id ',
                'channel_id': 'channel id '
            }
            
            for query in returns.keys():
                returns[query] = input((f"Please input {returns[query]}: "))
            
            return returns

        def _setup(self)-> None:
            """
            Method to create a configuration and chat status file under the data directory.

            Parameters:
                None
            
            Returns:
                None
            """
            file_path = f"{ROOT_DIR}/data/{self.nickname}/"
            try:
                os.mkdir(file_path)
            except FileExistsError:
                print("Data directory already exists. ")
                cont = input("Continue? y/n")
                if cont == 'y':
                    pass
                else:
                    sys.exit()

            except PermissionError:
                print("Insufficient permissions to write in data directory")
                sys.exit()

            data = self._get_init_data()

            try:
                with open(f"{file_path}channel.conf", "w") as conf_file:
                    conf_file.write(json.dumps(data))

            except PermissionError:
                print(f"Insufficient permissions to open {file_path}")
                sys.exit()
            except Exception as err:
                print(f"Error: {err}")
            print(f"Configuration file created for {self.nickname}\n")

            status_tracker = json.dumps({'ids':[]})
            try:
                with open(f"{file_path}chat_status", "w") as conf_file:
                    conf_file.write(status_tracker)
            except PermissionError:
                print(f"Insufficient permissions to open {file_path}")
                sys.exit()
            except Exception as err:
                print(f"Error: {err}")
            print(f"Status tracker created for {self.nickname}\n")

class ExisChat(Chat):
        """
        Class to create and manage a chat with an existing recipient

        Attributes:
            recipient (Recipient): A recipient object
            client (Client): A client object
            nickname (str): nickname of the chat instance

        """

        def __init__(self, nickname:str):
            """
            Method to initialize an empty ExistChat object.

            Parameters:
                nickname (str): the nickname of the chat to be used 
                
            """

            super().__init__(nickname)

