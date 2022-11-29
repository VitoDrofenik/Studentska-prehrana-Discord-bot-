# Študentska prehrana
### Discord bot

## Invite
Bota lahko povabite na svoj discord strežnik s klikom na [povezavo](https://bit.ly/2XaFvFn).

## Setup
Before usage, a new Discord application has to be created, as shown in the [instructions](http://discordpy.readthedocs.io/en/latest/discord.html), where the private key is aquired. The key is used when running the application for authentication. It has to be placed into a folder next to the bot file, or directly in the client.run command.

## Usage
The bot has 5 commands:
* /pomoc  
    usage: `/pomoc`  
    the bot sends the help message
* /hrana  
    usage: `/hrana`  
    the bot sends the menu of the chosen restaurant. Which restaurant has been chosen in this instance can be seen in the help message or in the bot.py file where the value is assigned to a variable called "default"
* /ponudba  
    usage: `/ponudba ponudnik:<query>`  
    the bot sends the menu of the restaurant that was chosen from the provided list. The command features autocomplete, which automatically updates choices in the list for the user to choose as the user inputs more characters.
* /informacije  
	usage: `/informacije ponudnik:<query>`  
	the bot sands informations about the restaurant that was chosen from the provided list. The command features autocomplete, which automatically updates choices in the list for the user to choose as the user inputs more characters.
* /povabi  
    usage: `/povabi`  
    the bot sends an invite link for itself to be added to other discord servers