from datetime import datetime
from post import Post

def weight(p: Post):
    current_time = datetime.now()  # Get the current time now to help find the most recent post
    if p.verified is True:
        weight = 1.5 #If it is a verified person, the score will increase by 0.5
    else:
        weight = 1.0
    time_dif = current_time-p.date
    time_weight = 1.0 - (time_dif.total_seconds())/(current_time.timestamp()) #this is a decay multiplier which decreases the score the older the post is
    weight = weight * time_weight

    return weight
        
