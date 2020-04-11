#!/usr/bin/env python
# coding: utf-8

# # Improve CampusX
# 
# ## Instructions
# 
# 1. You have to submit your solutions before **6:00pm tomorrow**
# 2. The problems that I have given(**except the 1st one**) are problems with which we are also dealing with. So, in a way we are asking for your help through this hackathon.
# 3. To be honest solving even a single question is a big deal in the given time duration. So, please don't get **frustrated** if you are not able to solve even one problem. 
# 4. A request - **don't quit**. Infact **never quit**.
# 5. Marking Scheme for this hackathon is as follows
# **Total Marks=200**
# but, while adding this to your dashboard, your total marks will be divided by a **factor of 10**.
# So, let's say you scored 90 in the hackathon, you dashboard score would be 9
# 6. Top 3 performers will get a **prize**, when we will meet next.Promise:)
# 

# In[2]:


import numpy as np
import pandas as pd

tasks=pd.read_csv('tasks.csv')
batch=pd.read_csv('batch.csv')
batch_task=pd.read_csv('batch_task.csv')
content=pd.read_csv('content.csv')
course=pd.read_csv('course.csv')
evaluation=pd.read_csv('evaluation.csv')
gyan=pd.read_csv('gyan.csv')
link_preview_details=pd.read_csv('link_preview_details.csv')
module=pd.read_csv('module.csv')
myday=pd.read_csv('myday.csv')
url_task=pd.read_csv('url_task.csv')
users=pd.read_csv('users.csv')


# In[ ]:




**Problem 1** : Write a python function which will receive 3 input i.e. batch name, start date and end date and returns the leaderboard(in that date window) of that particular batch with the following pieces of info - Name, Marks(till now)

Note: If no date range is provided, show the leaderboard for the entire duration of the course

**Marks -10**
# In[2]:


# Write your code here

def find_leaderboard(batch_name,start_date=0,end_date=str(pd.datetime.now().date())) :
    
    if start_date==0 :
        start_date=batch[batch['batch_name']==batch_name]['batch_start_date'].values[0]
    
    batch_id=batch[batch['batch_name']==batch_name]['batch_id'].values[0]
    user_data=users[users['batch_id']==batch_id]
    user_id=user_data['user_id'].index.tolist()
    evaluation_points=evaluation[(evaluation['user_id'].isin(user_id)) & (evaluation['evaluation_date']>=start_date) & (evaluation['evaluation_date']<=end_date)].groupby('user_id')['score'].sum().reset_index()
    my_day=myday.dropna()
    my_day_points=my_day[(my_day['user_id'].isin(user_id)) & (my_day['entry_date']>=start_date) & (my_day['entry_date']<=end_date)].groupby('user_id')['entry'].count().reset_index()
    gyan_points=gyan[(gyan['user_id'].isin(user_id)) & (gyan['submission_date']>=start_date) & (gyan['submission_date']<=end_date)].groupby('user_id')['link'].count().reset_index()
    myday_plus_gyan_points=my_day_points.merge(gyan_points,left_on='user_id',right_on='user_id')
    total_score=evaluation_points.merge(myday_plus_gyan_points,left_on='user_id',right_on='user_id')
    leader=user_data.merge(total_score,left_on='user_id',right_on='user_id')[['fname','lname','score','entry','link']]
    
    leader['sum']=leader[['score','entry','link']].sum(axis=1)
    
    return leader.sort_values(['sum'],ascending=False).rename(columns={'fname':'First Name','lname':'Last Name','score':'Task Score','entry':'Myday Score','link':'Gyan Score','sum':'Total Score'}).head(10)
find_leaderboard('Machine Learning Kolkata 2')


# In[ ]:





