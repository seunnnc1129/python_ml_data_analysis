#!/usr/bin/env python
# coding: utf-8

# # 0. 지도 시각화하기

# ## 0.1 folium 라이브러리 설치

# In[1]:


get_ipython().system(' pip install folium')


# In[2]:


import folium


# # 1. 지도 시각화

# * 지도생성하기
#     * ```m``` = folium.Map(location = [위도, 경도], zoom_start = 확대정도)
# * 정보 추가하기
#     * 마커 추가하기
#         * folium.Marker([위도, 경도]).add_to(```m```)
#     * 원 추가하기
#         * folium.CircleMarker([위도, 경도], radius = 원크기).add_to(```m```)
#     * 추가옵션
#         * tooltip = "마우스 올리면 보여질 정보"
#         * popup = "클릭하면 보여질 정보"
#     * 기타) ClickForMarker('체크').add_to(```m```)지도에서 클릭할 경우 마커 추가하기

# In[37]:


# 지도 생성하기 
# 지도 중심의 좌표를 위도, 경도 이용하여 표시
# 서울역을 기준으로 [37.555117428923765, 126.97070594158825]
# zoom_start 옵션 확대정도 지정할 수 있음
# 지도 생성후 위치 이동이나 확대/축소 조정할 수도 있음

m = folium.Map(location = [37.555117428923765, 126.97070594158825], zoom_start = 13)
m


# In[38]:


# 마커 추가하기

folium.Marker([37.555117428923765, 126.97070594158825],
             tooltip = '서울역', 
             popup = 'click!').add_to(m)
m


# In[40]:


# CircleMarker -> 동그라미 지도에 표시
# radius 옵션 통해 원 크기 지정 가능
# 써클마커 추가하기

folium.CircleMarker([37.555117428923765, 126.97070594158825],
                   radius = 20,
                   tooltip = '써클마커').add_to(m)
m


# ## 2. 미니맵을 추가할 경우 MiniMap

# In[44]:


# folium에는 다양한 효과를 줄 수 있는 plugin존재
# 미니맵을 지도 우측 하단에 추가, 현재 어느 위치를 살펴보고 있는지 확인 가능

from folium.plugins import MiniMap

m = folium.Map(location = [37.555117428923765, 126.97070594158825], zoom_start = 13)

# 미니맵 추가

minimap = MiniMap()
minimap.add_to(m)

m


# # 3. 서울 대피소 현황 지도 만들기

# 서울 대피소 현황 자료를 이용하여 지도에 시각화 해보기

# In[50]:


# csv파일 불러오기 위해 판다스 불러오기
import pandas as pd 


# In[59]:


# 서울열린데이터광장에 있는 서울시 대피소 현황 자료 다운 후 판스로 조회
# encoding = 'cp949' : MS 프로그램 사용시, 그 외 encoding = 'utf-8'(기본값)

file = './data/서울시 대피소 방재시설 현황 (좌표계_ WGS1984).csv'

raw = pd.read_csv(file, encoding = 'cp949') # utf-8  // MS-office : cp949
raw


# In[60]:


raw.head()


# In[61]:


raw.info()


# In[67]:


raw.head()


# In[97]:


# 인덱스번호가 0인 경우, 위도와 경도 데이터 출력하기

i = 0

lat = raw.loc[i, '위도']
long = raw.loc[i, '경도']
name = raw.loc[i, '대피소명칭']
address = raw.loc[i, '소재지']
maximum = raw.loc[i, '최대수용인원']
oper_yn = raw.loc[i, '현재운영여부']
tel = raw.loc[i, '전화번호']
addr_code = raw.loc[i, '행정동코드']

print(lat, long, name, address, maximum, oper_yn, tel, addr_code)


# In[98]:


# 모든 인덱스 번호에 대해 위도, 경도 출력

