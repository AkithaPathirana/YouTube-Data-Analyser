from datetime import date
from dateutil.relativedelta import relativedelta
from channels import Channels
from videos import Videos

#sorting the videos of a channel based on published date
def sort_date(channel_obj):

    video_dict= channel_obj.video_list
    video_published_dict={}
    
    #dictonary with video_id:video_published_date for all videos of channel
    for obj in video_dict.values():
        video_published_dict[obj]=date.fromisoformat(obj.video_published_date)

    #sort dict based on video_published_date
    video_published_dict={k: v for k,v in sorted(video_published_dict.items(), key= lambda v: v[1])}
    ordered_video_obj=list(video_published_dict.keys())


    #return a video object list sorted by date
    return ordered_video_obj



#slice video object list based on start and end points
def slice_list(video_list,start=None,end=None):

    length=len(video_list)

    if start!=None:
        if start>=1 and start<=length:
            video_list=video_list[start-1:]


    if end!=None:
        if end>=1 and end<=length:
            video_list=video_list[:end]

    return video_list


def round_number(number):

    number=int(number)
    if number<1000 and number>0:
        return number

    elif number>1000 and number<1000000:
        num=number//1000
        string1=str(num)+'K'
        return(string1)

    elif number>1000000 and number< 1000000000:
        num=round(number/1000000, 2)
        string1=str(num)+" Million"
        return(string1)

    elif number>1000000000:
        num=round(number/1000000000, 2)
        string1=str(num)+" Billion"
        return(string1)

    else:
        return number