# **Problem 2**: Write a python function that receives 1 input, batch_name and returns the list of top 10 students who require maximum attention from the teacher.
# 
# **Note**: I know this is kind of abstract, but truly we are facing this problem. Try to come up with a solution/algorithm. 
# 
# **Tip** : Don't just think in terms of marks, also think about things like late submissions, number of submissions, myday etc
# 
# **Tricky scenario**: Aisa bhi ho sakta hai koi student bas shuru me acha perform nai kar raha tha, but ab kar raha hai. So consider dates also.
# 
# **Marks : 50**

# In[3]:


# Write your code here

'''tried to have a window of last 30 days
    and find the students having least score,
    least number of tasks submitted,
    most number of late submissions,
    least number of myday,
    least number of gyan.
'''

from datetime import timedelta

def attention(batch_name) :
    
    batch_id=batch[batch['batch_name']==batch_name]['batch_id'].values[0]
    user_data=users[users['batch_id']==batch_id]
    user_id=user_data['user_id'].index.tolist()
    
    start_date=str(pd.datetime.now().date()-timedelta(days=30))
    end_date=str(pd.datetime.now().date())
    
    task_score=evaluation[(evaluation['user_id'].isin(user_id)) & (evaluation['evaluation_date']>=start_date) & (evaluation['evaluation_date']<=end_date)].groupby('user_id')['score'].sum().reset_index().sort_values('score').rename(columns={'score':'Marks Obtained'})
    
    number_of_tasks=evaluation[(evaluation['user_id'].isin(user_id)) & (evaluation['evaluation_date']>=start_date) & (evaluation['evaluation_date']<=end_date)].groupby('user_id')['score'].count().reset_index().sort_values('score').rename(columns={'score':'Number of Tasks Submited'})
    number_of_late_submissions=evaluation[(evaluation['user_id'].isin(user_id)) & (evaluation['evaluation_date']>=start_date) & (evaluation['evaluation_date']<=end_date) & (evaluation['late']==1)].groupby('user_id')['late'].count().reset_index().sort_values('late').rename(columns={'late':'Number of Late Submissions'})
    
    task_status=number_of_tasks.merge(number_of_late_submissions,left_on='user_id',right_on='user_id')
    
    my_day=myday.dropna()
    number_of_my_day=my_day[my_day['user_id'].isin(user_id)].groupby('user_id')['entry'].count().reset_index().sort_values('entry').rename(columns={'entry':'Number of Myday'})
    
    number_of_gyan=gyan[gyan['user_id'].isin(user_id)].groupby('user_id')['link'].count().reset_index().sort_values('link').rename(columns={'link':'Number of Gyan'})
    
    my_day_plus_gyan=number_of_my_day.merge(number_of_gyan,left_on='user_id',right_on='user_id')
    
    status=task_status.merge(my_day_plus_gyan,left_on='user_id',right_on='user_id')
    
    penultimate_data=data=task_score.merge(status,left_on='user_id',right_on='user_id')
    
    ultimate_data=user_data.merge(penultimate_data,left_on='user_id',right_on='user_id')[['user_id','fname','lname','Marks Obtained','Number of Tasks Submited','Number of Late Submissions','Number of Myday','Number of Gyan']].set_index('user_id').sort_values(['Marks Obtained','Number of Tasks Submited','Number of Late Submissions','Number of Myday','Number of Gyan'],ascending=[True,True,False,True,True]).rename(columns={'fname':'First Name','lname':'Last Name'}).head(10)
    
    return ultimate_data

attention('Machine Learning Kolkata 1')


# **Problem 3**: Write a python function that will take batch name and a date range as input and outputs the most consistent student in that given daterange and batch
# 
# **Note**: Come up with your definition of consistency
# 
# **Marks - 20** 

# In[4]:


# most number of task submissions(top 10) and  most number of mydays(top 10) and most number of gyan(top 10)

