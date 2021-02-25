#!/usr/bin/env python
# coding: utf-8

# In[19]:


import socket


# In[20]:


word_length = 60
control_bits = [i for i in range(1, word_length + 1) if not i & (i - 1)]


# In[21]:


def string2bits(s = ''):
    return [bin(ord(x))[2 : ].zfill(8) for x in s]

def bits2string(b = None):
    return ''.join([chr(int(x, 2)) for x in b])


# In[12]:


host = "127.0.0.1"
port = 8
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
sock.send("palindrom".encode())
result = sock.recv(1024).decode()
sock.close()
print("Получено:", result)


# In[ ]:




