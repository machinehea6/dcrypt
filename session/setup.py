from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from definitions import *
import os
import sys
from dotenv import *
from pathlib import Path 

class SetupUtils():
    """
    Class to manage setup of dcrypt, creation of config data, and retrieval of config data.

    Attributes:
        env_file_path (Path): the location of the .env file of dcrypt
    
    Private Methods:
        _has_api_key():
            Checks the .env file for the client's discord api key. Returns True if yes, False if not.
        
        _has_client_config():
            Checks for the user_id and username variables in the .env file. Returns True if both,
            False if not.
        
        _has_rsa_keys():
            Checks data/secrets for pub_key.pem and priv_key.pem. If they are there, returns True,
            else, False.
        
        _destroy_env_file():
            Deletes the existing .env file at the dcrypt program root.
        
        _make_env_file():
            Creates a blank .env file at dcrypt program root.

    Public Methods:
        first_time_setup():
            Checks if dcrypt has access to client rsa keys, api key, user id and username. 
            If not:
                Creates the necessary files and prompts the user for necessary input.
            If yes:
                Asks the user if they want to reset.
                    If yes:
                        Deletes all config data and builds new.
                    If no:
                        Exits the program.
        
        set_api_key():
            Takes user input to get api key, then attempts to write it to .env. Returns True if successful, False if not.
        
        set_client_config():
            Prompts client for their discord id and discord username. Returns true if both are successful, else False.
        
        reset_all_config():
            Prompts the user to reset all config data for dcrypt. 
            If yes:
                Deletes all files in data/secrets and deletes .env file.
                Generates new key pair at data/secrets

                Prompts user for api key, discord id, and discord username.
            
            If no:
                Exits dcrypt.
        
        change_env_variable(key, value):
            Takes a key:value pair and updates the .env file with them, then reloads the env to take effect during the
            current session. Returns True if successful, else False.
        
        gen_rsa_keys():
            Generates an rsa keypair and stores them at data/secrets. Returns True if successful, otherwise calls sys.exit()

    """

    def __init__(self):
        """Creates a new SetupUtils object. Sets .env file path."""
        self.env_file_path = Path(f"{ROOT_DIR}/.env")
        return

    def _has_api_key(self) -> bool:
        """
        Checks the .env file for an api_key

        Parameters:
            None
        
        Returns:
            successful (bool): returns successful if there is a key.
        """

        if os.getenv('api_key') == None:
            return False
        else:
            return True

    def _has_client_config(self) -> bool:
        """
        Function to check for user_id and username variables in the .env file.

        Parameters: 
            None

        Returns:
            successful (bool): returns true if both variables are accessible
        """

        try:
            user_id = (os.getenv('user_id') != None)
        except Exception as err:
            print(f"Problem getting user_id env variable. Error: {err}")
        try:
            username = (os.getenv('username') != None)
        except Exception as err:
            print(f"Problem getting username env variable. Error: {err}")
        if user_id and username:
            return True
        else:
            return False

    def _has_rsa_keys(self):
        try:
            key_files = os.listdir(f"{ROOT_DIR}/data/secrets")
            if len(key_files) < 2:
                return False
            else:
                return True
        except FileNotFoundError:
            os.mkdir(f"{ROOT_DIR}/data/secrets")
            return False

    def _destroy_env_file(self):
        try:
            os.remove(f"{ROOT_DIR}/.env")
        except PermissionError:
            print("Insufficient permissions to delete .env")
            sys.exit()

    def _make_env_file(self):
        try:
            with open(f"{ROOT_DIR}/.env","w") as env:
                pass
        except FileExistsError:
            pass

    def first_time_setup(self):
        is_setup = (self._has_rsa_keys() and self._has_api_key() and self._has_client_config())
        if is_setup == False:
            self._make_env_file()
            self.gen_rsa_key_files()
            self.set_api_key()
            self.set_client_config()
            print(f"Setup complete. Public and private keys placed at: {ROOT_DIR}/data/secrets.")
        else:
            self.reset_all_config()

    def set_api_key(self) -> bool:
        """
        Method to write api_key data to the .env file.

        Parameters:
            None

        Returns:
            succesful (bool): returns True if setting was successful
        """

        try:
            api_key = input("Enter client api key: ")
        except Exception as err:
            print(f"There was {err} with your input.")
            return False
        try:
            self.change_env_variable('api_key',api_key)
            print("api_key environmental variable set.")
            return True
        except:
            print("Could not set api_key environment variable.")
            return False

    def set_client_config(self) -> bool:
        """
        Method to place the client's config data in the .env file.

        Parameters:
            None

        Returns:
            succesful (bool): returns True if both variables were successfully set.
        """

        try:
            username = input("Enter client discord username: ")
        except Exception as err:
            print(f"There was {err} with your input.")
            return False
        try:
            self.change_env_variable('username',username)
            print("username environmental variable set.")
        except:
            print("Could not set username environment variable.")
            return False

        try:
            user_id = input("Enter client discord user id: ")
        except Exception as err:
            print(f"There was {err} with your input.")
            return False
        try:
            self.change_env_variable('user_id',user_id)
            print("user_id environmental variable set.")
        except:
            print("Could not set user_id environment variable.")
            return False

        return True
        
    def reset_all_config(self) -> bool:
        """
        Method to prompt the user to reset all config data for dcrypt.

        Parameter: 
            None
        
        Returns:
            successful (bool): whether the config data was reset. returns true if successfully altered, returns false if unaltered.
        
        Exceptions: 
            PermissionError: if insufficient permissions to write files calls sys.exit()
            Exception: calls sys.exit(). Program cannot proceed without config data.
        """
        try:
            reset = input(
                        "[READ CAREFULLY]\n Program already setup, reset? (y/n) \n[IF YES YOUR RSA KEY PAIR WILL BE DELETED PERMENTANTLY]\n"
                        ).lower()

        except Exception as err:
            print(f"Error, {err}, with your input.")
            self.reset_all_config()

        if reset == 'y':
            try:
                self._destroy_env_file()
                print("Existing .env file deleted.")
                self.gen_rsa_key_files()
                print("New keys generated.")
                self._make_env_file()
                print("Created")
                self.set_client_config()
                print("New user config set.")
                self.set_api_key()
                print("New api key set.")

            except PermissionError:
                print("Insufficient permissions to create necessary files.")
                sys.exit()
            except Exception as err:
                print(f"Other error, \"{err},\" occurred.")
                sys.exit()
            return True
        elif reset == 'n':
            print("Keys and config not altered.")
            return False
        else:
            print("Problem with input, please enter y or n.")
            self.reset_all_config()

    def change_env_variable(self, key:str, value:str) -> bool:
        """
        Sets a new key:value pair in the project root .env file. 

        Changes will take effect in the current session.

        Parameters:
            key (str): the key to set
            value (str): the value to set
        
        Returns: 
            successful (bool): whether the key and value were set successfully
        """

        try:
            set_key(self.env_file_path, key_to_set=key, value_to_set=value)
            os.environ[key] = value #updates the environment variables of the running process
            return True
        except Exception as err:
            print(f"Problem setting or retrieving .env key value pair key:{key}, value: {value}.\n")
            print(f"Error: {err}")
            return False

    def gen_rsa_key_files(self) -> bool:
        """
        Function to generate rsa key pair and write to data/secrets directory.

        Parameters:
            None

        Returns:
            succesful (bool): returns successful if both files were successfully created, calls sys.exit() if impossible.
        
        Exceptions:
            PermissionError: calls sys.exit()
            Other Exception: calls sys.exit(), program cannot proceed without these files.
        """

        priv_key = RSA.generate(3072)
        pub_key = priv_key.public_key()

        try:
            with open(f"{ROOT_DIR}/data/secrets/priv_key.pem", "wb") as f:
                data = priv_key.export_key()
                f.write(data)
        except PermissionError:
            print(f"Insufficient permissions to write to {ROOT_DIR}/data/secrets.")
            sys.exit()
        except Exception as err:
            print(f"Error {err} occurred writing private key to {ROOT_DIR}/data/secrets")
            sys.exit()
          

        try:
            with open(f"{ROOT_DIR}/data/secrets/pub_key.pem", "wb") as f:
                data = pub_key.export_key()
                f.write(data)
        except PermissionError:
            print(f"Insufficient permissions to write to {ROOT_DIR}/data/secrets.")
            sys.exit()
        except Exception as err:
            print(f"Error {err} occurred writing public key to {ROOT_DIR}/data/secrets")
            sys.exit()
        
        return True
    