from datetime import datetime
from post import Post

#This function identifies whether the post is made by a verified person and increases its score
def verified_weight(p: Post):
    if p.verified is True:
        return 1.5 #If it is a verified person, the score will increase by 0.5
    else:
        return 1.0

#This function determines how old a post is and adjust the score so that later posts have a lower score
def date_weight(p: Post):
    current_time = datetime.now() # Gets the current time
    time_dif = current_time-p.date
    time_weight = 1.0 - (time_dif.total_seconds())/(current_time.timestamp()) #this is a decay multiplier which decreases the score the older the post is
    return time_weight
        
