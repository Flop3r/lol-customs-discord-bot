import re

from responses import *

async def handle_command(message, message_content):
    message_content = message_content.lower()

    # Splitting the message content into a command and a list of arguments
    command, *args = message_content.split()

    try:
        if command == "hello":
            await message.reply(HELLO_RESPONSE, mention_author=False)

        elif command == "add":
            response = handle_add_command(args, message.guild)
            await message.reply(response, mention_author=False)

        else:
            await message.reply(INVALID_COMMAND_RESPONSE, mention_author=False)

    except Exception as e:
        print(e)

def handle_add_command(args, guild) -> str:
    # Helper function to check if the argument has a valid format
    def is_valid_arg(arg) -> bool:
        return bool(re.match(r'<@(\d{18})>', arg))

    # Helper function to extract player ID from a valid argument
    def extract_user_id(arg) -> str:
        return re.match(r'<@(\d{18})>', arg).group(1)

    # Check if the number of arguments is correct and if the argument is valid
    if len(args) != 1 or not is_valid_arg(args[0]):
        return INVALID_ARGUMENT_RESPONSE

    user_id = extract_user_id(args[0])
    member = guild.get_member(int(user_id))

    if member:
        return USER_ADDED_RESPONSE
    else:
        return USER_NOT_FOUND_RESPONSE

