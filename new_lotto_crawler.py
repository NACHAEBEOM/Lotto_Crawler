from selenium import webdriver
from datetime import datetime as dt
from bs4 import BeautifulSoup
import re
import pandas as pd

# 크롬 옵션 객체 생성
option = webdriver.ChromeOptions()
# 이미지 로딩하지 않고, 디스크캐시 사용하도록 설정하여 빠른접속 설정
prefs = {'profile.managed_default_content_settings.images': 2, 'disk-cache-size': 4096}
option.add_experimental_option("prefs", prefs)
# 헤드리스 브라우저 설정
option.add_argument("--headless")
# 크롬드라이버 객체 생성
driver = webdriver.Chrome("C:/Users\cbm/Downloads/chromedriver.exe", chrome_options=option)
# 크롬으로 해당 사이트 접속
driver.get('http://www.lotto.co.kr/article/list/AC01')
# 페이지 로딩될때까지 최대 5초대기
driver.implicitly_wait(5)

result = [] # 크롤링한 결과 담을 빈 list 생성
for page_nm in range(0, 92):
    # 페이지 넘기기(자바스크립트방식)
    driver.execute_script("paging.goPage({})".format(page_nm))
    driver.implicitly_wait(3)
    # 뷰티풀수프 객체로 html 문서를 파싱
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # selector로 해당 태그덩어리 리스트 지정
    sequences = soup.select("div.wnr_cur_list_wrap > ul > li")
    # 회차 덩어리별 파싱처리(반복문)
    for seq in sequences:
        # 회차는 span(범위) 5개로 이루어져 있음(개발자도구 참고)
        row = seq.select("span")
        # 회차번호 추출
        turn_nm = int(row[0].text.replace("회", ""))
        # 추첨날짜 추출
        raffle_date = dt.strptime(row[1].text, "%Y-%M-%d")
        # 당첨번호 6개 + 보너스번호 1개 추출
        win_nms = [re.findall(r'[\d]+(?=.png)', img['src'])[0] for img in row[2].select("img") if
                   img['src'].find("ico_add.png") is -1]
        win_nm1, win_nm2, win_nm3, win_nm4, win_nm5, win_nm6, bonus_nm = win_nms
        # 1등당첨번호 추출
        first_place_nm = int(row[3].text.strip())
        # 1등당첨금액 추출
        first_place_price = int(row[4].text.strip().replace(",", ""))
        # 변수 출력(저장하여 사용할것)
        print(turn_nm, raffle_date, win_nm1, win_nm2, win_nm3, win_nm4, win_nm5, win_nm6, bonus_nm, first_place_nm,
              first_place_price)
        # 결과를 담을 빈 list에 변수들을 list 형태로 전달
        result.append(
            [turn_nm, raffle_date, win_nm1, win_nm2, win_nm3, win_nm4, win_nm5, win_nm6, bonus_nm, first_place_nm,
             first_place_price]
        )
# 브라우저 종료(정상종료 안하면 메모리누수발생)
driver.close()
driver.quit()

# 결과물을 데이터프레임 형태로 변환 후 csv 파일로 저장
final_data_set = pd.DataFrame(result)
final_data.to_csv("C:/Python/Python36/venv/kmu/Scripts/final_data.csv", header=False, index=False)