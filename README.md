# Discord Bot

This is a Discord bot implemented in Python using the discord.py library. The bot tracks the activity of members in a server, including the number of commands used and the duration of their presence on the server.

## Features

- Track the number of commands used by each member.
- Calculate the duration of a member's presence on the server.
- Retrieve the command history of a member.
- Navigate through the command history.
- Reset the conversation and clear the command history.

## Installation

1. Clone the repository:

git clone https://github.com/burukku920/python_bot

2. Install the required dependencies:

pip install -r requirements.txt


3. Replace the placeholder token in the code (`bot.run("YOUR_BOT_TOKEN")`) with your Discord bot token. You can create a bot and obtain the token from the Discord Developer Portal.

## Usage

1. Run the bot using the following command:


2. The bot will connect to Discord and be ready to respond to commands.

3. Use the bot commands in Discord to interact with the bot. Some available commands include:

- `!resume`: Get a summary of your activity on the server.
- `!historique`: View your command history.
- `!lastCommand`: Get the last command used in the server.
- `!moveL`: Move to the left/previous command in the history.
- `!moveR`: Move to the next/right command in the history.
- `!binH`: Clear the command history.
- `!reset`: Reset the conversation and clear the command history.
- `!speakA <sujet>`: Make the bot speak about a specific subject.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.
