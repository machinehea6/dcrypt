from dotenv import load_dotenv, dotenv_values
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from definitions import *
import json
import sys
from session import setup

load_dotenv()

class Client():
    """
    Class to store client configuration data.

    Attributes:
        pub_key (str): client's public key
        priv_key (str): client's private key
        api_key (str): client's api key
        username (str): the client's discord username
        user_id (str): the client's discord id
    """

    def __init__(self):
        """
        Method to create an empty Client object

        Parameters: 
            None
        
        Returns:
            None
        
        """
        self.setup_tool = setup.SetupUtils()
        keys = self._get_keys()
        self.priv_key, self.pub_key = self._get_keys()
        self.api_key = os.getenv('api_key')
        self.username, self.user_id = self._disc_details()

    def _disc_details(self):
        username = os.getenv('username')
        user_id = os.getenv('user_id')

        if (username == None) or  (user_id  == None):
            print("Could not find client username and id\n")
            username = input("Enter client discord username: ")
            user_id = input("Enter client discord user id: ")
            self.setup_tool.change_env_variable('username', username)
            self.setup_tool.change_env_variable('user_id', user_id)

            # the above function has changed the env variables in the current session.
            username = os.getenv('username')
            user_id = os.getenv('user_id')

            return username, user_id
        else:
             return username, user_id

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

        except FileExistsError:
            print("No private key file, creating new public and private keys.\n")
            setup_tool.gen_rsa_key_files()

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
        def read_key() -> RSA.public_key:
            with open(f"{ROOT_DIR}/data/{self.nickname}/pub_key.pem", "rb") as f:
                data = f.read()
                return RSA.import_key(data)
        
        def prompt_for_file() -> str:
            print(f"Could not find a client public key file. Please have them send you it and place it in {ROOT_DIR}/data/{self.nickname}/ as \'pub_key.pem'\n")
            print(f"If you think you've already done this, make sure that it is titled verbatim: pub_key.pem")
            return input(f"Enter y when you have placed the file, or changed the title, or press n to close the program.\n").lower()
           
        try:
            read_key()

        except FileNotFoundError:
            proceed = prompt_for_file()
            if proceed == 'y':
                key = read_key()
                if key:
                    print("Public key successfully retrieved.")
                    return key
                else:
                    print("Still could not read key file, or key file is empty.")
                    sys.exit()

            elif proceed == 'n':
                sys.exit()
            else:
                print('Problem with your input...')
                proceed()

        except PermissionError:
            print("Insufficient permissions to read public key data, please rerun dcrypt after changing permissions.")
            sys.exit()
        
        except Exception as err:
            print("There was a problem retrieving recipient public key.\n")
            print(f"Make sure you have a public key file at {ROOT_DIR}/data/{self.nickname}/pub_key.pem.\n")
            print(f"Error: {err}")
            sys.exit()

