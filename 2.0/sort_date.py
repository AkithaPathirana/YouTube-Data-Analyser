from datetime import date
from dateutil.relativedelta import relativedelta
from channels import Channels
from videos import Videos

def sort_date(channel_obj,start_date=None,end_date=None):

    video_dict= channel_obj.video_list
    video_published_dict={}
    
    #dictonary with video_id:video_published_date for all videos of channel
    for obj in video_dict.values():
        video_published_dict[obj]=date.fromisoformat(obj.video_published_date)

    #sort dict based on video_published_date
    video_published_dict={k: v for k,v in sorted(video_published_dict.items(), key= lambda v: v[1])}
    ordered_video_obj=list(video_published_dict.keys())



    return ordered_video_obj





# date1=date.fromisoformat('')
# date2=date.fromisoformat('2019-12-04')
# print(date1-relativedelta(months=12))