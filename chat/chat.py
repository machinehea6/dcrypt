from dotenv import load_dotenv, dotenv_values
from definitions import *
import requests
import json 
import sys
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
        self.pub_key = keys['pub_key']
        self.priv_key = keys['priv_key']
        self.api_key = keys['api_key']

    def _get_keys(self):
        """
        Private method to retrieve credentials

        Parameters:
            None
        
        Returns:
            credentials (dict[str]): returns public key, private key, and api key.
        """

        try:
            return {'pub_key': os.getenv('pub'), 
                    'priv_key': os.getenv('priv'),
                    'api_key': os.getenv('api_key')
                    }
        except Exception as err:
            print(f"Problem reading public and private keys from .env or reading api key from .env. Error: {err}")
            sys.exit()

class Recipient():
    """
    Class to store recipient configuration data

    Attributes: 
        disc_id (str): the discord id of the recipient
        pub_key (str): the public key of the recipient
        channel_id (str): the channel id of the recipient
    """
    def __init__(self, disc_id:str, pub_key:str, channel_id:str):
        """
        Method to initialize an empty Recipient object

        Parameters:
            disc_id (str): discord id of recipient
            pub_key (str): public key of recipient
            channel_id (str): channel id of recipient
        
        Returns:
            None
        """
        self.disc_id = disc_id
        self.pub_key = pub_key
        self.channel_id =channel_id

class Message():
    """
    Class to store messages retrieved from chats.

    Attributes:
        msg_id (str): The message id of the message.
        author (str): The username of the author of the message.
        message_body (str): A string containing the text content of the message.

    """
    def  __init__(self, msg_id:str, author:str, message_body:str):
        """
        Initializes an empty Message.

        Parameters:
            msg_id (str): The message id of the message.
            author (str): The username of the author of the message.
            message_body (str): A string containing the text content of the message.

        """
        self.msg_id = msg_id
        self.author = author
        self.message_body = message_body
        self.is_encrypted = self._is_encrypted()
        self.should_encrypt = self._should_encrypt()
    
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
    
    def _should_encrypt(self):
        header = ''
        msg = "".join([''+x for x in reversed(self.message_body)])
        try:
            for char in range(4):
                header = header + msg[char]
        except IndexError:
            return True
        if header == "NLP-":
            return False
        else:
            return True
    
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
            client (Client): a Client object 
        """

        self.client = Client()
        self.nickname = nickname

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
            recip_pub_key (Recipient.pub_key): recipient's public key
            recip_disc_id (Recipient.discord_id): recipients discord id
            channel_id (Recipient.channel_id): the id of the dm channel of the chat
            client (Client): A client object
            nickname (str): nickname of the chat instance
        """

        def __init__(self, nickname:str):
            query_data = ['pub_key', 'disc_id', 'channel_id']
            query_results = self._get_init_data(query_data)
            self.recipient = Recipient(query_results['disc_id'],query_results['pub_key'],query_results['channel_id'])
            self.nickname = nickname
            self.client = Client()
            self._setup()

        def _get_init_data(self, queries:list) -> dict:
            """
            Method to prompt user for details about recipient.

            Parameters:
                queries (list): a list of fields to query
            
            Return: 
                returns (dict): a dict with values matching the user inputs to the queries
            """

            options = {
                'pub_key': 'public key ',
                'disc_id': 'discord id ',
                'channel_id': 'channel id '
            }
            returns = {}
            for query in queries:
                returns[query] = input((f"Please input {options[query]}: "))
            
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
            print(file_path)
            try:
                os.mkdir(file_path)
            except FileExistsError:
                print("File already exists in data directory.")
                sys.exit()
            except PermissionError:
                print("Insufficient permissions to write in data directory")
                sys.exit()

            
            data = json.dumps({'pub_key':self.recipient.pub_key,
                    'disc_id':self.recipient.disc_id,
                    'channel_id':self.recipient.channel_id
                    })
            try:
                with open(f"{file_path}channel.conf", "w") as conf_file:
                    conf_file.write(data)
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
            recip_pub_key (Recipient.pub_key): recipient's public key
            recip_disc_id (Recipient.discord_id): recipients discord id
            channel_id (Recipient.channel_id): the id of the dm channel of the chat
            client (Client): A client object
            nickname (str): nickname of the chat instance
            api_key (str): the api key used to connect
        """

        def __init__(self, nickname:str):
            self.nickname = nickname
            self.client = Client()
            recipient_conf = self._read_conf()
            self.recipient = Recipient(recipient_conf['disc_id'],recipient_conf['pub_key'],recipient_conf['channel_id'])
            
            
            

        def _read_conf(self) -> dict:
            """
            Private method to read configuration file.

            Parameters:
                None
            
            Returns:
                config_data (dict): contains 'pub_key', 'disc_id', and 'channel_id'
            
            Exceptions:
                Permission error: calls sys.exit()
            """

            file_path = f"{ROOT_DIR}/data/{self.nickname}/channel.conf"
            try:
                with open(file_path) as file:
                    return json.load(file)
            except PermissionError:
                print(f"Insufficient permissions to open {file_path}")
                sys.exit()
            except Exception as err:
                print(f"Error: {err}")
                sys.exit()