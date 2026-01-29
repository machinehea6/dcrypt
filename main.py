from chat.chat import *
from session.session import Session
from session.setup import Setup
import sys
def main():
    possible_args = {
        'new_chat':'',
        'open_chat':''
    }
    arguments = sys.argv
    ind = 0
    if arguments[1] == 'fts':
        first_time_setup = Setup()
    else:
        for argument in arguments[1:]:
            if argument in possible_args:
                try:
                    possible_args[argument] = arguments[arguments.index(argument)+1]
                except IndexError:
                    print("Please enter arguments adjacent to one another.\n")
                    print("Possible arguments are \'fst\' (enter first time setup),\n\
                        \'new_chat\' <chat_nickname>,\n\
                        or \'open_chat\' <chat_nickname>\n")
                    print("Please only enter one of these options.")
                    sys.exit()

                if argument == 'new_chat':
                    chat = NewChat(possible_args[argument])
                    session = Session(chat)
                    session.main_loop()
                    
                
                elif argument == 'open_chat':
                    chat = ExisChat(possible_args[argument])
                    session = Session(chat)
                    session.main_loop()
                
                else:
                    print("Failure parsing args. Please enter your argument and option verbatim without quotation marks and separated by a space.\n")
                    print("Possible arguments are \'fst\' (enter first time setup),\n\
                        \'new_chat\' <chat_nickname>,\n\
                        or \'open_chat\' <chat_nickname>\n")
                    print("Please only enter one of these options.")
                    sys.exit()
            else:
                print("No args detected.\n")
                print("Possible arguments are \'fst\' (enter first time setup),\n\
                    \'new_chat\' <chat_nickname>,\n\
                    or \'open_chat\' <chat_nickname>\n")
                print("Please only enter one of these options.")
                sys.exit()
        
if __name__ == "__main__":
    main()