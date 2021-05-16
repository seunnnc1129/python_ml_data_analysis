#!/usr/bin/env python
# coding: utf-8

# ## 0. 데이터 불러오기

# In[2]:


# 타자/경기별 기록 데이터 불러오기

import pandas as pd


# In[3]:


file = './data/KBO_2019_player_gamestats.csv'

raw = pd.read_csv(file, encoding = 'cp949')
raw.head()


# ## 1. 상대 팀별 기록 정리하기

# In[4]:


# unique()사용, '상대' 컬럼에 어떤 값이 들어있는지 확인하기

raw['상대'].unique()


# #### '상대' 컬럼에서 @가 붙어있는 경우 --> 원정경기, 없으면 --> 홈경기

# In[5]:


# '상대' 컬럼에서 홈/원정 여부에 따라 상대팀을 분리하여 각각 '홈어웨이', '상대팀' 컬럼으로 지정

opp_list = []
home_away_list = []

for opp in raw['상대']:
    
    if '@' in opp:
        home_away = '원정'
        opp = opp.replace('@', '')
    else:
        home_away = '홈'

    opp_list.append(opp)
    home_away_list.append(home_away)
    
raw['홈어웨이'] = home_away_list
raw['상대팀'] = opp_list

raw.head()
    


# In[6]:


raw.head()


# In[7]:


# 상대 팀별 실적 정리하기 위해 피벗테이블 만들기
# 상대팀별 실적 정리 ['타수', '안타', '홈런', '루타', '타점', '볼넷', '사구', '희비']

data = raw.pivot_table(index = ['팀', '이름', '생일', '상대팀'],   # '상대'라고 지정하면 홈, 어웨이 구분한 이유가 없어짐
                values = ['타수', '안타', '홈런', '루타', '타점', '볼넷', '사구', '희비'],
                aggfunc = 'sum') 

data.head()


# In[8]:


# 상대팀별 타수가 0보다 큰 경우의 데이터만 선택

cond = data['타수'] > 0

data = data[ cond ]
data.head()


# In[9]:


# reset_index()사용, 인덱스로 지정한 팀/이름/생일 컬럼으로 바꿔줌

data = data.reset_index()


# In[10]:


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


# In[11]:


# 타자/상대팀별 실적 계산

player_stats_opp = cal_hit(data)
player_stats_opp


# ## 2.  XXX팀 킬러는 누구?

# In[12]:


# 특정 팀 상대로 강한 타자가 누군지 살펴보는 함수 생성

def opp_team(team):
    cond = (player_stats_opp['상대팀'] == team) & (player_stats_opp['타수'] > 10)
    
    # player_stats_opp[cond].sort_values(by = 'OPS', ascending = False).head(10)
    
    return player_stats_opp[cond].sort_values(by = 'OPS', ascending = False).head(20)


# ### 2.1 기아

# In[13]:


'''
team = 'KIA'
cond = (player_stats_opp['상대팀'] == team) & (player_stats_opp['타수'] > 10)

player_stats_opp[cond].sort_values(by = 'OPS', ascending = False).head(10)
'''

opp_team('KIA')


# ### 2.2 두산

# In[14]:


opp_team('두산')


# ### 2.3 롯데

# In[15]:


opp_team('롯데')


# ### 2.4 삼성

# In[16]:


opp_team('삼성')


# ### 2.5 SK

# In[17]:


opp_team('SK')


# ### 2.6 NC

# In[18]:


opp_team('NC')


# ### 2.7 LG

# In[19]:


opp_team('LG')


# ### 2.8 KT

# In[20]:


opp_team('KT')


# ### 2.9 키움

# In[21]:


opp_team('키움')


# ### 2.10 한화

# In[22]:


opp_team('한화')


# In[23]:


# KBO 전체 팀 대상으로 팀별 OPS 상위 5명 타자

hitter_df = pd.DataFrame()

#player_stats_opp['상대팀']

for team in player_stats_opp['상대팀']:
    
    cond = (player_stats_opp['상대팀'] == team) & (player_stats_opp['타수'] > 20)
    df = player_stats_opp[cond].sort_values(by = 'OPS', ascending = False).head()
    hitter_df = hitter_df.append(df)


# In[24]:


hitter_df


# In[25]:


# 특정팀 상대 출루율 Top5이내 타자 리스트
# unique()사용하여 복수 팀 대상으로 top5에 들었을 경우 한번만 나타나게함 (중복제거)

hitter_df['이름'].unique()


# In[26]:


'민병헌' in hitter_df['이름'].unique()


# In[27]:


# 특정팀 상대 출루율 top5이내 상위타자들을 대상으로 팀별 출루율 피벗테이블 생성
# 반복문 사용

cond = []

for name in player_stats_opp['이름']:
    
    if name in hitter_df['이름'].unique():
        cond.append(True)
    else:
        cond.append(False)
        
player_stats_opp[cond]
# player_opp_top5 = player_stats_opp[cond].sort_values(by = ['OPS', '상대팀'], ascending = False)
# player_opp_top5.head(20)


# In[34]:


# 특정팀 상대 출루율 top5이내 상위타자들을 대상으로 팀별 출루율 피벗테이블 생성
# 판다스 명령어사용
cond = player_stats_opp['이름'].isin( hitter_df['이름'].unique() )
top_df = player_stats_opp[ cond ].sort_values( by = ['OPS', '출루율'], ascending = False)

top_pivot = top_df.pivot_table( index = ['팀', '이름'], values = 'OPS', columns = '상대팀' )
top_pivot


# In[35]:


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


# In[50]:


# 한번에 살펴보기 위해 히트맵으로 표시

fig, ax = plt.subplots( figsize = (10, 13))

sns.heatmap(data = top_pivot, 
            annot = True, fmt = '.3f',
            cmap = 'RdBu_r')


# In[54]:


# 히트멥 사용시 center 옵션 이용하여 컬러맵 기준(색상 변화 지점)을 변경할 수 있음
# center = 0.8로 지정할 경우 빨간색으로 표현되는 부분이 적어짐
# 상대적인 크기를 살펴보고자 할때 center를 변경하여 살펴 볼 수 있음

fig, ax = plt.subplots( figsize = (10, 13))

sns.heatmap(data = top_pivot,
            annot = True, fmt = '.3f',
            center = 0.75,
            cmap = 'RdBu_r',)

