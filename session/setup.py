from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from definitions import *
import os
from dotenv import load_dotenv, dotenv_values

class Setup():
    def __init__(self):
        is_setup = (self._check_is_keys() and self._is_api_key() and self._is_user_config)
        if is_setup == False:
            print("false")
            self._make_env()
            self._gen_keys()
            self._set_api_key()
            self._set_user_config()
            print(f"Setup complete. Public and private keys placed at: {ROOT_DIR}/data/secrets.")
        else:
            self._should_reset()

    def _set_api_key(self) -> None:
        try:
            api_key = input("Enter client api key: ")
        except Exception as err:
            print(f"There was {err} with your input.")
        try:
            self._add_env_var('api_key',api_key)
            print("api_key environmental variable set.")
        except:
            print("Could not set api_key environment variable.")
    
    def _make_env(self):
        if '.env' in os.listdir(ROOT_DIR):
            return
        else:
            with open(f"{ROOT_DIR}/.env","w") as f:
                f.write("init")

    def _is_api_key(self) -> bool:
        if os.getenv('api_key') == None:
            return False
        else:
            return True

    def _is_user_config(self) -> bool:
        try:
            user_id = (os.getenv('user_id') == None)
        except Exception as err:
            print(f"Problem getting user_id env variable. Error: {err}")
        try:
            username = (os.getenv('username') == None)
        except Exception as err:
            print(f"Problem getting username env variable. Error: {err}")
        if user_id and username:
            return True
        else:
            return False

    def _set_user_config(self) -> None:
        try:
            username = input("Enter client discord username: ")
        except Exception as err:
            print(f"There was {err} with your input.")
        try:
            self._add_env_var('username',username)
            print("username environmental variable set.")
        except:
            print("Could not set username environment variable.")
        try:
            user_id = input("Enter client discord user id: ")
        except Exception as err:
            print(f"There was {err} with your input.")
        try:
            self._add_env_var('user_id',user_id)
            print("user_id environmental variable set.")
        except:
            print("Could not set user_id environment variable.")
        
    def _should_reset(self) -> None:
        try:
            reset = input("Program already setup, reset? y/n").lower()
        except Exception as err:
            print(f"Error, {err}, with your input.")
            sys.exit()
        if reset == 'y':
            self._gen_keys()
            print("New keys generated.")
            self._set_user_config()
            print("New user config set.")
            self._set_api_key()
            print("New api key set.")
        elif reset == 'n':
            print("Keys and config not altered.")
        else:
            print("Problem with input, please enter y or n.")
            sys.exit()

    def _check_is_keys(self):
        try:
            key_files = os.listdir(f"{ROOT_DIR}/data/secrets")
            if len(key_files) < 2:
                return False
            else:
                return True
        except FileNotFoundError:
            os.mkdir(f"{ROOT_DIR}/data/secrets")
            return False
    
    def _gen_keys(self):
        priv_key = RSA.generate(3072)
        pub_key = priv_key.public_key()

        with open(f"{ROOT_DIR}/data/secrets/priv_key.pem", "wb") as f:
            data = priv_key.export_key()
            f.write(data)
        with open(f"{ROOT_DIR}/data/secrets/pub_key.pem", "wb") as f:
            data = pub_key.export_key()
            f.write(data)
    
    def _add_env_var(self, key:str, value:str) -> None:
        with open(f"{ROOT_DIR}/.env", "a") as env:
            env.write(f"{key} = {value}")
        return