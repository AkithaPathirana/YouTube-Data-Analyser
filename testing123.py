
from googleapiclient.discovery import build

from commentators import Commentators
from videos import Videos

api_key='AIzaSyBAJ5hNuOHzq2CcIXpnJ7x36Emfsoe4DOA'

youtube = build('youtube', 'v3', developerKey=api_key)


#Getting the Video via the api
channel_response = youtube.channels().list(
        part='contentDetails',
        id='UC8Ch40k7gSxNOCSnU-cmnwg'
    ).execute()

#id for uploads playlist which contatins all the videos
uploads_playlist=channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']


#setting up api to get individual video details
video_request= youtube.playlistItems().list(
        part='snippet',
        playlistId=uploads_playlist,
        maxResults=100
    )



while video_request != None:
    video_response=video_request.execute()
    for item in video_response['items']:
        title=item['snippet']['title']
        video_published_date=item['snippet']['publishedAt'].split('T')[0]
        video_id=item['snippet']['resourceId']['videoId']
        new_video=Videos(video_id,title,video_published_date)
        num_videos+=1
        videos_list[video_id]=new_video

        #go through individual videos
        video_details_response= youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=video_id 
        ).execute()
        api_requests+=1

        try:
            new_video.video_likes=video_details_response['items'][0]['statistics']['likeCount']
            new_video.video_views=video_details_response['items'][0]['statistics']['viewCount']
            new_video.video_tags=video_details_response['items'][0]['statistics']['viewCount']
            new_video.video_comments=video_details_response['items'][0]['snippet']['tags']
        except Exception:
            print("Comments Desabled for the video: ",title)




    
    api_requests+=1
    video_request=youtube.playlistItems().list_next(video_request,video_response)


for video in videos_list.keys():
    print(videos_list[video].title)
    print(videos_list[video].video_views)
    print(videos_list[video].video_likes)
    print(videos_list[video].video_comments)
    print(videos_list[video].video_tags)
    print('\n\n')


print("Api Requests: ",api_requests)