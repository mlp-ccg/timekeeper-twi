This is a simple, Python based script to help manage timing for rounds of a tournament via Discord.

You need Python 3 installed on a computer. Get that here, if you don't have it. Any Python 3 should be fine. https://www.python.org/downloads/

You'll also need (or know someone who has)
* a Discord server
* (suggested) a dedicated channel to use for tournament operations
* the ability to make webhooks in that server + channel
* a role for people playing in the tournament
* (optional) a role for judges who can help administrate the tournament

Help with Discord server setup and configuration is beyond the scope of this readme. Ask Google or ChatGPT or something.

You can run the script and it will go through a simple setup process for you to configure the webhooks and roles for your event. The script should send a message to the channel if all is well. Reminder: do not share the JSON file this produces; webhook URIs are secrets that give anypony who knows them power over the server.

You'll then want to edit the script to choose what kind of clock you want the players on. In general, this will follow the structure of a MLP:CCG tournament, where there's 3 minutes of setup, 35 minutes of play and 5 minutes of soft time. Once you change the script over to the appropriate clock, just run it and the clock will start.
