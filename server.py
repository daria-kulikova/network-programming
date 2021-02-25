#!/usr/bin/env python
# coding: utf-8

# In[1]:


import socket, string


# In[2]:


def do_something(x):
    return "good string"


# In[3]:


host = "127.0.0.1"
port = 8
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.bind((host, port))


# In[ ]:


while True:
    print("Слушаю порт " + str(port))
    srv.listen(True)
    sock, adr = srv.accept()
    while True:
        msg = sock.recv(1024).decode() # 1024 - число байт в очередной порции
        if not msg:
            break
        print("Получено от %s:%s:" % adr, msg)
        ans = do_something(msg)
        print("Отправлено %s:%s:" % adr, ans)
        sock.send(ans.encode())
    sock.close()


# In[ ]:




