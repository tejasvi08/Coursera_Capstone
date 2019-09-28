#!/usr/bin/env python
# coding: utf-8

# In[15]:


def get_cell(element):
    cells = element.find_all('td')
    row = []
    
    for cell in cells:
        if cell.a:            
            if (cell.a.text):
                row.append(cell.a.text)
                continue
        row.append(cell.string.strip())
        
    return row


# In[16]:


def get_row():    
    data = []  
    
    for tr in wiki_table.find_all('tr'):
        row = get_cell(tr)
        if len(row) != 3:
            continue
        data.append(row)        
    
    return data


# In[17]:


data = get_row()
columns = ['Postcode', 'Borough', 'Neighbourhood']
df = pd.DataFrame(data, columns=columns)
df.head()


# In[18]:


df.shape


# In[19]:


df1 = df[df.Borough != 'Not assigned']
df1 = df1.sort_values(by=['Postcode','Borough'])

df1.reset_index(inplace=True)
df1.drop('index',axis=1,inplace=True)

df1.head()


# In[20]:


df_postcodes = df1['Postcode']
df_postcodes.drop_duplicates(inplace=True)
df2 = pd.DataFrame(df_postcodes)
df2['Borough'] = '';
df2['Neighbourhood'] = '';


df2.reset_index(inplace=True)
df2.drop('index', axis=1, inplace=True)
df1.reset_index(inplace=True)
df1.drop('index', axis=1, inplace=True)

for i in df2.index:
    for j in df1.index:
        if df2.iloc[i, 0] == df1.iloc[j, 0]:
            df2.iloc[i, 1] = df1.iloc[j, 1]
            df2.iloc[i, 2] = df2.iloc[i, 2] + ',' + df1.iloc[j, 2]
            
for i in df2.index:
    s = df2.iloc[i, 2]
    if s[0] == ',':
        s =s [1:]
    df2.iloc[i,2 ] = s


# In[21]:


df2.shape


# In[22]:


df2['Latitude'] = '0';
df2['Longitude'] = '0';

df_geo = pd.read_csv('Geospatial_Coordinates.csv')
df_geo.head()


# In[23]:


for i in df2.index:
    for j in df_geo.index:
        if df2.iloc[i, 0] == df_geo.iloc[j, 0]:
            df2.iloc[i, 3] = df_geo.iloc[j, 1]
            df2.iloc[i, 4] = df_geo.iloc[j, 2]
            
df2.head()


# In[ ]:


toronto_map = folium.Map(location=[43.65, -79.4], zoom_start=12)

X = df3['Latitude']
Y = df3['Longitude']
Z = np.stack((X, Y), axis=1)

kmeans = KMeans(n_clusters=4, random_state=0).fit(Z)

clusters = kmeans.labels_
colors = ['red', 'green', 'blue', 'yellow']
df3['Cluster'] = clusters

for latitude, longitude, borough, cluster in zip(df3['Latitude'], df3['Longitude'], df3['Borough'], df3['Cluster']):
    label = folium.Popup(borough, parse_html=True)
    folium.CircleMarker(
        [latitude, longitude],
        radius=5,
        popup=label,
        color='black',
        fill=True,
        fill_color=colors[cluster],
        fill_opacity=0.7).add_to(toronto_map)  

toronto_map

