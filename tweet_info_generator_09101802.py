from twitter import *
import json
import urllib

def get_all_tweets(screen_name):

    # Authentication

    api = Twitter(
        auth = OAuth(
                    access_token_key,
                    access_token_secret,
                    consumer_key,
                    consumer_secret,))

    # Get an information list of most recent tweets (max = 200)
    
    new_tweets = api.statuses.user_timeline(screen_name = screen_name, count = 10)

    # Write tweet objects to txt file. Ref: The example script
    
    file_name = 'tweet1.txt'
    file = open(file_name, 'w') 
    print "Writing tweet objects to txt please wait..."

    # This part is messy... It's like there are dictionaries in a dictionary which is inside a list.
    # The for loop picks the picture URLs from the data
    
    for status in new_tweets:
        try:
            file.write(str(status[u'entities'][u'media'][0][u'media_url'])+'\n')

    # Simply skip the tweet if there are no pictures in a tweet. 
    
        except KeyError:
            continue
    
    # Close the file
        
    print "Done"
    file.close()

    # Read image URLs from file

    with open(file_name) as f:
        lines = f.readlines()

    # Download the images and name them in sequence
    
    file_count = 0
    for line in lines:
        file_count += 1
        urllib.urlretrieve(line, "image_"+str(file_count)+".jpg")
get_all_tweets("@Ibra_official")