for i in range(len(raw)):
    
    lat = raw.loc[i, '위도']
    long = raw.loc[i, '경도']
    name = raw.loc[i, '대피소명칭']
    address = raw.loc[i, '소재지']
    maximum = raw.loc[i, '최대수용인원']
    oper_yn = raw.loc[i, '현재운영여부']
    tel = raw.loc[i, '전화번호']
    addr_code = raw.loc[i, '행정동코드']

    print(lat, long, name, address, maximum, oper_yn, tel, addr_code)


# In[99]:


# 지도를 생성하고 위도/경도에 마커 추가
# 중심위치 서울역

# 지도생성

m = folium.Map(location = [37.555117428923765, 126.97070594158825], 
               zoom_start = 12)

# 대피소 마커 추가하기

for i in range(len(raw)):
    
    lat = raw.loc[i, '위도']
    long = raw.loc[i, '경도']
    name = raw.loc[i, '대피소명칭']
    address = raw.loc[i, '소재지']
    maximum = raw.loc[i, '최대수용인원']
    oper_yn = raw.loc[i, '현재운영여부']
    tel = raw.loc[i, '전화번호']
    addr_code = raw.loc[i, '행정동코드']

    folium.Marker([lat, long], 
                 tooltip = name, 
                 popup = [address, maximum, oper_yn, tel, addr_code]).add_to(m)
    # print(lat, long, name)
    
m


# In[82]:


# 지도를 html로 저장하기
m.save('./data/Sheltermap.html')


# ### 마커가 너무 많을때에는 살펴보는 것이 어려울 수 있음
# ### --> ClusterMarker 이용해 근처에 있는 마커들까리 그룹으로 표현

# In[87]:


# MarkerCluster 라이브러리 불러오기

from folium.plugins import MarkerCluster


# In[88]:


# MarkerCluster 이용해 대피소 정보 지도에 시각화

# 지도생성
m = folium.Map(location = [37.555117428923765, 126.97070594158825], 
               zoom_start = 12)


marker_cluster = MarkerCluster().add_to(m)

# 대피소 마커 추가하기(마커클러스터 적용)

for i in range(len(raw)):
    
    lat = raw.loc[i, '위도']
    long = raw.loc[i, '경도']
    name = raw.loc[i, '대피소명칭']

    folium.Marker([lat, long], 
                 tooltip = name).add_to(marker_cluster)
    # print(lat, long, name)
    
m


# ### 미니맵 추가하기

# In[90]:


# 미니맵 라이브러리 불러오기

from folium.plugins import MiniMap


# In[100]:


# 미니맵, 클러스터 마커 이용하여 서울 대피소 지도 만들기
# 중심좌표 : 서울역
# 위치명 / 수용인원 등 정보 추가하여 지도 만들기

# 지도생성
m = folium.Map(location = [37.555117428923765, 126.97070594158825], 
               zoom_start = 12)


# 클러스터 생성
marker_cluster = MarkerCluster().add_to(m)

# 미니맵 추가
minimap = MiniMap()
minimap.add_to(m)

# 대피소 마커 추가하기(마커클러스터 적용)

for i in range(len(raw)):
    
    lat = raw.loc[i, '위도']
    long = raw.loc[i, '경도']
    name = raw.loc[i, '대피소명칭']
    address = raw.loc[i, '소재지']
    maximum = raw.loc[i, '최대수용인원']
    oper_yn = raw.loc[i, '현재운영여부']
    tel = raw.loc[i, '전화번호']
    addr_code = raw.loc[i, '행정동코드']

    folium.Marker([lat, long], 
                 tooltip = name,
                 popup = [address, maximum, oper_yn, tel, addr_code]
                 ).add_to(marker_cluster)
    # print(lat, long, name)
    
m


# In[92]:


# 생성한 지도 html확장자로 저장할 경우
# 필요할떄 언제나 열어서 정보 확인 가능
# 지도 저장하기

m.save('./data/Sheltermap.html')

