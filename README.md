# Študentska prehrana
### Discord bot

## Invite
Mojo instanco bota lahko povabite na svoj discord strežnik s klikom na [povezavo](https://bit.ly/2XaFvFn).

## Setup
Before usage, a new Discord application has to be created, as shown in the [instructions](http://discordpy.readthedocs.io/en/latest/discord.html), where the private key is aquired. The key is used when running the application for authentication. It has to be placed into a file next to the bot file, or directly in the client.run command.

## Usage
The bot has 3 commands:
* !pomoc  
    usage: `!pomoc`  
    the bot sends the help message
* !hrana  
    usage: `!hrana`  
    the bot sends the menu of the chosen restaurant. Which restaurant has been chosen in this instance can be seen in the help message or in the bot.py file where the value is assigned to a variable called "default"
* !ponudba  
    usage: `!ponudba <query>`  
    the bot sends the menu of the restaurant that has the entered query in it's name. If there are more restaurants like that, bot sends a numbered list with all those restaurants and waits for the user to reply with a number that is in front of the restaurant he was looking for. If there are multiple restaurants with queryed text in their names, anwser has to be chosen from the list in one minute!
* !informacije  
	usage: `!informacije <query>`  
	the bot sands informations about the restaurant that has the entered query in it's name. If there are more restaurants like that, bot sends a numbered list with all those restaurants and waits for the user to reply with a number that is in front of the restaurant he was looking for. If there are multiple restaurants with queryed text in their names, anwser has to be chosen from the list in one minute!