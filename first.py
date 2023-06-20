
from googleapiclient.discovery import build
from comment_threads import CommentThreads

from commentators import Commentators

api_key='AIzaSyBAJ5hNuOHzq2CcIXpnJ7x36Emfsoe4DOA'

youtube = build('youtube', 'v3', developerKey=api_key)



#Getting the Comments via the api
comment_request = youtube.commentThreads().list(
        part='snippet,replies',
        allThreadsRelatedToChannelId='UC8Ch40k7gSxNOCSnU-cmnwg',
        maxResults=100
    )


while comment_request !=None:
    comment_response=comment_request.execute()
    for item in comment_response['items']:
        commentator_id=item['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
        if commentator_id not in commentators_list.keys():
            
            #create an instance of Commentators and save information
            new_commentator=Commentators(commentator_id)
            num_commentators+=1
            tl_comment_video_id=item['snippet']['topLevelComment']['snippet']['videoId']
            tl_comment_likes=item['snippet']['topLevelComment']['snippet']['likeCount']
            new_commentator.total_likes=new_commentator.total_likes+tl_comment_likes
            new_commentator.num_tl_comments+=1
            if commentator_id not in video_list[tl_comment_video_id].commentators:
                video_list[tl_comment_video_id].commentators.append(commentator_id)

            commentators_list[commentator_id]=new_commentator

            #Create an instance of CommentThreads and save information
            tl_comment_thread_id=item['id']
            new_commentator.comment_threads.append(tl_comment_thread_id)
            video_list[tl_comment_video_id].tl_comment_thread_id.append(tl_comment_thread_id)
            new_comment_thread=CommentThreads(tl_comment_thread_id)
            thread_comment=item['snippet']['topLevelComment']['snippet']['textOriginal']
            thread_replies= item['snippet']['totalReplyCount'] if item['snippet']['canReply']==True else 0
            new_comment_thread.thread_likes=tl_comment_likes
            new_comment_thread.num_replies=thread_replies
            new_comment_thread.comment=thread_comment


            




        else:
            #already existing commentator
            current_commentator=commentators_list[commentator_id]
            tl_comment_video_id=item['snippet']['topLevelComment']['snippet']['videoId']
            tl_comment_likes=item['snippet']['topLevelComment']['snippet']['likeCount']
            current_commentator.total_likes=current_commentator.total_likes+tl_comment_likes
            current_commentator.num_tl_comments+=1
            if commentator_id not in video_list[tl_comment_video_id].commentators:
                video_list[tl_comment_video_id].commentators.append(commentator_id)


            #Create an instance of CommentThreads and save information
            tl_comment_thread_id=item['id']
            current_commentator.comment_threads.append(tl_comment_thread_id)
            video_list[tl_comment_video_id].tl_comment_thread_id.append(tl_comment_thread_id)
            new_comment_thread=CommentThreads(tl_comment_thread_id)
            thread_comment=item['snippet']['topLevelComment']['snippet']['textOriginal']
            thread_replies= item['snippet']['totalReplyCount'] if item['snippet']['canReply']==True else 0
            new_comment_thread.thread_likes=tl_comment_likes
            new_comment_thread.num_replies=thread_replies
            new_comment_thread.comment=thread_comment



    api_requests+=1
    comment_request=youtube.commentThreads().list_next(comment_request,comment_response)
    


print("Number of requests: ",api_requests)
i=0
for key in commentators_list:
    print(commentators_list[key].id)
    print(commentators_list[key].display_name)
    print(commentators_list[key].total_likes)
    print(commentators_list[key].tl_comments)
    print("\n\n")

    i+=1

    if i==10:
        break








