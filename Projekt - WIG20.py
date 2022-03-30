#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

df = pdr.get_data_yahoo('SPOT', '2021-01-01')
df.head()
print(df)

df['śr. krocząca 10'] = df['Close'].rolling(10).mean()
df['śr. krocząca 15'] = df['Close'].rolling(15).mean()
df['śr. krocząca 20'] = df['Close'].rolling(20).mean()
df.tail()


# In[2]:


plt.figure(figsize=(20,10))
plt.plot(df['Close'], label='Spotify CLOSE')
plt.legend()


# In[3]:


plt.figure(figsize=(20,10))
plt.plot(df['Close'], label='Spotify CLOSE')
plt.plot(df['śr. krocząca 10'], label='śr. krocząca 10')
plt.plot(df['śr. krocząca 15'], label='śr. krocząca 15')
plt.plot(df['śr. krocząca 20'], label='śr. krocząca 20')
plt.legend(loc=2)


# In[ ]:





# In[ ]:





# In[ ]:




