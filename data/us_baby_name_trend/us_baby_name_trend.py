#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd


# In[44]:


file = './data/babyNamesUS.csv'

raw = pd.read_csv(file)


# In[45]:


raw.head()


# In[12]:


raw.info()


# # Q) 남자 여자 구분없이 사용되는 공통 이름은?

# ### 남 / 여 등록된 이름 횟수 정리

# In[46]:


# 피벗테이블 이용하여 이름, 성별에 따른 등록 횟수를 정리

name_df = raw.pivot_table(index = 'Name', values = 'Number', aggfunc = 'sum', columns = 'Sex')
# name_df

# 결측치 0 으로 채워주기
name_df = name_df.fillna(0)
name_df


# * 남.여 비율 차이가 적을 수록 성별 구분없는 이름

# In[47]:


# 남/여 이름 등록수 합계를 계산
# Sum 컬럼 추가해주기

name_df['Sum'] = name_df['M'] + name_df['F']
name_df.head()


# In[15]:


# 남/여 등록 비율을 계산
# 해당이름의 남/여 비율 컬럼 추가

name_df['F_ratio'] = name_df['F'] / name_df['Sum']
name_df['M_ratio'] = name_df['M'] / name_df['Sum']

#name_df.head()

# 두 비율의 차이를 계산
# abs()사용 : 절댓값
# 'M_F_Gap' 컬럼 추가하기

name_df['M_F_Gap'] = abs(name_df['M_ratio'] - name_df['F_ratio'])
name_df


# In[48]:


# 이름 가장 많이 사용된 수 기준 내림차순 정렬
# 'Sum'기준 내림차순 정렬

name_df = name_df.sort_values(by = 'Sum', ascending = False)
name_df.head()


# In[17]:


# 남/여 비율 0.1 보다 작은 경우 찾기
# name_df['M_F_Gap'] < 0.1

cond = name_df['M_F_Gap'] < 0.1

name_df[cond]


# In[18]:


# 남/여 구분 없이 가장 많이 사용되는 이름 top10

name_df[ cond ].head(10).index


# #### => 결과는 <i>'Jessie', 'Riley', 'Emerson', 'Justice', 'Kris', 'Carey', 'Amari', 'Stevie', 'Merle', 'Jaylin'</i> 순으로 나타남

# #### James, Mary 가 가장 대표적인 미국 이름?

# # Q) 가장 대표적인 미국이름은?

# * 최근의 트랜드에 따른

# In[49]:


# unique() 사용, 기간 YearOfBirth에 들어가는 값들 살펴봄

raw['YearOfBirth'].unique()


# #### 세대를 기준으로 그룹 만들기

# 한 세대 나누는 기준 30년 (2020년 기준으로 30년씩)
# * 1930년대 이전
# * 1960년대 이전
# * 1990년대 이전
# * 2020년대 이전

# In[50]:


# 출생연도 시리즈에서 순서대로 해당하는 세대 그룹명에 매칭 그 결과 리스트로 출력

# 빈 리스트 생성
year_class_list = []

# 반복문과 조건문 이용하여 연도 매칭
for year in raw['YearOfBirth']:
    if year <= 1930:
        year_class = '1930년 이전'
    elif year <= 1960:
        year_class = '1960년 이전'
    elif year <= 1990:
        year_class = '1990년 이전'
    else:
        year_class = '2020년 이전'
        
    year_class_list.append( year_class ) 


# In[51]:


year_class_list


# In[52]:


# 세대 그룹명이 저장된 리스트 컬렴명에 추가해줌

raw['year_class'] = year_class_list

raw.head()


# In[53]:


# pivot_table() 활용하여 이름/성벌, 세대별 이름 등록수 합계표 구하기
# 결측치는 0으로 처리

name_period = raw.pivot_table(index = ['Name', 'Sex'], values = 'Number', aggfunc = 'sum', columns = 'year_class')
name_period = name_period.fillna(0)

# astype() : 해당 타입으로 값 변환
name_period = name_period.astype(int)
name_period.head()


# #### 전체 컬럼 합계 계산하기

# option.1) 모든 컬럼을 하나씩 더하기 : df['컬럼1'] + df['컬럼2'] + ... + df['컬럼n'] <br/>
# option.2) sum() 활용하기 : df.sum(axis = 1)

#     - 참고) df.sum()을 활용하면, 기본값으로 axis = 0 으로 지정되며, 컬럼별 합계가 아닌 row 별 합계가 계산됨

# #### 1. 모든 컬럼을 하나씩 더하기

# In[24]:


name_period['1930년 이전'] + name_period['1960년 이전'] + name_period['1990년 이전'] + name_period['2020년 이전']


# #### 2. sum() 활용하기

# In[54]:


# sum(axis = 1)활용 컬럼별 합계 추가 (축을 지정해주는것)

# name_period.iloc[0, 1]
name_period['sum'] = name_period.sum(axis = 1)
name_period.head()


# In[55]:


# 모든 컬럼 컬럼별 합계로 나누어 세대별 등록 비율 계산
# 계산된 값 '비율' 이라는 신규 컬럼에 저장

# name_period.columns : 각 컬럼 가져올 수 있음
for col in name_period.columns:

    col_new = col + ' 비율'
    name_period[col_new] = name_period[col] / name_period['sum']
    
name_period.head()


# In[56]:


# 이름 사용 수 합계, 2020년 이전 비율, 1990년 이전 비율 기준으로 내림차순 정렬

name_period = name_period.sort_values(by = ['sum', '2020년 이전 비율', '1990년 이전 비율'], ascending = False)
name_period


# In[57]:


# 인덱스가 여러 레벨로 되어있을 경우, 인덱스를 활용해 컨트롤 하는 것은 복잡함
# 따라서 reset_index()를 활용하여 인덱스로 설정된 이름과 성별을 컬럼으로 변경

name_period = name_period.reset_index()
name_period.head()


# In[58]:


# 남자 이름만 선택해서 보기

cond = name_period['Sex'] == 'M'
name_period[ cond ].head(10)


# In[59]:


# 2020년 이전 비율이 30% 보다 큰 경우에 해당하는 이름만?
## 남자의 경우

cond_age = name_period['2020년 이전 비율'] > 0.3
cond_sex = name_period['Sex'] == 'M'
cond = cond_age & cond_sex

name_period[cond].head(10)


# In[60]:


## 여자의 경우

cond = name_period['Sex'] == 'F'
name_period[cond].head(10)


# In[61]:


name_period.head()


# In[62]:


# 2020년 이전 비율이 30% 보다 큰 경우에 해당하는 이름만?
## 여자의 경우

cond_age = name_period['2020년 이전 비율'] > 0.3
cond_sex = name_period['Sex'] == 'F'
cond = cond_age 


# In[ ]:




