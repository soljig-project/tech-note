import time
import datetime
import json
from dateutil.parser import parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# ------------Version Information------------
# Python 3.7.4
# Chrome version 84
# -------------------------------------------

# ------Additional Installation Library------
# pip install beautifulsoup4
# pip install python-dateutil
# pip install selenium
# -------------------------------------------

def group_by_time(post_date):
    return int(post_date.split()[1][:2])


def open_next_post(post_idx):
    browser.find_elements_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow')[0].click()
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, ".s2MYR")
            )
        )
    except TimeoutException:
        print(f'{post_idx}번째 게시글 로딩 Timeout')


def open_first_post():
    first_post_line = browser.find_elements_by_css_selector('.Nnq7C')[0]
    first_post_line.find_elements_by_css_selector('.v1Nh3')[0].click()
    time.sleep(3)

    
keyword = input('검색할 인스타그램 키워드(키워드 없이 Enter 누르면 종료): ')
if keyword != '':
    # 현재 시간에 따른 오늘 날짜의 게시글 확인할 때는 아래 코드로 확인
    now_date = str(parse(str(datetime.datetime.now())))[:10]
    # 특정 날짜 게시글 확인하고 싶을 때 아래와 같은 날짜 형태로 임의로 작성해서 확인
    # now_date = '2020-07-19'

    # 크롬 브라우저 안 띄우고 할 때
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--log-level=3')
    browser = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=options)

    # 크롬 브라우저 띄우고 할 때
    # browser = webdriver.Chrome(executable_path="./chromedriver.exe")

    browser.get('https://www.instagram.com/accounts/login/?source=auth_switcher')

    browser.implicitly_wait(3)

    # 자동 스크롤을 위한 인스타그램 페이지 로그인
    print('인스타그램 로그인 중')
    user_id = '' # 인스타그램 계정 이메일 주소
    password = '' # 인스타그램 계정 비밀번호

    if user_id == '' or password == '':
        print('68, 69번 line에 인스타그램 계정을 입력한 후 다시 시도해주세요')
    else:
        id_input = browser.find_elements_by_css_selector('#react-root > section > main > div > article > div > div > div > form > div > div > label > input')[0]
        id_input.send_keys(user_id)
        password_input = browser.find_elements_by_css_selector('#react-root > section > main > div > article > div > div > div > form > div > div > label > input')[1]
        password_input.send_keys(password)
        password_input.submit()

        time.sleep(3)

        browser.get(f'https://www.instagram.com/explore/tags/{keyword}/')

        time.sleep(3)

        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Instagram 커뮤니티 가이드라인을 준수하지 않는 콘텐츠가 일부 포함되어 있어서 최근 게시물이 보이지 않는 경우 체크
        h2_tags = soup.select('#react-root > section > main > article')[0].find_all('h2')
        check_instagram_hide_contents = len(h2_tags) == 1
        crawling_post_count = 31 if check_instagram_hide_contents else 101

        open_first_post()

        # 오늘 게시글 개수, 오늘 게시글 시간대별 개수 분포
        print('크롤링 시작')
        today_post_count, time_dict, posts_detail = 0, dict(), []
        for idx in range(1, crawling_post_count):
            print(f'{idx}번째 게시글 상세 정보 추출 중')
            try:
                post_dict = dict()
                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')
                post_dict['username'] = soup.select('body > div._2dDPU.CkGkG > div.zZYga > div > article > header > div.o-MQd.z8cbW > div.PQo_0.RqtMr > div.e1e1d > span > a')[0].text
                like_count = soup.select('body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > section.EDfFK.ygqzn > div > div > button > span')[0].text
                post_dict['like_count'] = int(like_count.replace(',', ''))
                post_date = soup.select('body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > div.k_Q0X.NnvRN > a > time')[0]['datetime']
                convert_date = datetime.datetime.strptime(post_date[:-2], '%Y-%m-%dT%H:%M:%S.%f')
                post_date_in_korea = parse(post_date) + datetime.timedelta(hours=9)
                filtered_post_date = str(post_date_in_korea)
                post_dict['created_at'] = str(filtered_post_date)
                if now_date == filtered_post_date[:10]:
                    time_info = group_by_time(filtered_post_date)
                    if time_info in time_dict:
                        time_dict[time_info] += 1
                    else:
                        time_dict[time_info] = 1
                    today_post_count += 1
                posts_detail.append(post_dict)
            except IndexError:
                pass
            open_next_post(idx)
        
        json_data = dict()
        json_data['keyword'] = keyword # 검색 키워드
        json_data['crawling_date'] = now_date # 크롤링 기준 날짜
        json_data['posts'] = posts_detail # 크롤링한 게시글 상세 정보(유저 아이디, 좋아요 개수, 작성 날짜)
        json_data['crawling_post_count'] = len(posts_detail) # 로딩 Timeout을 제외한 크롤링한 게시글 수
        json_data['today_post_count'] = today_post_count # 크롤링 기준 날짜에 작성된 게시글 수
        json_data['keyword_score'] = round((today_post_count / crawling_post_count) * 100, 3) if today_post_count else 0 # 점수화 => (크롤링 기준 날짜에 작성된 게시글 수 / 크롤링한 게시글 수) * 100
        json_data['today_post_distribution_group_by_time'] = time_dict # 오늘 게시글 수 시간대별 분포
        json_data['unable_to_search_more_posts'] = check_instagram_hide_contents # Instagram 가이드라인에 의해 인기 게시물만 보여지는 경우
        with open(f'./json/version2/{keyword}.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_data, indent='\t', ensure_ascii=False))
        print('크롤링 종료')    
else:
    print('크롤링 실행 안 함')