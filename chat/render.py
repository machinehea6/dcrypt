
class Artist():
    """
    Class to handle rendering the chat.

    Public Methods:
        print_messages():
            Accepts a list of messages as an argument and prints them them to terminal.
    
    Private Methods:
        _pad_name():
            Accepts the author a message and returns the name with the addition of padding.
    """
    def __init__(self):
        return

    def print_messages(self, all_messages_to_print:list[InMessage]) -> None:
        """
        Method to print messages to the console.

        Parameters:
            A list of Message objects: each one has the attributes 'msg_id', 'author', and 'message_body.'

        Returns:
            None
        """

        for message in reversed(all_messages_to_print): # prints from earliest message to received to latest
            message, author, encrypted = message.output_text, message.author, message.is_encrypted
            print(f"{self._pad_name(author)} [{encrypted}]: {message}\n")

    def _pad_name(self, name:Message.author) -> str:
        """
        Private method to pad spaces around the author name for printing. 

        Parameters:
            name (str): The name of the message author
        
        Returns:
            name (str): A string containing the correctly sized author name.
        """
        if len(name) >= 12:
            return name
        else:
            while len(name) < 12:
                name = name + ' '
        return name


