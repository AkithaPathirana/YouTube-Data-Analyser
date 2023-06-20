
from googleapiclient.discovery import build
from channels import Channels


from videos import Videos
import time

def processing(api_key,channel_id):

    video_list={}
    num_videos=0
    api_requests=0


    youtube = build('youtube', 'v3', developerKey=api_key)


    #Getting the Video via the api
    channel_response = youtube.channels().list(
            part='snippet,contentDetails,statistics',
            id=channel_id
        ).execute()

    api_requests+=1

    #id for uploads playlist which contatins all the videos
    uploads_playlist=channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    channel_name=channel_response['items'][0]['snippet']['title']
    channel_views=channel_response['items'][0]['statistics']['viewCount']
    channel_video_count=channel_response['items'][0]['statistics']['videoCount']
    new_channel=Channels(channel_id)
    new_channel.channel_name=channel_name
    new_channel.channel_views=channel_views
    new_channel.channel_video_count=channel_video_count


    #setting up api to get individual video details
    video_request= youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads_playlist,
            maxResults=100
        )

    api_requests+=1


    while video_request != None:
        video_response=video_request.execute()
        for item in video_response['items']:
            video_title=item['snippet']['title']
            video_published_date=item['snippet']['publishedAt'].split('T')[0]
            video_id=item['snippet']['resourceId']['videoId']
            new_video=Videos(video_id,video_title,video_published_date)
            num_videos+=1
            video_list[video_id]=new_video


            #go through individual videos
            video_details_response= youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=video_id 
            ).execute()
            api_requests+=1

            try:
                new_video.video_likes=video_details_response['items'][0]['statistics']['likeCount']
                new_video.video_views=video_details_response['items'][0]['statistics']['viewCount']
                new_video.video_comments=video_details_response['items'][0]['statistics']['commentCount']
                new_video.video_tags=video_details_response['items'][0]['snippet']['tags']
            except Exception:
                print("Comments Disabled for the video: ",video_title)




        
        api_requests+=1
        video_request=youtube.playlistItems().list_next(video_request,video_response)

    new_channel.video_list=video_list
    return new_channel,api_requests



channels={}
start_time=time.time()
channels['UCSGoIq_tVESqNYF1Re-zn1Q'],api_requests=processing(api_key='AIzaSyBAJ5hNuOHzq2CcIXpnJ7x36Emfsoe4DOA',channel_id= 'UCJZrgdE18ZCUKRBNEqeoOjA')
end_time=time.time()


print('api requests: ',api_requests)

print('\n')

print(channels['UCSGoIq_tVESqNYF1Re-zn1Q'].channel_name)
print(channels['UCSGoIq_tVESqNYF1Re-zn1Q'].channel_views)
print(channels['UCSGoIq_tVESqNYF1Re-zn1Q'].channel_video_count)
print(channels['UCSGoIq_tVESqNYF1Re-zn1Q'].video_list)
print("\n")
print('processing_time:min ',(end_time-start_time)/60)