from twitter import *
#import json
import urllib
import os
from google.cloud import videointelligence
#from bookshelf import get_model, storage
#from flask import Blueprint, current_app, redirect, render_template, request, url_for
import io


def get_all_tweets(screen_name):

    # Twitter Authentication

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

    # Convert images to a mp4 video
def generate_video(output_name, image_initial_name = None, start_number = None, framerate = None):
    
    # Default settings
    
    if image_initial_name == None:
        image_initial_name = "image_"
    if start_number == None:
        start_number = 1
    if framerate == None:
        framerate = 1/3

    # e.g. image_3.jpg image_initial_name = 'image_'
    # Run ffmpeg in Windows
    
    os.system('ffmpeg -framerate '+str(framerate)+' -i '+image_initial_name+'%d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p '+output_name+'.mp4')
    return output_name
'''
    # Upload the video to google storage
    
def upload_file(file_stream, filename, content_type):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """
    _check_extension(filename, current_app.config['ALLOWED_EXTENSIONS'])
    filename = _safe_filename(filename)

    client = _get_storage_client()
    bucket = client.bucket(current_app.config['CLOUD_STORAGE_BUCKET'])
    blob = bucket.blob(filename)

    blob.upload_from_string(
        file_stream,
        content_type=content_type)

    url = blob.public_url

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url
'''
def analyze_labels_file(path):

    # [START video_analyze_labels]

    """Detect labels given a file path."""

    video_client = videointelligence.VideoIntelligenceServiceClient()

    features = [videointelligence.enums.Feature.LABEL_DETECTION]



    with io.open(path, 'rb') as movie:

        input_content = movie.read()



    operation = video_client.annotate_video(

        features=features, input_content=input_content)

    print('\nProcessing video for label annotations:')



    result = operation.result(timeout=90)

    print('\nFinished processing.')



    # Process video/segment level label annotations

    segment_labels = result.annotation_results[0].segment_label_annotations

    for i, segment_label in enumerate(segment_labels):

        print('Video label description: {}'.format(

            segment_label.entity.description))

        for category_entity in segment_label.category_entities:

            print('\tLabel category description: {}'.format(

                category_entity.description))



        for i, segment in enumerate(segment_label.segments):

            start_time = (segment.segment.start_time_offset.seconds +

                          segment.segment.start_time_offset.nanos / 1e9)

            end_time = (segment.segment.end_time_offset.seconds +

                        segment.segment.end_time_offset.nanos / 1e9)

            positions = '{}s to {}s'.format(start_time, end_time)

            confidence = segment.confidence

            print('\tSegment {}: {}'.format(i, positions))

            print('\tConfidence: {}'.format(confidence))

        print('\n')



    # Process shot level label annotations

    shot_labels = result.annotation_results[0].shot_label_annotations

    for i, shot_label in enumerate(shot_labels):

        print('Shot label description: {}'.format(

            shot_label.entity.description))

        for category_entity in shot_label.category_entities:

            print('\tLabel category description: {}'.format(

                category_entity.description))



        for i, shot in enumerate(shot_label.segments):

            start_time = (shot.segment.start_time_offset.seconds +

                          shot.segment.start_time_offset.nanos / 1e9)

            end_time = (shot.segment.end_time_offset.seconds +

                        shot.segment.end_time_offset.nanos / 1e9)

            positions = '{}s to {}s'.format(start_time, end_time)

            confidence = shot.confidence

            print('\tSegment {}: {}'.format(i, positions))

            print('\tConfidence: {}'.format(confidence))

        print('\n')



    # Process frame level label annotations

    frame_labels = result.annotation_results[0].frame_label_annotations

    for i, frame_label in enumerate(frame_labels):

        print('Frame label description: {}'.format(

            frame_label.entity.description))

        for category_entity in frame_label.category_entities:

            print('\tLabel category description: {}'.format(

                category_entity.description))



        # Each frame_label_annotation has many frames,

        # here we print information only about the first frame.

        frame = frame_label.frames[0]

        time_offset = frame.time_offset.seconds + frame.time_offset.nanos / 1e9

        print('\tFirst frame time offset: {}s'.format(time_offset))

        print('\tFirst frame confidence: {}'.format(frame.confidence))

        print('\n')

    # [END video_analyze_labels]
'''
def analyze_labels(path):
    """ Detects labels given a GCS path. """
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.LABEL_DETECTION]
    operation = video_client.annotate_video(path, features=features)
    print('\nProcessing video for label annotations:')

    result = operation.result(timeout=90)
    print('\nFinished processing.')

    segment_labels = result.annotation_results[0].segment_label_annotations
    for i, segment_label in enumerate(segment_labels):
        print('Video label description: {}'.format(
            segment_label.entity.description))
        for category_entity in segment_label.category_entities:
            print('\tLabel category description: {}'.format(
                category_entity.description))

        for i, segment in enumerate(segment_label.segments):
            start_time = (segment.segment.start_time_offset.seconds +
                          segment.segment.start_time_offset.nanos / 1e9)
            end_time = (segment.segment.end_time_offset.seconds +
                        segment.segment.end_time_offset.nanos / 1e9)
            positions = '{}s to {}s'.format(start_time, end_time)
            confidence = segment.confidence
            print('\tSegment {}: {}'.format(i, positions))
            print('\tConfidence: {}'.format(confidence))
        print('\n')
    '''
if __name__ == '__main__':

    # Find image URLs from twitter and make a list of them, save in a txt file,
    # then download them which are named as image_NUMBER
        
    get_all_tweets("@Ibra_official")
    
    # Generate the video out of the images
    
    video_name = generate_video('out', "image_", 1, 0.3)
    analyze_labels_file(video_name)
