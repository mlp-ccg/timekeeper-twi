This is a simple, Python based script to help manage timing for rounds of a tournament via Discord.

You need Python 3 installed on a computer. Get that here, if you don't have it. Any Python 3 should be fine. https://www.python.org/downloads/

You'll also need (or know someone who has)
* a Discord server
* (suggested) a dedicated channel to use for tournament operations
* the ability to make webhooks in that server + channel
* a role for people playing in the tournament
* (optional) a role for judges who can help administrate the tournament

Help with Discord server setup and configuration is beyond the scope of this readme. Ask Google or ChatGPT or something.

# Setup and use

Download the Python script to somewhere handy.

Run the script and it will go through a simple setup process for you to configure the webhooks and roles for your event. You can use either a person's user id or a role for the judges, if you have a lot of them; remember to be kind and clean the role out lest you repeatedly ping somebody at 4 AM their time. The script should send a message to the channel if all is well. Reminder: do not share the JSON file this produces; webhook URIs are secrets that give anypony who knows them power over the server.

You'll then want to edit the script around line 25 to choose what kind of clock you want the players on. You probably want `onlineSwissPlayClock`, which will follow the structure of a MLP:CCG tournament where there's 3 minutes of setup, 35 minutes of play and 5 minutes of soft time.

Once you change the script over to the appropriate clock, just run it and the clock will start and ping the players/judges at crucial points in the round.
