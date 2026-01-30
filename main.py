from chat.chat import *
from session.session import Session
from session.setup import SetupUtils
import sys
def main():
    possible_args = {
        'new_chat':'',
        'open_chat':''
    }
    setup_tools = SetupUtils()
    arguments = sys.argv
    ind = 0
    if arguments[1] == 'fts':
        setup_tools.first_time_setup()
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
                    session.start_session()
                    
                
                elif argument == 'open_chat':
                    chat = ExisChat(possible_args[argument])
                    session = Session(chat)
                    session.start_session()
                
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