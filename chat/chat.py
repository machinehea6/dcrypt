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
    A Superclass to create and manage chat configuration data, get messages, and send messages.

    Attributes:
        client (members.Client): a client
        recipient (members.Recipient): a recipient object
        nickname (str): nickname of the chat instance

    Private Methods: 
        None 

    Public Methods:
        send_message(): 
            Sends the body of an OutMessage object with a post request to the channel. 
        
        get_messages():
            Public method to get a batch of messages from the chat.
            
        ping():
            Checks the connection to the chat. Returns True if the response is 200, else False.
    """

    def __init__(self, nickname:str):
        """
        Creates a new empty Chat object.

        Parameters:
            nickname (str): the nickname of the chat
        """

        self.nickname = nickname
        self.recipient = chat.members.Recipient(self.nickname)
        self.client = chat.members.Client()
        self.__setup_tool = setup.SetupUtils()


    def send_message(self, message:chat.messages.OutMessage) -> bool:
        """
        Method to send a message to a channel.

        Sends the body of an outmessage object to the chat with a post request.

        Initiates a post request, if response.status_code is 200, returns True. If 401 or 403 tries updating api key and making the request again.

        Parameters:
           message (OutMessage): An OutMessage object.
        
        Returns:
            sent (bool): returns True if got code 200, else returns False.

        """

        def header(api_key:str)->dict:
            """
            Helper function to format authorization header.

            Parameters:
                api_key (str): the api key belonging to the current session. 
            
            Returns:
                headers (dict): 'User Agent': user_agent, 'Authorization' : api_Key 
            """

            return {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
                'Authorization': api_key
            }

        def json_data(message_text:str) -> dict:
            """
            Helper function to process message data

            Parameters:
                message_test (str): the body of an OutMessage object
            
            Returns:
                formatted json (dict): 'content' : 'message_text'
            """

            return {
                'content':message_text
            }

        def make_request() -> requests.Response:
            """
            Helper function to send a post request to the current channel.

            Parameters:
                None

            Returns:
                response (requests.response): returns a response object for the post request.
            """

            response = requests.post(
                                f"https://discord.com/api/v10/channels/{self.recipient.channel_id}/messages",
                                headers=header(self.client.api_key),
                                json=json_data(message.output_text)
                                )
            return response
        
        # Calls the make_request function to send a post request containing the body of the OutMessage
        response = make_request()

        # If the post request is successfully completed returns True
        if response.status_code == 200:
            return True

        # Checks for reponse 401, unauthorized, and tries updating the api key.
        elif response.status_code == 401: 
            print(f"Got code 401.\n")
            new_api_key = (f"Enter new api key to try: ")
            self.__setup_tool.change_env_variable('api_key', new_api_key)
            self.client.api_key = os.getenv('api_key') # changes client api key for future requests

            # Retries the request, returns True if successful
            if make_request().status_code == 200:
                return True

            else:
                # Other response codes aren't as easily fixed, exits.
                print(f"Still could not complete the request. Status code: {response.status_code}")
                return False

        # Checks for 403, forbidden, and tries updating the key and making a new request
        elif response.status_code == 403:
            print(f"Got code 403.\n")
            new_api_key = (f"Enter new api key to try: ")
            self.__setup_tool.change_env_variable('api_key', new_api_key)
            self.client.api_key = os.getenv('api_key') # changes client api key for future requests

            # Retries the request, returns True if successful.
            response = make_request()
            if response.status_code == 200:
                return True
            else:
                print(f"Still could not complete the request. Status code: {response.status_code}")
                return False
        else:
            print(f"Unable to send message. Response code:{response.status_code}")
            return False

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
    
    def ping(self) -> bool:
        """
        Method to check the connection status of a chat.

        Returns:
            connection status (bool): true if 200, false if other.
        """
        
        response = requests.get(f"https://discord.com/api/v10/channels/{self.recipient.channel_id}/messages")
        if response.status_code == 200:
            return True
        else:
            return False


class NewChat(Chat):
        """
        Class to create and manage a chat with a new recipient

        Attributes:
            client (Client): A client object
            recipient (Recipient): A recipient object
            nickname (str): nickname of the chat instance
        
        Public Methods:
            None
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

        def _get_recip_data(self) -> dict:
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
            # Attempts to make the data directory for the new chat
            try:
                os.mkdir(file_path) 
            except FileExistsError:
                # If it exists, either continue with the program or exit the program.
                print("Data directory already exists. ")
                cont = input("Continue? y/n")
                if cont == 'y':
                    pass
                else:
                    sys.exit()

            except PermissionError:
                print("Insufficient permissions to write in data directory")
                sys.exit()

            # Calls the _get_recip_data method to get the recipient's discord id and channel id.
            data = self._get_recip_data()

            try:
                # Writes the recipient configuration data to the channel.conf file
                with open(f"{file_path}channel.conf", "w") as conf_file:
                    conf_file.write(json.dumps(data))

            except PermissionError:
                print(f"Insufficient permissions to open {file_path}")
                sys.exit()
            except Exception as err:
                print(f"Error: {err}")
            print(f"Configuration file created for {self.nickname}\n")
            
            # Creates an empty dictionary that will be used to store chat status.
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
        Class to create and manage a chat with an existing recipient.
        
        Exists to provide readability to code base, currently has no unique attributes or methods.

        Attributes:
            Same as Chat superclass.

        Private Methods:
            Same as Chat superclass.
        Methods:
            Same as Chat superclass.
        """

        def __init__(self, nickname:str):
            """
            Method to initialize an empty ExistChat object.

            Parameters:
                nickname (str): the nickname of the chat to be used 
                
            """

            super().__init__(nickname)

