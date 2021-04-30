#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd


# # 데이터 불러오기

# In[4]:


fpath = './data/babyNamesUS.csv'
raw = pd.read_csv(fpath)


# In[4]:


# 상위 5개 데이터 살펴보기
raw.head()


# In[6]:


# 데이터 구조 살펴보기
raw.info()


# # 8. 집계하기(pivot_table)

# <strong>df.pivot_table(index = '컬럼명', columns = '컬럼명', values = '컬럼명', ```aggfunc``` = 'sum')</Strong>
# 
# ```aggfunc``` 옵션 : sum, count, mean, ....

# * 이름 빈도수 집계하기

# In[11]:


# state, 성별, 출생연도 상관없이 이름 등록된 수 합하여 정리
# 인덱스 : 이름, 값은 등록된 수 모두 더하여 피벗 테이블 생성
# index = 'Name', values = 'Number'

raw.pivot_table(index = 'Name', values = 'Number', aggfunc = 'sum')


# In[10]:


raw.head()


# In[14]:


# 앞서 생성한 데이터에서 성별 구분 컬럼 추가하여 피벗 테이블 생성
# 인덱스는 이름으로 값은 등록된 수 합계, 컬럼은 성별로 구분
# index = 'Name', values = 'Number', columns = 'Sex'

name_df = raw.pivot_table(index = 'Name', values = 'Number', columns = 'Sex', aggfunc = 'sum')
name_df


# => 값이 NaN 이유 : 해당 이름이 여성에서 사용되지 않았기 때문임 (값이 0이 아님 주의!)

# In[15]:


# info() 이용하여 데이터 구조 보기

name_df.info()


# => 성별/이름 데이터는 ```20815```개가 있으며 <br/>
#     여자이름은 ```14140```개, 남자이름은 ```8658```개의 데이터가 있음<br/>
#     <mark>여성의 경우 남성보다 이름을 다양하게 사용한다는 것을 확인할 수 있음</mark>

# # 9. 비어있는 데이터 채워넣기

# 데이터를 정리하다보면, 비어있는 데이터들이 존재하게됨 => 결측치라고 부름<br/>
# 비어있는 데이터 부분을 어떻게 정리할지에 따라 분석 결과가 달라질 수도 있음!

# * 공통된 값을 입력하기 ex) 0
# * 임의의 수 입력 ex) 평균, 최댓값, 최솟값, 비어있는 자리 주변의 값 등
# * 비어있는 데이터 삭제

# 여러방법으로 처리 가능, 어떤 방법을 선택할 지는 데이터 / 분석방향 등에 따라 상이함

# In[20]:


name_df.head()


# In[21]:


# name_df의 결측치에 0입력
# fillna()

name_df = name_df.fillna(0)
name_df.head()


# => NaN으로 보여지던 결측치 0으로 채워진 것을 확인할 수 있음

# In[22]:


# info()통하여 데이터 구조 확인
name_df.info()


# => 확인결과 남녀 모두 ```20815```개의 데이터 값을 가지는 것을 확인할 수 있음

# Q) 남자/여자 가장 만히 사용되는 이름 top5?

# # 10. 정렬하기

# * name_df.```sort_values```(by = '컬럼명', ascending = False)

# In[25]:


# 남자 컬럼 기준으로 정렬 (by = 'M')
# 내림차순 정렬
name_df.sort_values(by = 'M', ascending = False)


# In[31]:


# 남자 컬럼 기준으로 내림차순하여 정렬한 상위 5개 데이터 확인

name_df.sort_values(by = 'M', ascending = False).head()


# => 남자 이름 top5 순서대로 <strong>Michael, James, Robert, John, David</strong> 라는것을 알 수 있음

# In[33]:


# 유사 방법으로 여자이름 top5확인해보기

name_df.sort_values(by = 'F', ascending = False).head()


# In[34]:


# .index 사용하여 index값만 확인할 수 있음
name_df.sort_values(by = 'F', ascending = False).head().index


# => 여자 이름 top5 순서대로 <strong>Mary, Jennifer, Elizabeth, Patricia, Linda</strong> 라는것을 알 수 있음

# # 11. 컬럼별 데이터 종류 확인하기

# * df['컬럼'].unique()
# * df['컬럼'].value_counts()

# In[5]:


raw.head()


# In[6]:


# StateCode 컬럼에 어떤 값 들어있는지 확인
raw['StateCode'].unique()


# In[7]:


# StateCode 컬럼 값 종류별로 몇 번 사용되었는지 확인
raw['StateCode'].value_counts()


# In[8]:


# YearOfBirth 컬럼의 연도별 데이터 수 살펴보기

raw['YearOfBirth'].value_counts()


# In[ ]:




