#!/usr/bin/env python
# coding: utf-8

# # 0. 데이터 불러오기

# In[1]:


# 판다스 불러오기
import pandas as pd


# In[6]:


# KBO 2019시즌 타자 기록지 데이터 불러오기

file = './data/KBO_2019_player_gamestats.csv'

raw = pd.read_csv(file, encoding = 'cp949')


# In[7]:


# 데이터 살펴보기

raw.head()


# In[8]:


raw.info()


# In[14]:


# 타자 데이터 분석에 활용할 컬럼만 선택

raw.columns

columns_select = ['팀', '이름', '생일', '일자', '상대', '타수', '안타', '홈런', 
                  '루타', '타점', '볼넷', '사구', '희비']

data = raw[columns_select]
data.head()


# ### Q) KBO 최고의 타자는?
# * 선수별 기록 집계하기

# In[25]:


# 피벗테이블 이용, 선수별 주요 기록 정리

data_player = data.pivot_table(index = ['팀', '이름', '생일'],
                values = ['타수', '안타', '홈런', '루타', '타점', '볼넷', '사구', '희비'],
                aggfunc = 'sum')
data_player


# In[26]:


# 타수가 0인 데이터는 제외
# 어느 정도가 적은지 판단하기 위해, 타수 데이터 분포 살펴보기
# 방법 : sns.histplot() 또는 pandas 내장된 시리즈.hist()

data_player['타수'].hist()


# In[27]:


# 타수가 50보다 큰 선수들만 선택
# reset_index()이용해 현재 인덱스로 설정된 팀/이름/생일 데이터 컬럼으로 다시 변경해줌

cond = data_player['타수'] > 50

data_player = data_player[cond].reset_index()
data_player


# In[31]:


# 타율/출루율/장타율/OPS 계산함수 만들어주기
# 데이터 프레임 입력하면 해당 데이터 프레임에서 인데긋별 실적을 계산하여 반환해주는 함수
# - 타율 : 안타 / 타수
# - 출루율 : (안타 + 볼넷 + 사구) / (타수 + 볼넷 + 사구 + 희생플라이)
# - 장타율 : 타율에 진루한 베이스 가중치 추가 --> 루타 / 타수
# - OPS: 출루율 + 장타율

def cal_hit(df):
    
    df['타율'] = df['안타'] / df['타수']
    df['출루율'] = (df['안타'] + df['볼넷'] + df['사구']) / (df['타수'] + df['볼넷'] + df['사구'] + df['희비'])
    df['장타율'] = df['루타'] / df['타수']
    df['OPS'] = df['출루율'] + df['장타율']
    
    return df


# In[33]:


# data_player에 있는 선수별 실적을 이용해 타율, 출루율, 장타율, OPS계산한 데이터 프레임 가져오기

player_stat = cal_hit(data_player)

player_stat


# In[42]:


# 출루율/장타율/OPS/타율 기준으로 정렬
# 출루율을 기준으로 정렬, 만약 동일값이 있을 경우 그 다음 기준인 장타율, OPS, 타율 순으로 정렬

player_stat = player_stat.sort_values( by = ['출루율', '장타율', 'OPS', '타율'], ascending = False)
player_stat = player_stat.reset_index(drop = True)
player_stat.head(20)


# In[46]:


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
    


# In[47]:


# 팀별 선수 출루율 분포 boxplot이용하여 알아보자

import seaborn as sns

sns.boxplot( data = player_stat, x = '팀', y = '출루율' )


# In[48]:


# 팀별 선수 출루율 swarmplot과 boxplot같이 사용하여 살펴보기

sns.boxplot( data = player_stat, x = '팀', y = '출루율' )
sns.swarmplot( data = player_stat, x = '팀', y = '출루율')


# In[59]:


# swarmplot과 boxplot같이 사용하면 색상이 겺쳐 구분하기 어려움
# 이럴경우 boxplot 색상 제거하고 간단하게 표시하면 깔끔하게 표현가능
# showcaps = False --> 박스 상/하단 가로라인 보이지 않게 하기
# whiskerprops{ 'linewidth' : 0}  --> 박스 상/하단 세로라인 보이지 않게 하기
# showfliers = False  --> 박스 범위 벗어난 아웃라이어 표시하지 않기
# boxprops = { 'facecolor' : 'None' }  --> 박스 색상 지우기

sns.boxplot( data = player_stat, x = '팀', y = '출루율',
           showcaps = False, whiskerprops = {'linewidth':0},
           showfliers = False, boxprops = {'facecolor':'None'})
sns.swarmplot( data = player_stat, x = '팀', y = '출루율')


# In[ ]:


# 타자별 2019시즌 기록 데이터 저장
# MS-엑셀 에서도 조회 가능하게끔 encoding = 'cp949'로 저장
# index 0 부터 시작하는 번호는 저장하지 않게 index = False 지정

file = './data/2019_KBO_hiiter_stat.csv'

player_stat.to_csv(file, encoding = 'cp949', index = False)

