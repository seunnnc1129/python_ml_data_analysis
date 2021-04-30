#!/usr/bin/env python
# coding: utf-8

# # 반복문
# for 변수 in 그룹:
#     작업내용

# In[2]:


fruits = ['바나나', '딸기', '배', '감', '귤']


# In[5]:


for fruit in fruits:
    print(fruit)


# # 조건문
# if 조건1:
#     조건1이 true일 경우 실행되는 코드
# elif 조건2:
#     조건1이 False이면서, 조건2라 True일 경우 실행되는 코드
# else:
#     위 조건들 모드 False일 경우 실행되는 코드
#     
#     
# 조건에서 > < = 활용 가능
# ex) A == B

# In[6]:


n = 20

if n < 1:
    print('1 이상의 자연수를 입력해 주세요')
elif n % 2 == 0:
    print('짝수')
else:
    print('홀수')


# In[7]:


shop_A = ['사과', '배', '파인애플']
shop_B = ['딸기', '포도', '사과', '배']


# In[10]:


if len(shop_A) > len(shop_B):
    print("A")
elif len(shop_A) < len(shop_B):
    print("B")
else:
    print("A == B")


# In[11]:


# 딸기 파는지 여부
'딸기' in shop_A


# In[12]:


'딸기' in shop_B


# In[13]:


if '딸기' in shop_A:
    print("딸기를 팔아요!")
else:
    print("딸기가 없어요ㅠㅠ")


# In[14]:


# 포도 미판매 여부
'포도' not in shop_A


# In[15]:


if '포도' not in shop_A:
    print("포도가 없어요ㅠㅠ")
else:
    ("포도를 팔아요!")


# In[16]:


A = '태극기'
B = '태극기가 바람에 펄럭입니다'


# In[19]:


if A == B:
    print('일치')
elif A in B:
    print(A + '가 ' + B + '에 포함됩니다')
else:
    print('불일치!')


# In[ ]:





# # 문자열 포매팅/정리하기
# 문자열 포매팅 : 문자열에서 변수를 표시하게 하는것
# * f "문자열 {변수}" python3.6이상
# * "문자열{}".format(변수) python3.5이하

# In[21]:


sentence = '안녕하세요 홍길동님 만나서 반갑습니다.'
print(sentence)


# In[24]:


# 파이썬 3.5 이하
name = '홍길동'

sentence = '안녕하세요 {}님 만나서 반갑습니다.'.format(name)
print(sentence)


# In[26]:


# 파이썬 3.6이상
name = '홍길동'

sentence = f'안녕하세요 {name}님 만나서 반갑습니다.'
print(sentence)


# In[29]:


month = '12월'
day = '25일'

sentence = "오늘은 {} {} 입니다.".format(month, day)
print(sentence)


# In[30]:


month = '12월'
day = '25일'

sentence = f"오늘은 {month} {day} 입니다."
print(sentence)


# ## strip()

# In[33]:


# 문자열에서 줄바꿈문자는 \n으로, 탭 문자는 \t로 표현합니다.
raw = '\n\t태극기가 바람에 펄럭입니다. \n 하늘 높이 하늘높이 펄럭입니다.'
print(raw)


# In[36]:


# 문자열.strip() : 문자열 시작과 끝부분 공백문자 제거 가능
raw_strip = raw.strip()
print(raw_strip)


# ## replace(변경전, 변경후)

# In[40]:


# 문자열.replace() : 특정 문자 없애거나 변경 가능
raw_edit = raw_strip.replace('태극기', '국기')
print(raw_edit)


# # 함수 만들기

# * 반복적으로 사용하는 코드들에 이름을 붙여서 쉽게 사용할 수 있게 하는것을 함수라고 함

# In[ ]:


def 함수이름(변수1, 변수2, ..., 변수n):
    
    실행내용1
    실행내용2
    
    return 실행결과


# In[52]:


# 두수 곱하는 함수

def multiple(a, b):
    
    result = a * b
    
    return result


# In[53]:


result = multiple(2, 5)
print(result)


# ### 구구단 출력

# In[56]:


for a in [2, 3, 4, 5, 6, 7, 8, 9]:

    for b in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        # print(a, b, multuple(a, b))
        sentence = f'{a} x {b} = {multiple(a,b)}'
        print(sentence)
    print('************')


# In[ ]:


a = 5
for b in range [1, 2, 3, 4, 5, 6, 7, 8, 9]:
    print(a * b)

