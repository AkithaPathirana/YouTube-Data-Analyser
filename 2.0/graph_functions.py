from cProfile import label
from datetime import date
from email import header
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt
from tabulate import tabulate

#views against video number for a single channel
def views_plot(video_list):
    
    i=1
    x_axis=[]
    y_axis=[]
    for obj in video_list:
        x_axis.append(i)
        y_axis.append(int(obj.video_views))
        i+=1

    return x_axis,y_axis



#likes against video number for a single channel
def likes_plot(video_list):
    
    i=1
    x_axis=[]
    y_axis=[]
    for obj in video_list:
        x_axis.append(i)
        y_axis.append(int(obj.video_likes))
        i+=1

    return x_axis,y_axis



#comments against video number for a single channel
def comments_plot(video_list):
    
    i=1
    x_axis=[]
    y_axis=[]
    for obj in video_list:
        x_axis.append(i)
        y_axis.append(int(obj.video_comments))
        i+=1

    return x_axis,y_axis


#publish period against video number for a single channel
def published_plot(video_list):
    
    i=1
    x_axis=[]
    y_axis=[]
    last_published_date=date.fromisoformat(video_list[0].video_published_date)
    for obj in video_list:
        current_published_date=date.fromisoformat(obj.video_published_date)
        x_axis.append(i)
        delta=current_published_date-last_published_date
        y_axis.append(delta.days)
        last_published_date=current_published_date
        i+=1

    return x_axis,y_axis


#comments_by_views against video number for a single channel scaled by 1000
def comments_by_views_plot(video_list,sfactor=1000):
    
    i=1
    x_axis=[]
    y_axis=[]

    for obj in video_list:
        r_views=int(obj.video_views)
        views=r_views if r_views!=0 else 1
        x_axis.append(i)
        y_axis.append((int(obj.video_comments)/views)*sfactor)
        i+=1

    return x_axis,y_axis



#likes_by_views against video number for a single channel scaled by 100
def likes_by_views_plot(video_list,sfactor=100):
    
    i=1
    x_axis=[]
    y_axis=[]

    for obj in video_list:
        r_views=int(obj.video_views)
        views=r_views if r_views!=0 else 1
        x_axis.append(i)
        y_axis.append((int(obj.video_likes)/views)*sfactor)
        i+=1

    return x_axis,y_axis



#draw a single line corresponding to a single channel in one chart
def single_line_single_plot(x_axis,y_axis,y_label,legend,title):

    plt.style.use('fivethirtyeight')
    plt.plot(x_axis,y_axis,label=legend)
    plt.xlabel('Video Number')
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#draw multiple lines corresponding to multiple channels in one chart
def multi_line_single_plot(x_axises,y_axises,y_label,legends,title):

    plt.style.use('fivethirtyeight')
    number_of_charts=len(x_axises)
    for graph_number in range(number_of_charts):

        plt.plot(x_axises[graph_number],y_axises[graph_number],label=legends[graph_number])

    
    
    plt.xlabel('Video Number')
    plt.ylabel(y_label)
    plt.title(title)    
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#draw multiple charts
def multi_plot(x_axises,y_axises,y_labels,legends,title):

    plt.style.use('fivethirtyeight')
    fig,(ax1,ax2,ax3)=plt.subplots(nrows=3,ncols=1)

    ax1.plot(x_axises[0],y_axises[0],label=legends[0])
    ax2.plot(x_axises[1],y_axises[1],label=legends[1])
    ax3.plot(x_axises[2],y_axises[2],label=legends[2])

    ax1.legend()
    ax1.set_title(title)
    ax1.set_xlabel('Video Number')
    ax1.set_ylabel(y_labels[0])

    ax2.legend()
    ax2.set_xlabel('Video Number')
    ax2.set_ylabel(y_labels[1])

    ax3.legend()
    ax3.set_xlabel('Video Number')
    ax3.set_ylabel(y_labels[2])
      

    plt.tight_layout()
    plt.show()


#print a table
def table(table_data):
    return tabulate(table_data,headers="firstrow",tablefmt="fancy_grid")