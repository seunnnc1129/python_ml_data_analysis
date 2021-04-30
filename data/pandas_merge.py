#!/usr/bin/env python
# coding: utf-8

# # 1. pandas 불러오기

# In[3]:


# 판다스 라이브러리 불러오기

import pandas as pd


# # 2. 데이터 불러오기
# 
# pd.read('엑셀파일경로+명')

# In[4]:


# 엑셀 파일의 데이터 읽어오기
fpath = './data/exam.xlsx'
data = pd.read_excel(fpath, index_col = '번호')
data


# ## 데이터 살펴보기

# In[4]:


# 데이터 살펴보기 head()
data.head()


# In[5]:


# info() 사용하여 인덱스/컬럼 구조 살펴보기

data.info()


# In[6]:


# describe() 사용 기초통계량 살펴보기

data.describe()


# # 5. 데이터 추가하기
# 
# ### df['컬럼명']=```data```
#  ✖︎ ```data```에 들어갈 수 있는것
#     * 하나의 값 : 전체 모두 동일한 값
#     * 그룹 : 기스트, 판다스의 시리즈
#         
#  ✖︎ 새로운 컬럼을 만들 경우에는 ```df.컬럼명``` = data 형태는 사용 불가. (df['컬럼명']으로만 가능)

# In[5]:


# data['컬럼명']을 이용해 하나의 컬럼을 선택가틍
data['수학']


# In[6]:


# 하나의 컬렴을 선택한 뒤, 하나의 값으로 입력할 경우 전체가 동일한 값을가진 시리즈를 입력할 수 있음
# '음악' 컬럼으로 모두 90을 입력

data['음악'] = 90

data


# In[7]:


# 여러 개의 값을 그룹(리스트나 시리즈 형태)으로 입력할 경우, 위에서부터 순서대로 해당값을 가진 시리즈를 입력할 수 있음
# '체육' 컬럼으로 100, 80, 60 을 순서대로 입력하기

data['체육'] = [100, 80, 60]

data


# 컬럼 간의 계산을 통해 신규 컬럼을 만들 수도 있음

# In[16]:


# 사칙연산도 가능(컬럼끼리 연산)
# 국영수 평균컬럼 추가하기

data['평균'] = (data['국어'] + data['영어'] + data['수학']) / 3

data


# # 6. 데이터 표 병합하기
# 
# 두 개의 엑셀 파일에서 데이터를 불러온 뒤, 데이터를 병합

# In[8]:


# 첫번째 데이터 불러오기 (index_col = '번호')
fpath = './data/exam.xlsx'
A = pd.read_excel(fpath, index_col = '번호')
A


# <strong>요청!</strong>```두 과목 점수 누락! 점수 추가하기!```

# In[9]:


# 두 번째 데이터 불러오기(inedx_col = '번호')
fpath2 = './data/exam_extra.xlsx'
B = pd.read_excel(fpath2, index_col = '번호')
B


# <strong>데이터 병합하기 : pd.```merge```(A, B, how = ```'left'```, left_on = ```'A컬럼명'```, right_index = True)</strong>

# ```how```:
# <br>
# - left(왼쪽 표 기준)<br>
# - right(오른쪽 표 기준)<br>
# - inner(A, B 둘 다 있는 데이터만)<br>
# - outer(A, B 한쪽이라도 있는 데이터)<br>

# ```left_on``` : A 병합 기준 컬럼 지정<br>
# ```left_index = True``` : A 병합 기준 인덱스로 지정<br>
# ```right_on``` : B 병합 기준 컬럼 지정<br>
# ```right_index = True``` : B 병합 기준 인덱스로 지정<br>
# ```on``` : A & B 같은 이름의 열을 기주으로 지정할 경우<br>

# In[15]:


# 엑셀의 Vlookup 처럼 합치기
# A, B 테이블을 A테이블에 있는 키값을 기준으로 (how = 'left')
# A 테이블은 인덱스를 키 값으로, B 테이블은 인덱스를 키 값으로 병합하기

total = pd.merge(A, B, how = 'left', left_index = True, right_index = True)
total


# => <strong><mark>A테이블 인덱스 기준으로 병합</mark></strong>되어 B테이블에 있는 4, 5번은 나타나지 않고 B테이블에 3번이 존재하지 않기 때문에 3번의 과학, 사회 컬럼의 값이 NaN이 됨

# In[16]:


# A, B 테이블을 B테이블에 있는 키값을 기준으로 (how = 'right')
# A 테이블은 인덱스를 키 값으로, B 테이블은 인덱스를 키 값으로 병합하기

pd.merge(A, B, how = 'right', left_index = True, right_index = True)


# => <mark><strong>B테이블 인덱스 기준으로 병합</strong></mark>되어 A테이블에 있는 3번은 나타나지 않고 B테이블에 4, 5번이 존재하지 않기 때문에 3, 5번의 국영수 컬럼의 값이 NaN이 됨

# In[17]:


# A, B 테이블을 A, B테이블 양쪽에 모두있는 키값을 기준으로 (how = 'inner')
# A 테이블은 인덱스를 키 값으로, B 테이블은 인덱스를 키 값으로 병합하기

pd.merge(A, B, how = 'inner', left_index = True, right_index = True)


# => <mark><strong>A, B 테이블 양쪽 모두 있는 인덱스 기준으로 병합</strong></mark>되어 1, 2번만 존재

# In[19]:


# A, B 테이블을 A, B테이블 양쪽에 한번이라도 값이 있는 키값을 기준으로 (how = 'outer')
# A 테이블은 인덱스를 키 값으로, B 테이블은 인덱스를 키 값으로 병합하기

pd.merge(A, B, how = 'outer', left_index = True, right_index = True)


# => <mark>합집합</mark> 개념 / A, B 양쪽테이블 한개라도 값이 있으면 전부 병합<br/>
# 3번의 과학, 사회의 값이 NaN으로 4, 5번의 국영서 값이 NaN으로 나타남

# # 7. 저장하기

# <strong>df.to_excel('파일경로+파일명.xlsx', index = False</strong>

# In[20]:


total = pd.merge(A, B, how = 'left', left_index = True, right_index = True)
total


# In[21]:


# 현재 폴더 내의 data폴더 안에 exam_total.xlsx 파일에 저장

fpath = './data/exam_total.xlsx'

total.to_excel(fpath)


# In[26]:


# 판다스 데이터프레임에서는 항상 인덱스 값 가지게 됨
# 인덱스 지정하고 싶지 않을경우 저장시 index = False 옵션 사용하면 됨

fpath = './data/exam_total_withoutindex.xlsx'

total.to_excel(fpath, index = False)


# In[ ]:




