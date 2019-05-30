# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 10:47:06 2019

@author: LENOVO
"""
from flask import flash
import facebook
import instagram
from datetime import datetime
import pandas as pd
def get_fb_token(stoken):
    graph = facebook.GraphAPI(stoken)
    app_id = '373526949908614'
    app_secret = '363a948596918281544a628c57802c7a'
    extended_token = graph.extend_access_token(app_id, app_secret)
    return extended_token['access_token']
def get_fb_data(stoken):
    try:
        page_token = stoken
        graph = facebook.GraphAPI(access_token=page_token, version="3.2")
        page_id=405667483335062
        imageheadercolumns = ['type','created_time','object_id','id']
        videoheadercolumns = ['type','name','created_time','id']
        posts_25 = graph.get_object(id=page_id,fields='posts.fields(type, name, created_time, object_id)')
        vidataarr = []
        virowarr = []
        imdataarr = []
        imrowarr = []
        for i in range(len(posts_25) - 1):
            for j in range(len(posts_25['posts']['data'])):
                if(posts_25['posts']['data'][j]['type'] == 'video'):
                    for vi in videoheadercolumns:
                        virowarr.append(posts_25['posts']['data'][j][vi])
                    vidataarr.append(virowarr)
                    virowarr = []
                else:
                    for im in imageheadercolumns:
                        imrowarr.append(posts_25['posts']['data'][j][im])
                    imdataarr.append(imrowarr)
                    imrowarr = []
        videodata = pd.DataFrame(vidataarr,columns = videoheadercolumns)
        imagedata = pd.DataFrame(imdataarr,columns = imageheadercolumns)

        posts_2019 = graph.get_all_connections(id=page_id,connection_name='posts',fields='type, name, created_time, object_id',since=datetime(2019, 1, 1, 0, 0, 0))
        videopost2019row = []
        videopost2019data = []
        imagepost2019row = []
        imagepost2019data = []
        for ind, post in enumerate(posts_2019):
             if(post['type'] == 'video'):
                for vi in videoheadercolumns:
                    videopost2019row.append(post[vi])
                videopost2019data.append(videopost2019row)
                videopost2019row = []
             else:
                for im in imageheadercolumns:
                    imagepost2019row.append(post[im])
                imagepost2019data.append(imagepost2019row)
                imagepost2019row = []
        videodata2019 = pd.DataFrame(videopost2019data,columns = videoheadercolumns)
        imagedata2019 = pd.DataFrame(imagepost2019data,columns = imageheadercolumns)
        recent_2_posts = graph.get_object(id=page_id,fields='posts.fields(type, name, created_time, object_id)')

        total_post_1 = recent_2_posts['posts']['data']
        commentsdataarr = []
        commentsdataheader = ['created_time','message','id']
        commentsdata = []
        reactionsdataarr = []
        reactionsdataheader = ['id','name','type']
        reactionsdata = []
        for i in range(len(total_post_1)):
            posts = recent_2_posts['posts']['data'][i]
            postdata = graph.get_object(id=posts['id'], fields="""message, comments.summary(total_count), reactions.summary(total_count), shares""")
            for j in range(len(postdata['comments']['data'])):
                for c in commentsdataheader:
                    commentsdataarr.append(postdata['comments']['data'][j][c])
                commentsdata.append(commentsdataarr)
                commentsdataarr = []
            for k in range(len(postdata['reactions']['data'])):
                for r in reactionsdataheader:
                    reactionsdataarr.append(postdata['reactions']['data'][k][r])
                reactionsdata.append(reactionsdataarr)
                reactionsdataarr = []
        comments = pd.DataFrame(commentsdata,columns = commentsdataheader)
        reactions = pd.DataFrame(reactionsdata,columns = reactionsdataheader)      
        def checkKey(dict, key): 
      
            if key in dict.keys(): 
                return "Present" 
            else: 
                return "Not present"
        activity_insightsheaders = ['name','period','values','title','description','id']
        activitiesheaders = ['name','period','likes','comments','title','description','id']
        activityrow = []
        activitydata = []
        valueheaders = ['like','comment']
        for i in range(len(total_post_1)):
            posts = recent_2_posts['posts']['data'][i]
            Activity_insights = graph.get_connections(id=posts['id'],
                                                 connection_name='insights',
                                                 metric='post_activity_by_action_type',
                                                 date_preset='yesterday',
                                                 period='lifetime',
                                                 show_description_from_api_doc=True)

            for j in range(len(Activity_insights['data'])):
                for a in activity_insightsheaders:
                    if a == 'values':
                        for v in valueheaders:
                            if not Activity_insights['data'][j][a][0]['value']:
                                activityrow.append(None)
                            else:
                                if checkKey(Activity_insights['data'][j][a][0]['value'],v) == 'Not present':
                                    activityrow.append(None)
                                else:
                                    activityrow.append(Activity_insights['data'][j][a][0]['value'][v])
                    else:
                        activityrow.append(Activity_insights['data'][j][a])
            activitydata.append(activityrow)
            activityrow = []
        activityinsights = pd.DataFrame(activitydata,columns = activitiesheaders)
        video_insights = graph.get_object(id=page_id,fields='videos{video_insights}')
        videoinsightsheaders = ['name','period','values','title','description','id']
        videorealheaders = ['name','period','page_owned','not_monetizable','like/love','comment','title','description','id']
        value = {'page_owned','not_monetizable','like','love'}
        vidarr = []
        vidinsights = []
        for i in range(len(video_insights['videos']['data'][0]['video_insights']['data'])):
            for v in videoinsightsheaders:
                if(v == 'values'):
                    if type(video_insights['videos']['data'][0]['video_insights']['data'][i][v][0]['value']) is dict:
                        if bool(video_insights['videos']['data'][0]['video_insights']['data'][i][v][0]['value']) == True:
                            for va in value:
                                if checkKey(video_insights['videos']['data'][0]['video_insights']['data'][i][v][0]['value'],va) == 'Not present':
                                    vidarr.append('')
                                else:
                                    vidarr.append(video_insights['videos']['data'][0]['video_insights']['data'][i][v][0]['value'][va])
                    else:
                        vidarr.append('')
                else:
                    vidarr.append(video_insights['videos']['data'][0]['video_insights']['data'][i][v])
            vidinsights.append(vidarr)
            vidarr = []
        vidreal = []
        for j in range(len(vidinsights)):
            if(len(vidinsights[j]) == 9):
                vidreal.append(vidinsights[j])
        videoinsights = pd.DataFrame(vidreal,columns = videorealheaders)      
        writer = pd.ExcelWriter('DataInsights.xlsx')
        videoinsights.to_excel(writer,'Insights',index=False)
        comments.to_excel(writer,'Comments',index=False)
        reactions.to_excel(writer,'Reactions',index=False)
        videodata.to_excel(writer,'AllVideos',index=False)
        imagedata.to_excel(writer,'AllImages',index=False)
        videodata2019.to_excel(writer,'Videos2019',index=False)
        imagedata2019.to_excel(writer,'Images2019',index=False)
        activityinsights.to_excel(writer,'Activity_Insights',index=False)
        writer.save()
        return 'Data has been saved!!'
    except:
        return 'Short Lived Access Token has Expired!!Please go to Facebook for developers to get new one'
# for i in range(len(total_post_1)):
#     posts = recent_2_posts['posts']['data'][i]
#     engagement = graph.get_connections(id=posts['id'],connection_name='insights',metric='post_engaged_fan',
#                                                   date_preset='yesterday',
#                                                   period='lifetime',
#                                                   show_description_from_api_doc=True)
#     print(engagement['data'])
#     engagementheaders = ['name','period','values','title','description','id']
#     for j in range(len(engagement['data'])):
#          for  in activity_insightsheaders:
#             if a == 'values':
#                 for v in valueheaders:
#                     if not Activity_insights['data'][j][a][0]['value']:
#                         activityrow.append(None)
#                     else:
#                         if checkKey(Activity_insights['data'][j][a][0]['value'],v) == 'Not present':
#                             activityrow.append(None)
#                         else:
#                             activityrow.append(Activity_insights['data'][j][a][0]['value'][v])
#             else:
#                 activityrow.append(Activity_insights['data'][j][a])
#     activitydata.append(activityrow)
#     activityrow = []
# activityinsights = pd.DataFrame(activitydata,columns = activitiesheaders)



# print(post_1_activity_insights)

# #emoji count



# post_1_activity_insights = graph.get_connections(id=post_1['id'],
#                                                  connection_name='insights',
#                                                  metric='post_reactions_by_type_total',
#                                                  date_preset='yesterday',
#                                                  period='lifetime',
#                                                  show_description_from_api_doc=True)

# print(post_1_activity_insights)

# #like count


# post_1_activity_insights = graph.get_connections(id=post_1['id'],
#                                                  connection_name='insights',
#                                                  metric='post_reactions_like_total',
#                                                  date_preset='yesterday',
#                                                  period='lifetime',
#                                                  show_description_from_api_doc=True)

# print(post_1_activity_insights)



# #photo view count
# post_1_activity_insights = graph.get_connections(id=post_1['id'],
#                                                  connection_name='insights',
#                                                  metric='post_clicks_by_type',
#                                                  date_preset='yesterday',
#                                                  period='lifetime',
#                                                  show_description_from_api_doc=True)

# print(post_1_activity_insights)

# #post activity
# post_1_activity_insights = graph.get_connections(id=post_1['id'],
#                                                  connection_name='insights',
#                                                  metric='post_activity',
#                                                  date_preset='yesterday',
#                                                  period='lifetime',
#                                                  show_description_from_api_doc=True)

# print(post_1_activity_insights)

# #action type
# post_1_activity_insights = graph.get_connections(id=post_1['id'],
#                                                  connection_name='insights',
#                                                  metric='post_activity_by_action_type_unique',
#                                                  date_preset='last_3d',
#                                                  period='lifetime',
#                                                  show_description_from_api_doc=True)

# print(post_1_activity_insights)


# post_1_activity_insights = graph.get_connections(id=page_id,
#                                                  connection_name='insights',
#                                                  metric='page_cta_clicks_by_age_gender_logged_in_unique',
#                                                  date_preset='',
#                                                  period='day',
#                                                  show_description_from_api_doc=False)

# print(post_1_activity_insights)

# # count of fans and other
# page_impressions = graph.get_connections(id=page_id,
                                       
#                                          connection_name='insights',
#                                          metric='page_content_activity_by_action_type_unique',
#                                          date_preset='yesterday',
#                                          period='week',
#                                          show_description_from_api_doc=False
#                                          )
# print(page_impressions)


# #instagram
# page_impressions = graph.get_connections(id=insta_id,
                                       
#                                          connection_name='media',
#                                          metric='followers_count',
                                         
#                                          )
# print(page_impressions)