def most_consistent(batch_name,start_date=0,end_date=str(pd.datetime.now().date())) :
    
    if start_date==0 :
        start_date=batch[batch['batch_name']==batch_name]['batch_start_date'].values[0]
    
    batch_id=batch[batch['batch_name']==batch_name]['batch_id'].values[0]
    user_data=users[users['batch_id']==batch_id]
    user_id=user_data['user_id'].index.tolist()
    
    evaluation_count=evaluation[(evaluation['user_id'].isin(user_id)) & (evaluation['evaluation_date']>=start_date) & (evaluation['evaluation_date']<=end_date)].groupby('user_id')['score'].count().sort_values(ascending=False).head(10).index.tolist()

    my_day=myday.dropna()
    my_day_count=my_day[(my_day['user_id'].isin(user_id)) & (my_day['entry_date']>=start_date) & (my_day['entry_date']<=end_date)].groupby('user_id')['entry'].count().sort_values(ascending=False).head(10).index.tolist()
    
    gyan_count=gyan[(gyan['user_id'].isin(user_id)) & (gyan['submission_date']>=start_date) & (gyan['submission_date']<=end_date)].groupby('user_id')['submission_date'].count().sort_values(ascending=False).head(10).index.tolist()
    
    most_consistent_students=list(set(evaluation_count).intersection(set(my_day_count)).intersection(set(gyan_count)))
    
    return users[users['user_id'].isin(most_consistent_students)][['user_id','fname','lname']].set_index('user_id').rename(columns={'fname':'First Name','lname':'Last Name'})

most_consistent("Machine Learning HIT 1")


# **Problem 4**: Find the best student across batches
# 
# **Marks - 20**

# In[5]:


number_of_evaluations=evaluation.groupby('user_id')['score'].count().reset_index().rename(columns={'score':'Number of Tasks Submitted'})
score_of_evaluations=evaluation.groupby('user_id')['score'].sum().reset_index().rename(columns={'score':'Task Scores'})
scores=number_of_evaluations.merge(score_of_evaluations,left_on='user_id',right_on='user_id')

not_late=evaluation[evaluation['late']==0]
number_of_not_late=not_late.groupby('user_id')['late'].count().reset_index().rename(columns={'late':'Number of Tasks on Time'})

scores_not_late=scores.merge(number_of_not_late,left_on='user_id',right_on='user_id')

my_day=myday.dropna()
number_of_my_day=my_day.groupby('user_id')['entry'].count().reset_index().rename(columns={'entry':'Number of Myday'})

number_of_gyan=gyan.groupby('user_id')['link'].count().reset_index().rename(columns={'link':'Number of Gyan'})

my_day_gyan=number_of_my_day.merge(number_of_gyan,left_on='user_id',right_on='user_id')

scores_not_late_my_day_gyan=scores_not_late.merge(my_day_gyan,left_on='user_id',right_on='user_id')

final_data=users.merge(scores_not_late_my_day_gyan,left_on='user_id',right_on='user_id')[['user_id','batch_id','fname','lname','Number of Tasks Submitted','Task Scores','Number of Tasks on Time','Number of Myday','Number of Gyan']].set_index('user_id').rename(columns={'fname':'First Name','lname':'Last Name'})
final_data.sort_values(['Number of Tasks Submitted','Task Scores','Number of Tasks on Time','Number of Myday','Number of Gyan'],ascending=[False,False,False,False,False]).drop_duplicates('batch_id').head(1)


# **Problem 5** : Write a function/piece of analysis that can compare the performance of 2 batches on the whole
# 
# **Note**: Again Abstract
# 
# **Note 2**: Will be judging you a lot on the basis of this.
# 
# **Note 3**: You can get an instant internship under us, if can apply the right thought process to this problem
# 
# **Marks - 50**

# In[5]:


# Write your code here

data=users[(users['batch_id']==1) | (users['batch_id']==3)][['user_id','batch_id','fname','lname']]
user_id=data['user_id'].index.tolist()

