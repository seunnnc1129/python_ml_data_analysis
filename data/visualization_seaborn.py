#!/usr/bin/env python
# coding: utf-8

# # 데이터 시각화 방법 - seaborn 라이브러리 사용

# ## 0. 데이터 시각화 중요성?
# * 통계량이 모두 동일한 데이터 -> 항상 똑같은 데이터일까?
#     * 아님 -> 시각화를 통해 어떤 데이터 특성을 가졌는지 비교하는것 중요
# 

# * 데이터 타입별 시각화
#     * 수치형 * 수치형 : scatterplot, lmplot, jointplot 이용
#     * 수치형 * 카테고리형 : boxplot, barplot, heatmap 이용
#     * 수치형 * 위치정보 : folium 라이브러리 활용

# In[1]:


# 시각화를 위해 seaborn 라이브러리 불러오기
import seaborn as sns


# In[6]:


# seaborn에 예제로 활용할 수 있는 데이터셋 있음 - tips 데이터셋 활용
# 판다스 동일한 명령어 사용가능

raw = sns.load_dataset('tips')


# In[7]:


raw.head()


# In[8]:


raw.info()


# ## 1. seaborn 함수 기본 형태
# * sns.그래프 종류(data = 데이터프레임, x = '값', y = '값', hue = '색상지정값')

# ## 2. 데이터 분포 살펴보기(수치형 VS 수치형)

# #### 2.1 ```relplot```(data = df, x = , y = , hue = , kind = 'scatter')<br/>
# 두 개의 변수(모두 수치형 데이터) 분포를 확인할 때
# * kind 옵션
#     * 'scatter'(기본값)
#     * 'line'

# In[11]:


# sns.relplot()을 이용해 두 데이터 간의 관계를 시각화 할 수 있음
# kind 옵션을 이용해 표현 방식을 조절할 수 있는데, default값은 scatter

sns.relplot( data = raw, x = 'tip', y = 'total_bill')


# In[12]:


# kind옵션을 line으로 조정
sns.relplot( data = raw, x = 'tip', y = 'total_bill', kind = 'line')


# In[14]:


# hue옵션 사용하여 성별따라 색 구분

sns.relplot( data = raw, x = 'tip', y = 'total_bill', hue = 'sex')


# #### 2.2 ```jointplot```(data = df, x = , y = , kind = 'scatter')
# * kind에 따라 그래프 형태가 변경됨
#     * default : 'scatter'
#     * 'reg' : point + regression
#     * 'kde' : 누적 분포 차트 like 지도

# In[16]:


# jointplot을 이용해 두 수치데이터 간의 관계와 각 데이터의 분포를 함께 확인 가능
# kind 옵션을 통해 여러 타입으로 시각화 할 수 있는데 default값은 'scatter'

sns.jointplot(data = raw, x = 'tip', y = 'total_bill')


# In[18]:


# kind = 'kde'로 지정할 경우, 밀도함수를 이용해 시각화 가능
# 진하게 표시될 수록 집중되어있다는 것 의미, 값이 급격하게 변할 수록 선의 간격이 좁게 표시

sns.jointplot(data = raw, x = 'tip', y = 'total_bill', kind = 'kde', shade = True)


# In[22]:


# kind = 'reg' 사용, 회귀선 확인 가능

sns.jointplot(data = raw, x = 'tip', y = 'total_bill', kind = 'reg')


# In[24]:


# kind = 'hex' 사용, ked 속성과 유사하게 밀도를 표현 
# but 간격이 다르지않고 모두 동일한 육각형 모양으로 시각화

sns.jointplot(data = raw, x = 'tip', y = 'total_bill', kind = 'hex')


# ### 2.3 ```pairplot```(data = df) <br/>
# df의 모든 수치형데이터 컬럼에서 두 컬럼씩 관계를 시각화함

# In[25]:


# pairplot을 이용해 total_bill, tip, size 데이터 간의 관계 살펴봄

sns.pairplot(data = raw)


# In[26]:


# hue이용하여 특정 컬럼의 값에 따른 분포 색상 이용해 시각화 가능

sns.pairplot(data = raw, hue = 'sex')


# ## 3. 데이터 분포 살펴보기(수치형 VS 카테고리형)

# ### 3.1 ```boxplot```(data = df, x = , y = , hue = )

# In[32]:


# boxplot을 이용하여 가로축은 day, 세로축은 tip값의 분포로 박스플랏을 그릴수 있음

sns.boxplot(data = raw, x = 'day', y = 'tip')


# In[33]:


# hue 옵션을 추가, 특정 기준의 변화에 따른 데이터분포 살펴볼수 있음

sns.boxplot(data = raw, x = 'day', y = 'tip', hue = 'smoker')


# In[39]:


# boxplot 하나의 기준에 대한 데이터 분포 범위를 파악하는데 용이
# 데이터 개수를 표현하지는 않기 댸문에 데이터 갯수가 다른 값을 비교하기에 문제 있을수 있음
# swarmplot 이용하면 데이터 개수와 함께 분포 살펴보기 가능

sns.swarmplot(data = raw, x = 'day', y = 'tip', hue = 'smoker', dodge = True, size = 3)


# In[40]:


# boxplot과 swarmplot 함계 그려볼 수 있음

sns.boxplot(data = raw, x = 'day', y = 'tip', hue = 'smoker')
sns.swarmplot(data = raw, x = 'day', y = 'tip', hue = 'smoker', dodge = True, size = 3)


# In[41]:


# size/성별 별 tip의 분포

sns.boxplot( data = raw, x = 'size', y = 'tip', hue = 'sex')


# ### 3.2 barplot(data = df, x = , y = , hue = )

# In[43]:


# barplot 의 경우 특정 값에 대한 개수를 살펴볼 수 있음


sns.barplot(data = raw, x = 'size', y = 'tip', hue = 'sex')


# ## 4. 데이터 분포 살펴보기 (수치형 VS 카테고리형 VS 카테고리형)

# ### 4.1 heatmap(data = df, annot = True, fmt = '.nf', cmap = '색상값')
# * fmt : '.0f' -> 정수표현, '.1f' -> 소수점 아래 한자리 까지, '.2f' -> 소수점 아래 두번째 자리 까지
# * cmap : 히트맵 색상 컬러 조정 / 추천색상 : Reds, Blues, vlag, Pastel1, RdBu_r

# In[44]:


raw.head()


# In[46]:


# 히트맵을 이용하며느 두 카테고리형 분포에 대한 수치형데이터의 값을
# 색상을 히용하여 한눈에 살펴볼 수 있음
# 요일별, size별, 평군 tip 데이터를 가진 피봇테이블 생성

df = raw.pivot_table(index = 'day', columns = 'size', values = 'tip', aggfunc = 'mean')
df


# In[47]:


# 보고자 하는 관점에 따라 데이터프레임을 만든 후, heatmap() 함수 이용

sns.heatmap(data = df)


# In[50]:


# 실제 데이터를 확인하기 위해, 히트맵 내에 수치 표현 가능
# annot = True 로 지정해주면 수치를 표현, 표현되는 숫자 형태는 fmt 옵션으로 지정
# fmt = '.2f'의 경우 소숫점 아래 두 자리까지 표시
# '.0f' : 소수점뒤에 표현되는 자리수 없이 정수로만 표현하라는 의미

sns.heatmap(data = df,
           annot = True, fmt = '.0f')


# In[66]:


# cmap옵션을 이용해, 색상을 조정할 수 있음
# seaborn에서 다양한 종류의 컬러차트 지원하며, 이번에 Blues 사용

sns.heatmap(data = df,
           annot = True, fmt = '.0f',
           cmap = 'Blues')


# In[ ]:




