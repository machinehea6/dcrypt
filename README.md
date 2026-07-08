# dcrypt
dcrypt is a Linux CLI wrapper for discord dms with integrated RSA encryption. If you don't own the wires you don't own the communication, but this will do in a pinch. 
## LLM Training Disclaimer
This project is distributed under a GPL license with the express intent that it remain free. It is the position of the creator of this project that an LLM does meaningfully encode the data it is trained on, and that should a model be trained on GPL licensed material the model must be distributed under the same license. 
## About
- RSA encryption is handled with the PyCryptodome package. Key generation, message padding, encryption, and decryption are all handled with this package.
- Implementing RSA is notoriously difficult and it is beyond my confidence level to create my own implementation or audit it.
- For stable and working version please stick to x.0.0 releases. Currently 1.0.0 is the last stable version.
## Setup Guide
### Dependencies and Environment
- Create a new virtual environment. *It must be titled 'venv'.* 
```Bash
python -m venv venv
```
- Activate the virtual environment. 
```Bash
source venv/bin/activate
```
- Install dependencies.
```Bash
pip install -r requirements.txt
```

### Running the Program
#### General
- Dcrypt has options fts (first time setup), new_chat, and open_chat. 
- fts: takes no arguments and begins first time setup
- new_chat: takes an argument 'nickname' which will create a new chat config entry titled 'nickname.'
- open_chat: takes an argument 'nickname' which will create a session based on data in the data/'nickname' directory

#### First Time Setup
- Run first time setup. Have on hand your discord user id, api key, and discord username.  
- Get your user id by clicking your profile in the discord client and clicking 'Copy User ID.' <br>
**This is not the same as your username.**
- Get your api key by doing the following:
    1. Open the discord *web client.* 
    2. Open any direct message.
    3. Press ctrl + shift + i.
    4. Click the 'Network' tab.
    5. Type any text in the message box.
    6. You will see a new entry under the 'Network' tab labeled 'typing' under file type.
    7. Click this entry and go to Request Headers -> Authorization then copy the key.
- Run first time setup as follows:
```Bash
python main.py fts
```

#### Opening a New Chat
- Have on hand your friend's discord id, the channel id of the dm, their public key file, and a nickname to call the chat.
- To get their discord id right click on their name and click 'Copy User ID.' <br>
**This is not the same as their username.**
- To get their public key file, have them run first time setup and send you their pub_key.pem file, keep it somewhere easy to access. <br>
**Keep the title as 'pub_key.pem'**
- To get the channel id, right click on the dm and click 'Copy Channel ID.'
- Nickname is your preference.
- With all this available, enter the following:
```Bash
python main.py new_chat [chat_nickname]
```
Note, nickname does not need to be enclosed in quotation marks.

#### Opening an Existing Chat
- All you need on hand is the nickname you selected for the chat.
```Bash
python main.py open_chat [chat_nickname]
```
Note, the 'nickname' argument should be as you entered it in setup, **verbatim**. 
### Using the Chat
Using the chat should be fairly straightforward, simply enter your text and press enter. To exit the chat hit ctrl + c. 
Messages are encrypted by default, but if you'd like to send in plaintext simply add -PLN to the end of your message.
Messages will appear in the chat in the following format: <br>
[author discord username]   [Encrypted: True or False]: Message body.
