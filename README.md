# groupmebot

This is a bot for the GroupMe chat platform. GroupMe allows bots to be added to your chats and will automatically post all messages to a specified URL. The bot is created using the Django framework and hosted at https://www.responsebot.herokuapp.com. I currently use it in a personal group chat and anyone is welcome to sign up for a bot using the instructions on the aforementioned site. Instructions on how to set up the bot on GroupMe's end can be found here: https://responsebot.herokuapp.com/create_bot_instructions/.

The bot is simple and has several built in commands for creating and editing custom commands. There are two types of creatable commands: unique commands and non-unique commands. Unique commands only have one pre-programmed response and are used like /commandname. The bot will then send the response specified when the command was created. Non-unique or random commands may have more than one response. When the command is called like /random commandname the bot will randomly pick from all of the responses programmed for that command and send that to the chat. Instructions on how to use the bot can be found here: https://responsebot.herokuapp.com/guide/.

Currently the bot is programmed using text commands directly in chat. The next upcoming feature will be editing the bot on the website and hold an account with multiple bots.
