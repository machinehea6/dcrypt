from dotenv import load_dotenv, dotenv_values
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
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