evaluation_count=evaluation[evaluation['user_id'].isin(user_id)].groupby('user_id')['score'].count().reset_index().rename(columns={'score':'Number of Tasks Submitted'})
evaluation_score=evaluation[evaluation['user_id'].isin(user_id)].groupby('user_id')['score'].sum().reset_index().rename(columns={'score':'Task Scores'})
evaluation_data=evaluation_count.merge(evaluation_score,left_on='user_id',right_on='user_id')

not_late=evaluation[evaluation['late']==0]
number_of_not_late=not_late.groupby('user_id')['late'].count().reset_index().rename(columns={'late':'Number of Tasks on Time'})

evaluation_data_not_late=evaluation_data.merge(number_of_not_late,left_on='user_id',right_on='user_id')

my_day=myday.dropna()
number_of_my_day=my_day.groupby('user_id')['entry'].count().reset_index().rename(columns={'entry':'Number of Myday'})

number_of_gyan=gyan.groupby('user_id')['link'].count().reset_index().rename(columns={'link':'Number of Gyan'})

my_day_gyan=number_of_my_day.merge(number_of_gyan,left_on='user_id',right_on='user_id')

evaluation_data_not_late_my_day_gyan=evaluation_data_not_late.merge(my_day_gyan,left_on='user_id',right_on='user_id')

final_data=users.merge(evaluation_data_not_late_my_day_gyan,left_on='user_id',right_on='user_id')[['batch_id','Number of Tasks Submitted','Task Scores','Number of Tasks on Time','Number of Myday','Number of Gyan']]
final_data_with_batch_name=final_data.merge(batch,left_on='batch_id',right_on='batch_id')[['batch_id','batch_name','Number of Tasks Submitted','Task Scores','Number of Tasks on Time','Number of Myday','Number of Gyan']]

final_data_with_batch_name.pivot_table(index=['batch_id','batch_name'],aggfunc='sum')[['Number of Tasks Submitted','Task Scores','Number of Tasks on Time','Number of Myday','Number of Gyan']]


# **Problem 6** : Surprise us
# 
# **Description**: Find something(point/points of analysis) that might surprise us
# 
# **Marks - 50**

# In[37]:


# Shy Students
''' tTop 10 students who have submitted the least amount of myday and gyan
    within a specified date range, if no date is provided,
    the range should be between the start of his/her batch and today's date
    
    input given : batch name
    output : list of inactive students of that batch
'''

def find_shy(batch_name,start_date=0,end_date=str(pd.datetime.now().date())) :
    
    if start_date==0 :
           start_date=batch[batch['batch_name']==batch_name]['batch_start_date'].values[0]
    
    batch_id=batch[batch['batch_name']==batch_name]['batch_id'].values[0]
    user_data=users[users['batch_id']==batch_id]
    user_id=user_data['user_id'].index.tolist()
    
    my_day=myday.dropna()
    
    shy_day=my_day[(my_day['user_id'].isin(user_id)) & (my_day['entry_date']>=start_date) & (my_day['entry_date']<=end_date)].groupby('user_id')['entry'].count().sort_values().reset_index()
    
    shy_gyan=gyan[(gyan['user_id'].isin(user_id)) & (gyan['submission_date']>=start_date) & (gyan['submission_date']<=end_date)].groupby('user_id')['link'].count().sort_values().reset_index()
    
    shy=shy_day.merge(shy_gyan,left_on='user_id',right_on='user_id')
    shy['total']=shy[['entry','link']].sum(axis=1)
    shy=shy.head(10)
    
    final_data=users.merge(shy,left_on='user_id',right_on='user_id')[['user_id','fname','lname','entry','link','total']].rename(columns={'user_id':'User ID','fname':'First Name','lname':'Last Name','entry':'Number of Myday','link':'Number of Gyan','total':'Total Number of Myday and Gyan'}).sort_values('Total Number of Myday and Gyan').set_index('User ID')
    
    return final_data

find_shy('Machine Learning Kolkata 2')


# In[ ]:




