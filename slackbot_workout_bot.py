import os
import time
import re
import random
import sys
from slackclient import SlackClient


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
LOWER_BODY_COMMAND = ("Make me a lower body workout")
UPPER_BODY_COMMAND = ("Make me an upper body workout")
FULL_BODY_COMMAND = ("Make me a full body workout")
#BIRTHDAY_WORKOUT_COMMAND = "Make me a birthday workout"
USER_HELPER_COMMAND = "Make me a lower body workout, Make me an upper body workout or Make me a full body workout"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

#move arrays
chest_moves = ["Incline Dumbell Press", "Flat DB Press", 
               "Plyo Push Up", "Barbell Bench Press", 
               "DB Pullover","Incline DB Fly","Triangle Push Ups", 
               "Plate Squeeze Raise","Wide Grip Push Ups"]
               
               
back_moves = ["Wide-Grip Pull-Up", "Bent-Over Barbell Deadlift", 
             "Standing T-Bar Row", "Single-Arm Dumbbell Row", 
             "Inverted Row", "DB Rows", "Chin Ups", "Body Weight Row"]


front_leg_moves = ["Barbell Squats", "Barbell Front Squats", "Prowler Push",
                  "Goblet Squats","Squat Jumps", "Wall Ball Squat Throw"]

back_leg_moves = ["Deadlift", "Lunges", "Hamstring Raises", "Romanian Deadlift",
                  "Kettlebell One Legged Deadlift","Glut Ham Lowers"]


full_body_moves = ["Burpees", "Single Arm KB Snatch", "Ball Slams",
                   "Sledge Hammer Tire Hits","Spider-Man Plank", "DB Complex", 
                   "Sandbag Over Shoulder","20 Jump Ropes", "Bar Push Up - Clean + Press", 
                   "Ladder Push-Ups (Optional: Feet Jump In)", "Jumping Chins or 1 x Salmon Ladder"]



def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)





def heh_lower_body_workout_maker():

	back_leg_moves_random =  "\n".join(random.sample(front_leg_moves, 4))
	front_leg_moves_random = "\n".join(random.sample(back_leg_moves, 4))

	return "-----BLOCK A-----" + "\n"+ "{}".format(back_leg_moves_random) +"\n" + "-----BLOCK B-----" + "\n"+ "{}".format(front_leg_moves_random)
    
    
def heh_upper_body_workout_maker():

	chest_moves_random =  "\n".join(random.sample(chest_moves, 4))
	back_moves_random = "\n".join(random.sample(back_moves, 4))

	return "-----CHEST BLOCK-----" + "\n"+ "{}".format(chest_moves_random) +"\n" + "-----BACK BLOCK-----" + "\n"+ "{}".format(back_moves_random)
    
def primed_weekend_full_body_workout_maker():

    primed_weekend_full_body_random = "\n".join(random.sample(full_body_moves, 8))
    return "******** 5 - 7 - 11 - 13 - 17 - 23 ********" + "\n"+ "{}".format(primed_weekend_full_body_random) #+"\n" + "-----BLOCK B-----" + "\n"+ "{}".format(front_leg_moves_random)
    


def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(USER_HELPER_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    #first lets do the lower body commands
    
    if command.startswith(UPPER_BODY_COMMAND):
        response = "Of course! Heres an upper body workout: "+"\n"+"Each block 3 rounds before moving on. (8-10 reps) "+"```{}```".format(heh_upper_body_workout_maker())
        
    elif command.startswith(LOWER_BODY_COMMAND):
        response = "Of course! Heres a lower body workout: "+"\n"+"4 rounds, alternate between Block A and B (8-10 reps) "+"```{}```".format(heh_lower_body_workout_maker())

    elif command.startswith(FULL_BODY_COMMAND):
        response = "Of course! Heres a full body workout: "+"\n"+"Reps go up each round in Prime factors, complete after 40 minutes. "+"```{}```".format(primed_weekend_full_body_workout_maker())

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )
	
if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
