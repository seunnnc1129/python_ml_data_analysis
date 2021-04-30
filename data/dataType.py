#!/usr/bin/env python
# coding: utf-8

# In[3]:


# 변수 = 값/데이터
x = 1


# In[4]:


print(x)


# In[5]:


y = 3


# In[6]:


y = 11


# In[7]:


print(y)


# In[8]:


# int, float
x = 15
print(type(x))


# In[9]:


y = 9.5
print(type(y))


# In[10]:


a = 9
b = 5

print(a + b)
print(a - b)
print(a * b)
print(a / b)


# In[12]:


print(a // b) # 몫
print(a % b)  # 나머지


# In[ ]:





# In[13]:


# str
st = '가가'
print(type(st))


# In[15]:


st2 = '가나다라마'
st2


# In[16]:


# list
# 리스트명 = [원소1, 원소2, ..., 원소n]
li = [1, 2, 3, 4, 5]
print(li)


# In[17]:


li = [1, 2, 'red', 'blue', 3, 4, [1, 2, 3, 4]]
print(li)


# In[19]:


li = ['a', 'b', 'c', 'd', 'e']
print(li[2])
print(li[-3])


# In[20]:


print(li[1:4])
# 슬라이싱
# 리스트이름[시작인덱스 번호 : 마지막인덱스 번호]


# In[21]:


print(len(li))


# In[22]:


len('apple')


# In[25]:


li1 = ['a', 'b', 'c', 'd']
li2 = [1, 3, 5, 7, 9]

print(li1 + li2)

print(li2 + li1)

li_total = li1 + li2
print(li_total)


# In[26]:


li3 = ['a', 'b', 'c', 'd']
li4 = [2, 4, 6, 8, 10]

li3.append(li4)
print(li3)


# In[27]:


print(len(li3))


# In[28]:


# dict
data = {
    '일자' : '2020-01-1',
    '이름' : '홍길동',
    '전화번호' : '010-1111-2222'
}


# In[30]:


data


# In[31]:


data.keys()


# In[32]:


data.values()


# In[33]:


data.items()


# In[34]:


# dict[키]
data['이름']


# In[36]:


data['나이'] = 20
data


# In[ ]:




