
# coding: utf-8

# In[368]:


import pandas as pd

in_file = 'C:/McD/Covid/Covid FAQ.xlsx'
sheet_tab_key = 'Sheet1'
sheet_tab_res = 'Sheet1'


# In[369]:


xls_in = pd.ExcelFile(in_file)
df_key = pd.read_excel(xls_in, sheet_tab_key)
df_res = pd.read_excel(xls_in, sheet_tab_res)

df_res = df_res.rename(columns = {"Unnamed: 5": "Resolution_Text", })

#df_key['Sales activity no.']
#df_res['Resolution_Text']
df_res.dtypes

df_key.shape
df_res.shape
#df_res
#print(df_res)

# In[370]:


df_res_t1 = df_res.drop_duplicates(subset=['Sales activity no.', 'Resolution_Text'])

print(type(df_res_t1['Current Date']))
#df_res_t1['date_time_comb'] = df_res_t1['Current Date'].map(str) + df_res_t1['Time']

#df_res_t1['date_time_num'] = df_res_t1[['date_time_comb']].apply(lambda x: x[0].timestamp(), axis=1).astype(int)
df_res_t1.head()


# In[371]:


import datetime
#dates = pd.to_datetime(pd.Series(df_res_t1['Current Date']), format = '%Y%m%d')
#dates.apply(lambda x: x.strftime('%Y-%m-%d'))
#df_res_t1['Time']= pd.to_datetime(df_res_t1['Time']) 
#datetime.Current Date.combine(datetime.df_res_t1['Current Date'], 
                          #datetime.df_res_t1['Time'])
#df_res_t1.dtypes
#dates


# In[372]:


#df_res_t1['Time_New'] = pd.to_datetime(df_res_t1['Time'], format='%H:%M').dt.time
#pd.to_datetime(df_res_t1['Current Date'] + df_res_t1['Time'])
df_res_t1['date_time']=pd.to_datetime(df_res_t1['Current Date'].astype(str)+' '+df_res_t1['Time'].astype(str))


# In[373]:


df_res_t1.head()


# In[434]:


df_res_t1.sort_values(by=['date_time'])


# In[375]:


df_res_t1_new=df_res_t1.drop(['Text ID', 'Language Key', 'Current Date','Time'], axis=1)


# In[376]:


df_res_t1_new.head()


# In[377]:


df_res_t1_new.groupby('Sales activity no.')['Resolution_Text'].apply(' '.join).reset_index()


# In[378]:


df_res_join=df_res_t1_new.groupby('Sales activity no.')['Resolution_Text'].apply(' '.join).reset_index()


# In[379]:


df_res_join_op = df_res_join.to_excel (r'C:/Users/PRANABGHOSH/Desktop/work/Python SPSS Cognos/NLP/df_res_join_op.xlsx', index = None, header=True)


# In[380]:


df_key.groupby('Sales activity no.')


# In[381]:


df_key.columns


# In[1]:


# df_key.head()


# In[383]:


Final_DF = pd.merge(df_key[['Sales activity no.','Reason','Reason Description','Resolution Detail','Created On','Created At','End Date','End Time','Start Date']],
                 df_res_join[['Sales activity no.', 'Resolution_Text']],
                 on='Sales activity no.')


# In[384]:


Final_DF.columns


# In[385]:


Final_DF.head()


# In[386]:


Final_DF['mStart_date'] = pd.to_datetime(Final_DF['Start Date'])


# In[387]:


Final_DF['mEnd_date'] = pd.to_datetime(Final_DF['End Date'])


# In[388]:


Final_DF.dtypes 


# In[389]:


Final_DF['Day_Diff'] = Final_DF['mEnd_date']-Final_DF['mStart_date']


# In[390]:


Final_DF.head()


# In[391]:


Final_DF.dtypes


# In[392]:


Final_DF['Day_Diff'] = Final_DF['Day_Diff'].astype('timedelta64[D]')


# In[393]:


Final_DF.head()


# In[394]:


Final_DF['Day_Diff'] = Final_DF['Day_Diff'] + 1


# In[395]:


Final_DF.head()


# In[396]:


# Final_DF['Reason'].replace(Final_DF['Reason Description'],'Hello')


# In[397]:


Final_DF.head()


# In[427]:


def Cluster_Summary (filter_name, num_of_cluster, file_name):
    Final_DF_Ord_Min=Final_DF[Final_DF['Reason Description'].str.contains (filter_name)]
    Final_DF_Ord_Min.head()
    
    from sklearn.feature_extraction.text import CountVectorizer

    #count_vect = CountVectorizer(analyzer='word')
    count_vect = CountVectorizer()
    #file_name = file_name

    X_counts = count_vect.fit_transform(Final_DF_Ord_Min['Resolution_Text'])
    print(X_counts.shape)
    print(count_vect.get_feature_names())
    
    from sklearn.cluster import KMeans

    num_clusters = num_of_cluster

    km = KMeans(n_clusters=num_clusters)

    get_ipython().run_line_magic('time', 'km.fit(X_counts)')

    clusters = km.labels_.tolist()
    
    
    import pylab as pl
    Nc = range(1, 20)

    kmeans = [KMeans(n_clusters=i) for i in Nc]

    kmeans

    score = [kmeans[i].fit(X_counts).score(X_counts) for i in range(len(kmeans))]

    score

    pl.plot(Nc,score)

    pl.xlabel('Number of Clusters')

    pl.ylabel('Score')

    pl.title('Elbow Curve')

    pl.show()
    
    Final_DF_Ord_Min['Clusters']=clusters
    Final_DF_Ord_Min_Cluster = Final_DF_Ord_Min.groupby('Clusters')
    #Final_DF_Ord_Min.head()
    
    Final_DF_Ord_Min_Cluster = Final_DF_Ord_Min.groupby('Clusters')
    
    Final_DF_Ord_Min__Cluster_Aggregate = Final_DF_Ord_Min_Cluster.agg({'Sales activity no.':'count', 'Day_Diff':'mean'})        .rename(columns={'Sales activity no.':'Sales activity count','Day_Diff':'Average Day Diff'})        .reset_index()
    
    Final_DF_Ord_Min__Cluster_Aggregate['Average Day Diff'] = round(Final_DF_Ord_Min__Cluster_Aggregate['Average Day Diff'],2)
    
    Final_DF_Ord_Min__Cluster_Aggregate = Final_DF_Ord_Min__Cluster_Aggregate.to_excel (r'C:/Users/PRANABGHOSH/Desktop/work/Python SPSS Cognos/NLP' + file_name+'.xlsx', index = None, header=True)
    
    return Final_DF_Ord_Min__Cluster_Aggregate


# In[433]:


Cluster_Summary('Minimum Value', 3, 'Final_Minimum_Value_Agg')


# In[398]:


#Final_DF_Duplicate=Final_DF[Final_DF['Reason Description'].str.contains ('Dup. Order Check')]
#Final_DF_Minimum=Final_DF[Final_DF['Reason Description'].str.contains ('Minimum Value')]
Final_DF_Ord_Min=Final_DF[Final_DF['Reason Description'].str.contains ('Dup. Order Check')]
#df[df['model'].str.contains('ac')]


# In[399]:


#Final_DF_Maximum.head()
#Final_DF_Duplicate.head()
#Final_DF_Minimum.head()
Final_DF_Ord_Min.head()


# In[400]:


#Final_DF_output_1 = Final_DF.to_excel (r'C:\DataScience\SP\Final_DF_output_1.xlsx', index = None, header=True)


# In[401]:


from sklearn.feature_extraction.text import CountVectorizer

#count_vect = CountVectorizer(analyzer='word')
count_vect = CountVectorizer()
#X_counts = count_vect.fit_transform(Final_DF_Maximum['Resolution_Text'])
#X_counts = count_vect.fit_transform(Final_DF_Duplicate['Resolution_Text'])
#X_counts = count_vect.fit_transform(Final_DF_Minimum['Resolution_Text'])
X_counts = count_vect.fit_transform(Final_DF_Ord_Min['Resolution_Text'])
print(X_counts.shape)
print(count_vect.get_feature_names())

#tfidf_transformer = TfidfTransformer().fit(messages_bow)


# In[402]:


#X_counts.toarray()[0].max()


# In[403]:


#X_counts.toarray()


# In[404]:


#X_counts.toarray().max()


# In[405]:


#Final_DF['Feature']=list(X_counts)


# In[406]:


from sklearn.cluster import KMeans

num_clusters = 2

km = KMeans(n_clusters=num_clusters)

get_ipython().run_line_magic('time', 'km.fit(X_counts)')

clusters = km.labels_.tolist()


# In[407]:


import pylab as pl
Nc = range(1, 20)

kmeans = [KMeans(n_clusters=i) for i in Nc]

kmeans

score = [kmeans[i].fit(X_counts).score(X_counts) for i in range(len(kmeans))]

score

pl.plot(Nc,score)

pl.xlabel('Number of Clusters')

pl.ylabel('Score')

pl.title('Elbow Curve')

pl.show()


# In[408]:


pl.show()


# In[409]:


#Final_DF_Maximum['Clusters']=clusters
#Final_DF_Duplicate['Clusters']=clusters
#Final_DF_Minimum['Clusters']=clusters
Final_DF_Ord_Min['Clusters']=clusters


# In[410]:


#Final_DF=Final_DF.drop(['Feature'], axis=1)


# In[411]:


#Final_DF_Maximum.head()
#Final_DF_Duplicate['Clusters']=clusters
#Final_DF_Minimum.head()
Final_DF_Ord_Min.head()


# In[412]:


# Final_DF_Ord_Min_Output = Final_DF_Ord_Min.to_excel (r'C:/Users/PRANABGHOSH/Desktop/work/Python SPSS Cognos/NLP/Final_DF_Ord_Min_Output_Pranab.xlsx', index = None, header=True)


# In[413]:


#Final_DF_Maximum = Final_DF_Maximum.groupby('Clusters')
#Final_DF_Maximum_Aggregate=Final_DF_Maximum.agg([ 'count'])
#Final_DF_Duplicate = Final_DF_Duplicate.groupby('Clusters')
#Final_DF_Duplicate_Aggregate=Final_DF_Duplicate.agg([ 'count'])
#Final_DF_Minimum = Final_DF_Minimum.groupby('Clusters')
#Final_DF_Minimum_Aggregate=Final_DF_Minimum.agg([ 'count'])
Final_DF_Ord_Min_Cluster = Final_DF_Ord_Min.groupby('Clusters')
#Final_DF_Ord_Min_Aggregate=Final_DF_Ord_Min.agg([ 'count'])


# In[414]:


Final_DF_Ord_Min.columns


# In[415]:


Final_DF_Ord_Min__Cluster_Aggregate = Final_DF_Ord_Min_Cluster.agg({'Sales activity no.':'count', 'Day_Diff':'mean'})        .rename(columns={'Sales activity no.':'Sales activity count','Day_Diff':'Average Day Diff'})        .reset_index()


# In[416]:


Final_DF_Ord_Min__Cluster_Aggregate


# In[417]:


type(Final_DF_Ord_Min__Cluster_Aggregate)


# In[418]:


Final_DF_Ord_Min__Cluster_Aggregate['Average Day Diff'] = round(Final_DF_Ord_Min__Cluster_Aggregate['Average Day Diff'],2)


# In[419]:


Final_DF_Ord_Min__Cluster_Aggregate


# In[365]:


Final_DF_Ord_Min__Cluster_Aggregate = Final_DF_Ord_Min__Cluster_Aggregate.to_excel (r'C:/Users/PRANABGHOSH/Desktop/work/Python SPSS Cognos/NLP/Final_Dup_Order_Check_Agg_Pranab.xlsx', index = None, header=True)

