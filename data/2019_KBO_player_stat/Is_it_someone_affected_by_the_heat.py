#!/usr/bin/env python
# coding: utf-8

# # 0. 데이터 불러오기

# In[27]:


# 2019년 선수별/경기별 기록 데이터 불러오기

import pandas as pd

file = './data/KBO_2019_player_gamestats.csv'
raw = pd.read_csv(file, encoding = 'cp949')


# In[28]:


raw.head()


# In[29]:


raw.info()


# In[30]:


raw.columns


# # Q) 꾸준한 선수 VS 여름에 힘떨어지는 선수?

# * 월별 기록 정리하기

# In[31]:


# '일자' 에서 '월' 꺼내서 컬럼 추가
# 시리즈에서 반복문 통해 하나씩 계산/점검

# 빈 월 리스트 만들어줌
month_list = []

# 반복문 통해 
for monthdate in raw['일자']:
    
    month = monthdate.split('-')[0]
    month_list.append(month)
raw['월'] = month_list   


# In[32]:


raw.head()


# In[33]:


# 분석에 사용할 컬럼만 선택

columns_select = ['팀', '이름', '생일', '일자', '상대', '타수', '안타', '홈런', '루타', '타점', '볼넷', '사구', '희비', '월']
data = raw[columns_select]

data.head()


# In[34]:


# 피벗테이블 이용해 월별 실적 집계
# fill_value = 0, 결측치 0으로 입력해주기

data_player_month = data.pivot_table(index = ['팀', '이름', '생일', '월'],
                values = ['타수', '안타', '홈런', '루타', '타점', '볼넷', '사구', '희비'],
                aggfunc = 'sum', fill_value = 0)

data_player_month.head()


# In[35]:


data_player_month.info()


# In[36]:


# 현재 인덱스로 정리된 팀/이름/생일/월 데이터 다시 컬럼으로 변경

data_player_month = data_player_month.reset_index()
data_player_month


# In[37]:


# 데이터 프레임에 포함된 타자의 타율/출루율/장타율/OPS 데이터 정리하는 함수

def cal_hit(df):
    
    '''
        - 타율 : 공을 쳐서 나가는 비율 --> 안타/타수
        - 출루율 : 진루해서 나가는 비율 --> (안타+볼넷+사구)/(타수+볼넷+사구+희비)
        - 장타율 : 타율에 진류한 베이스 가중치 추가 --> 루타 / 타수
        - OPS : 출루율 + 장타율
    '''
    
    df['타율'] = df['안타'] / df['타수']
    df['출루율'] = (df['안타'] + df['볼넷'] + df['사구']) / (df['타수'] + df['볼넷'] + df['사구'] + df['희비'])
    df['장타율'] = df['루타'] / df['타수']
    df['OPS'] = df['출루율'] + df['장타율']
    
    return df


# In[38]:


# data_player_month 데이터의 타자별 주요 실적 계산

player_month_stat = cal_hit(data_player_month)
player_month_stat.dropna().reset_index()


# In[39]:


# 월별 출루율 정리
# index = ['팀', '이름', '생일'], columns = '팀', values = '출루율'

month_pivot = player_month_stat.pivot_table(index = ['팀', '이름', '생일'], 
                              values = '출루율',
                              columns = '월')

month_pivot.head()


# ## KBO 출루율 최고타자 데이터 불러오기

# 앞서 정리한 선수별 시즌 출루율 기록 불러오고, 가장 실적이 좋은 타자들의 일별 출루율을 비교해보기

# In[40]:


# 시즌별 타자 실적 데이터 불러오기

file = './data/2019_KBO_hitter_stat.csv'
player_stat = pd.read_csv(file, encoding = 'cp949')
player_stat.head(10)


# In[41]:


# 불러온 시즌 기록과 월별 출루율 데이터 병합하기

df = pd.merge(player_stat, month_pivot, how = 'left', on = ['팀', '이름', '생일'])   #left_on = ['팀', '이름', '생일'], right_on = ['팀', '이름', '생일']
df.head()


# In[42]:


# 출루율 실적을 기준으로 정렬, 출루율 상위 50인 데이터 가져오기

df_sort = df.sort_values(by = '출루율', ascending = False).head(50)
df_sort


# In[43]:


# 출루율 관련 실적만 선택
df_sort.columns
df_selected = df_sort[['팀', '이름', '출루율', '03', '04', '05', '06', '07', '08', '09', '10']]
df_selected


# 히트맵으로 시각화 --> 숫자 많을경우 시각화하여 쉽게 확인 할 수 있음 <br>
# 히트맵 사용할 경우 데이터 프레임의 values 값이 모두 수치형이어야 함 (팀, 이름 --> 에러가 남, NaN은 괜찮음)
# 

# 팀, 이름 컬럼을 인덱스로 변경해줌

# In[44]:


# 팀, 이름 컬럼을 인덱스로 변경

df_selected = df_selected.set_index( ['팀', '이름'] )
df_selected


# In[45]:


# seaborn, matplotlib 으로 시각화 진행할때 데이터에 한글 있으면 실행해줌
# 이미지 상에 있는 한글을 표시하기 위한 한글 폰트 지정하고 필요한 라이브러리 불러들이는 코드

import matplotlib
from matplotlib import font_manager, rc
import platform
import matplotlib.pyplot as plt
import seaborn as sns

# 이미지 한글 표시 설정
if platform.system() == 'Window': # 윈도우인 경우 맑은 고딕
    font_name = font_manager.FontProperties(fname='c:/Windows/Fonts/malgun.ttf').get_name()
    rc('font', family = font_name)
else:  # Mac인 경우 애플고딕
    rc('font', family = 'AppleGothic')

# 그래프에서 마이너스 기호가 표시되도혹 하는 설정
matplotlib.rcParams['axes.unicode_minus'] = False


# In[46]:


# 먼저, 기본이 되는 히트맵 생성

sns.heatmap(df_selected)


# In[47]:


# 월별 출루율을 히트맵으로 그려보기
# 출루율 실적 히트맵에 표현하고 컬러맵은 Reds 활용 출루율 놓을수록 진하게 표현

fig, ax = plt.subplots( figsize = (13, 13) )
sns.heatmap(df_selected,
           annot = True, fmt = '.3f',
           cmap = 'Reds')


# In[51]:


# 월별 출루율을 시즌 출루율 대비한 +-값으로 변경, 월별 변화 정도 살펴보기


for col in df_selected.columns[1:]:
    df_selected[col] = df_selected[col] - df_selected['출루율']
    
df_selected['출루율'] = 0.0

df_selected.head()


# In[59]:


# 히트맵으로 살펴보기
# 컬러맵 Blue-Red 로 나타내기 위해 Rdbu_r로 지정해줌
fig, ax = plt.subplots( figsize = (13, 13) )
sns.heatmap(df_selected, 
            annot = True, fmt = '.3f',
            cmap = 'RdBu_r')


# In[ ]:




