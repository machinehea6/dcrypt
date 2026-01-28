from chat.chat import Message
class Artist():
    def __init__(self):
        return

    def _pad_name(self, name:str) -> str:
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

    def print_messages(self, all_messages_to_print:list[Message]) -> None:
        """
        Method to print messages to the stdio.

        Parameters:
            A list of Message objects): each one has the attributes 'msg_id', 'author', and 'message_body.'

        Returns:
            None
        """

        for message in reversed(all_messages_to_print):
            message, author = message.message_body, message.author
            print(f"{self._pad_name(author)}: {message}\n")

