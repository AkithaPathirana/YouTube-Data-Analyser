
from logging import exception
from googleapiclient.discovery import build
import time
from graph_functions import *
from main_functions import *
from processing import processing

api_key='AIzaSyBAJ5hNuOHzq2CcIXpnJ7x36Emfsoe4DOA'
channels={}
youtube = build('youtube', 'v3', developerKey=api_key)
api_requests=0
channel_index=0

while True:
    print("-------------------------------------------\n")
    print("1) ADD CHANNELS")
    print("2) VIEW CURRENT CHANNELS")
    print("3) ANALYZE CHANNELS\n")
    print("Enter The Number Corresponding to Your Choice")
    user_input1=input()


    if(user_input1=='1'):
        print("-------------------------------------------\n")
        print("Enter the channel ID's as a comma separated list")
        print('Example: "channelID1","channelID2"')
        user_input2=input().split(',')
        for channelID in user_input2:
            try:
                #Getting the Video via the api
                channel_response = youtube.channels().list(
                        part='snippet,contentDetails,statistics',
                        id=channelID
                    ).execute()

                start_time=time.time()
                print("Processing Channel: ",channelID)
                channels[channel_index+1],api_requests=processing(api_key=api_key,channel_id= channelID)
                end_time=time.time()
                print("\nChannel ",channels[channel_index+1].channel_name," Processed Successful!")
                print("Api Requests Made: ",api_requests)
                print("\n")
                channel_index+=1

            except Exception as e:


                print("The Channel: ",channelID," is incorrect!")
                continue

        print("\nAll Channels Processed!")
        for ch in channels.values():
            print("Channel: ",ch.channel_name)

    
    
    
    
    elif(user_input1=='2'):
        table_data=[]
        table_data.append(["Channel Name","Channel Views","Channel Video Count"])
        for chan in channels.values():
            name=chan.channel_name
            view=round_number(chan.channel_views)
            video=chan.channel_video_count
            table_data.append([name,view,video])
            
        tb_graph=table(table_data)
        print(tb_graph)


    elif(user_input1=='3'):
        print("-------------------------------------------\n")
        print("1) GO BACK")
        print("2) ANALYZE A SINGLE CHANNEL")
        print("3) ANALYZE MULTIPLE CHANNELS\n")
        print("Enter The Number Corresponding to Your Choice: ")
        user_input3=input()

        if(user_input3=='1'):
            continue
        elif(user_input3=='2'):
            channel_table=[]
            channel_table.append(['Index','Channel Name','Channel Views','Channel Video Count'])
            index=1
            for ch in channels.values():
                name=ch.channel_name
                views=round_number(ch.channel_views)
                videos=ch.channel_video_count
                channel_table.append([index,name,views,videos])
                index+=1

            tb_graph=table(channel_table)
            print("CHANNEL INFORMATION\n")

            print(tb_graph)
            print('\n')
            print("Enter the index of the channel to be analyzed: ")
            analyse_channel=input()

            try:
                channel_number=int(analyse_channel)
                if channel_number>len(channels) or channel_number<1:
                    print("Wrong Index")
                    continue
            except exception:
                print("Wrong Input")
                continue
            start=None
            end=None
            ordered_video_obj=sort_date(channels[channel_number])
            while True:
                print("-------------------------------------------")
                print("Note: Graph will display information based on the ascending order of the published date\n")
                print("1) Video Views Graph")
                print("2) Video Likes Graph")
                print("3) Video Comments Graph")
                print("4) Video Publish Period Graph")
                print("5) Video Views,Likes,Comments in one Graph")                
                print("6) Video Details")
                print("7) Change the number of videos on the graph")
                print("8) Go Back\n")
                print("Enter The Number Corresponding to Your Choice: ")
                graph_input=input()

                if(graph_input=='1'):
                    video_list=slice_list(ordered_video_obj,start,end)
                    x_axis,y_axis=views_plot(video_list)
                    single_line_single_plot(x_axis,y_axis,y_label='Views',legend=channels[channel_number].channel_name,title='Total Views for Each Published Video')

                elif(graph_input=='2'):
                    video_list=slice_list(ordered_video_obj,start,end)
                    x_axis,y_axis=likes_plot(video_list)
                    single_line_single_plot(x_axis,y_axis,y_label='Likes',legend=channels[channel_number].channel_name,title='Total Likes for Each Published Video')

                elif(graph_input=='3'):
                    video_list=slice_list(ordered_video_obj,start,end)
                    x_axis,y_axis=comments_plot(video_list)
                    single_line_single_plot(x_axis,y_axis,y_label='Comments',legend=channels[channel_number].channel_name,title='Total Comments for Each Published Video')            

                elif(graph_input=='4'):
                    video_list=slice_list(ordered_video_obj,start,end)
                    x_axis,y_axis=published_plot(video_list)
                    single_line_single_plot(x_axis,y_axis,y_label='Published Date Difference',legend=channels[channel_number].channel_name,title='Published Day Difference between Successive Videos for Each Published Video')            
                
                elif(graph_input=='5'):
                    video_list=slice_list(ordered_video_obj,start,end)
                    x_axises=[]
                    y_axises=[]
                    x_axis,y_axis=views_plot(video_list)
                    x_axises.append(x_axis)
                    y_axises.append(y_axis)
                    x_axis,y_axis=likes_plot(video_list)
                    x_axises.append(x_axis)
                    y_axises.append(y_axis)                    
                    x_axis,y_axis=comments_plot(video_list)
                    x_axises.append(x_axis)
                    y_axises.append(y_axis)
                    legends=['Views Count','Likes Count','Comments Count']
                    title='Total Views,Likes,Comments for Each Published Video'
                    multi_line_single_plot(x_axises,y_axises,y_label='Y',legends=legends,title=title)

                    
                elif(graph_input=='6'):

                    video_data=[]
                    video_data.append(['Index','Name','Comments','Likes','Views'])
                    index1=1
                    video_list=slice_list(ordered_video_obj,start,end)
                    for vid in video_list:
                        name=vid.video_title
                        comments=vid.video_comments
                        views=round_number(vid.video_views)
                        likes=vid.video_likes
                        video_data.append([index1,name,comments,likes,views])
                        index1+=1

                    print(table(video_data))

                elif(graph_input=='7'):
                    try:
                        start=int(input('Enter the Index for the First Video\n'))
                        end=int(input('Enter the Index for the Last Video [Enter -1 to keep the default last Video]\n'))
                        if end==-1:
                            end=None
                        else:
                            end=end-start+1
                    except exception:
                        print("Wrong Input")
                elif(graph_input=='8'):
                    break
                else:
                    print("Wrong Input")



        elif(user_input3=='3'):
            channel_table=[]
            channel_table.append(['Index','Channel Name','Channel Views','Channel Video Count'])
            index=1
            for ch in channels.values():
                name=ch.channel_name
                views=round_number(ch.channel_views)
                videos=ch.channel_video_count
                channel_table.append([index,name,views,videos])
                index+=1

            tb_graph=table(channel_table)
            print("CHANNEL INFORMATION\n")

            print(tb_graph)
            print('\n')
            print("Enter a space separated list of indexes of the channels to be analyzed: ")
            print('Example: 1 2 4 5\n')
            analyse_channels=input().split(' ')
            index_of_channels_analyzed=[]
            
            for ch in analyse_channels:
                if ch!=' ' or ch!='':
                    try:
                        channel_number=int(ch)
                        if channel_number>len(channels) or channel_number<1:
                            print("Wrong Index")
                            continue
                        index_of_channels_analyzed.append(channel_number)
                    except exception:
                        print("Wrong Input")
                        continue    

            start=None
            end=None
            ordered_video_obj_channels={}
            for number in index_of_channels_analyzed:
                ordered_video_obj_channels[number]=sort_date(channels[number])

            while True:
                print("-------------------------------------------")
                print("Note: Graph will display information based on the ascending order of the published date\n")
                print("1) Video Views Graph")
                print("2) Video Likes Graph")
                print("3) Video Comments Graph")
                print("4) Video Publish Period Graph")
                print("5) Video Likes/Views Graph[Scaled to 100]")
                print("6) Video Comments/Views Graph[Scaled to 1000]")
                print("7) Video Details")
                print("8) Change the number of videos on the graph")
                print("9) Go Back\n")
                print("Enter The Number Corresponding to Your Choice: ")
                graph_input=input()               
                
                if(graph_input=='1'):
                    x_axises=[]
                    y_axises=[]
                    legends=[]
                    for key,value in ordered_video_obj_channels.items():
                        video_list=slice_list(value,start,end)
                        x_axis,y_axis=views_plot(video_list)
                        x_axises.append(x_axis)
                        y_axises.append(y_axis)
                        legends.append(channels[key].channel_name)

                    multi_line_single_plot(x_axises,y_axises,y_label='Views',legends=legends,title='Total Views for Each Published Video for the Selected Channels')


                elif(graph_input=='2'):
                    x_axises=[]
                    y_axises=[]
                    legends=[]
                    for key,value in ordered_video_obj_channels.items():
                        video_list=slice_list(value,start,end)
                        x_axis,y_axis=likes_plot(video_list)
                        x_axises.append(x_axis)
                        y_axises.append(y_axis)
                        legends.append(channels[key].channel_name)

                    multi_line_single_plot(x_axises,y_axises,y_label='Likes',legends=legends,title='Total Likes for Each Published Video for the Selected Channels')                           


                elif(graph_input=='3'):
                    x_axises=[]
                    y_axises=[]
                    legends=[]
                    for key,value in ordered_video_obj_channels.items():
                        video_list=slice_list(value,start,end)
                        x_axis,y_axis=comments_plot(video_list)
                        x_axises.append(x_axis)
                        y_axises.append(y_axis)
                        legends.append(channels[key].channel_name)

                    multi_line_single_plot(x_axises,y_axises,y_label='Comments',legends=legends,title='Total Comments for Each Published Video for the Selected Channels')


                elif(graph_input=='4'):
                    x_axises=[]
                    y_axises=[]
                    legends=[]
                    for key,value in ordered_video_obj_channels.items():
                        video_list=slice_list(value,start,end)
                        x_axis,y_axis=published_plot(video_list)
                        x_axises.append(x_axis)
                        y_axises.append(y_axis)
                        legends.append(channels[key].channel_name)

                    multi_line_single_plot(x_axises,y_axises,y_label='Date Difference',legends=legends,title='Published Date Difference between Successive Videos for the Selected Channels')  


                elif(graph_input=='5'):
                    x_axises=[]
                    y_axises=[]
                    legends=[]
                    for key,value in ordered_video_obj_channels.items():
                        video_list=slice_list(value,start,end)
                        x_axis,y_axis=likes_by_views_plot(video_list)
                        x_axises.append(x_axis)
                        y_axises.append(y_axis)
                        legends.append(channels[key].channel_name)

                    multi_line_single_plot(x_axises,y_axises,y_label='Likes/Views[Scaled by 100]',legends=legends,title='Likes/Views[Scaled by 100] for Each Published Video for the Selected Channels') 


                elif(graph_input=='6'):
                    x_axises=[]
                    y_axises=[]
                    legends=[]
                    for key,value in ordered_video_obj_channels.items():
                        video_list=slice_list(value,start,end)
                        x_axis,y_axis=comments_by_views_plot(video_list)
                        x_axises.append(x_axis)
                        y_axises.append(y_axis)
                        legends.append(channels[key].channel_name)

                    multi_line_single_plot(x_axises,y_axises,y_label='Comments/Views[Scaled by 1000]',legends=legends,title='Comments/Views[Scaled by 1000] for Each Published Video for the Selected Channels') 


                elif(graph_input=='7'):
                    x_axises=[]
                    y_axises=[]
                    legends=[]
                    for key,value in ordered_video_obj_channels.items():

                        video_data=[]
                        video_data.append(['Index','Name','Comments','Likes','Views'])
                        index1=1
                        video_list=slice_list(value,start,end)
                        for vid in video_list:
                            name=vid.video_title
                            comments=vid.video_comments
                            views=round_number(vid.video_views)
                            likes=vid.video_likes
                            video_data.append([index1,name,comments,likes,views])
                            index1+=1
                        
                        print("Channel Name: ",channels[key].channel_name)
                        print('\n')
                        print(table(video_data))


                elif(graph_input=='8'):
                    try:
                        start=int(input('Enter the Index for the First Video\n'))
                        end=int(input('Enter the Index for the Last Video [Enter -1 to keep the default last Video]\n'))
                        if end==-1:
                            end=None
                        else:
                            end=end-start+1
                    except exception:
                        print("Wrong Input")
                elif(graph_input=='9'):
                    break
                else:
                    print("Wrong Input")


        else:
            print("Wrong Input")

        
    
    
    
    
    else:
        print("Wrong Input\n")





