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
from chat.messages import *
from chat.members import *
load_dotenv()

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
        self.recipient = chat.members.Recipient(self.nickname)
        self.client = chat.members.Client()


    def send_message(self, message:chat.messages.Message) -> bool:
        """
        Method to send a message to a channel.

        Parameters:
           message (Message): A Message object.
        
        Returns:
            sent (bool): returns True if got code 200

        """

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Authorization': self.client.api_key
        }

        json_data = {
            'content':message.output_text
        }

        response = requests.post(f"https://discord.com/api/v10/channels/{self.recipient.channel_id}/messages", headers=headers, json=json_data)
        if response.status_code == 200:
            return True
        else:
            print(f"Error sending message...Code {response.status_code}")
            sys.exit()

    def get_messages(self,last_message_id:str='', number_of_messages:int=1, both_authors:bool=True, author_id:str='') \
                        -> list[chat.messages.InMessage]:
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
            return [InMessage(output, self.client.priv_key) for output in response.json()]
        else:
            return [InMessage(output, self.client.priv_key) for output in response.json() if output['author']['id'] == self.recipient.disc_id]
    
    def fetch_latest(self, last_message_id:str='') -> bool:
        if last_message_id:
            headers = headers = {'authorization': self.client.api_key}
            receive = requests.get(f"https://discord.com/api/v10/channels/{self.recipient.channel_id}/messages?limit=1&after={last_message_id}", headers=headers)
            if (len(receive.json()) > 0):
                if receive.json()[0]['author']['id'] == self.recipient.disc_id:
                    return True
            else: 
                return False
        else:
            headers = headers = {'authorization': self.client.api_key}
            receive = requests.get(f"https://discord.com/api/v10/channels/{self.recipient.channel_id}/messages?limit=1", headers=headers)
            return receive.json()[0]['id']

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
            self._setup()
            self.recipient = chat.members.Recipient(self.nickname)
            self.client = chat.members.Client()

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

