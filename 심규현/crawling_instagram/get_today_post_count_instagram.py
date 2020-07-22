import time
import datetime
import json
import re
from dateutil.parser import parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
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


def get_post_date(detail_url):
    browser.get(detail_url)
    time.sleep(0.25)
    time_link_tag = browser.find_elements_by_css_selector('._1o9PC')[0]
    get_time = parse(time_link_tag.get_attribute('datetime'))
    return str(get_time.date())
    

keyword = input('검색할 인스타그램 키워드(키워드 없이 Enter 누르면 종료): ')
if keyword != '':
    start_time = time.time()
    # 현재 시간에 따른 오늘 날짜의 게시글 확인할 때는 아래 코드로 확인
    now_date = str(parse(str(datetime.datetime.now())))[:10]
    # 특정 날짜 게시글 확인하고 싶을 때 아래와 같은 날짜 형태로 임의로 작성해서 확인
    # now_date = '2020-07-19'

    options = Options()
    options.headless = True
    browser = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
    # browser = webdriver.Chrome(executable_path="./chromedriver.exe")

    browser.implicitly_wait(3)
    
    browser.get(f'https://www.instagram.com/explore/tags/{keyword}/')

    time.sleep(3)

    # 오늘 게시글 개수, 게시글 url 모음, 오늘 게시글 시간대별 개수 분포
    today_post_count, post_urls, time_dict = 0, [], dict()

    print('[1] 자동 스크롤 다운 + 약 100개 게시글 URL 수집 중')
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Instagram 커뮤니티 가이드라인을 준수하지 않는 콘텐츠가 일부 포함되어 있어서 최근 게시물이 보이지 않는 경우
    h2_tags = soup.select('#react-root > section > main > article')[0].find_all('h2')
    check_instagram_hide_contents = len(h2_tags) == 1

    # 인기 게시물은 기본으로 크롤링
    posts = soup.select('#react-root > section > main > article > div:nth-child(1) div.v1Nh3.kIKUG > a')
    for post in posts:
        url = post.get('href')
        if url not in post_urls:
            post_urls.append(url)

    # 최근 게시물이 검색되는 경우 최근 게시물도 추가 크롤링
    if not check_instagram_hide_contents:
        scroll_count = 0
        while scroll_count < 5:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            posts = soup.select('#react-root > section > main > article > div:nth-child(3) div.v1Nh3.kIKUG > a')
            
            temp_urls = []
            for post in reversed(posts):
                url = post.get('href')
                if url not in post_urls:
                    temp_urls.append(url)
                else:
                    break
            post_urls += reversed(temp_urls)
            scroll_count += 1

            time.sleep(0.5)

            # 자동 스크롤
            for i in range(5):
                browser.execute_script("document.documentElement.scrollTop = document.body.scrollHeight;")
                time.sleep(0.1)
            
            time.sleep(0.5) # 페이지 로딩 및 파싱 완료를 위한 대기 시간 0.5초 세팅
    print('-----------------------------------------------------------------------------')

    print('[2] 각 게시글 상세 정보 추출')
    posts_detail = [] # 게시글의 상세 정보들을 담을 리스트
    for url in post_urls:
        try:
            post_dict = dict()
            browser.get(f'https://www.instagram.com{url}')
            browser.implicitly_wait(3)
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            post_dict['username'] = soup.select('#react-root > section > main > div > div > article > header > div.o-MQd.z8cbW > div.PQo_0.RqtMr > div.e1e1d > a')[0].text
            # 게시글에 작성된 해시태그는 검색 키워드와 무관한 내용들이 많아서 제외시킴(구현된 코드는 주석으로 남겨놓음)
            # post_contents = soup.select('#react-root > section > main > div > div.ltEKP > article > div.eo2As > div.EtaWk > ul > div > li > div > div > div.C4VMK > span')[0].text
            # post_dict['added_hashtags_by_user'] = ''.join(re.findall('#[A-Za-z0-9가-힣]+', post_contents)).replace('#', ' ').split()
            like_count = soup.select('#react-root > section > main > div > div.ltEKP > article > div.eo2As > section.EDfFK.ygqzn > div > div > button > span')[0].text
            post_dict['like_count'] = int(like_count.replace(',', ''))
            post_date = soup.select('#react-root > section > main > div > div > article > div.eo2As > div.k_Q0X.NnvRN > a > time')[0]['datetime']
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
    end_time = time.time()
    print(f'데이터 수집 및 게시글 상세 정보 추출 총 소요 시간: {round(end_time - start_time, 3)}[초]')
    print('-----------------------------------------------------------------------------')

    print('[3] 수집한 게시글 중 오늘 작성된 게시글 개수')
    print(f'{len(post_urls)}개 게시글 중 오늘 작성된 게시글은 {today_post_count}개 입니다.')
    print('-----------------------------------------------------------------------------')

    print('[4] json 파일로 저장')
    # json 파일로 저장할 dictionary 형태의 크롤링 정보
    json_data = dict()

    # 검색 키워드
    json_data['keyword'] = keyword

    # 크롤링 기준 날짜
    json_data['crawling_date'] = now_date

    # 크롤링한 게시글 상세 정보(유저 아이디, 좋아요 개수, 작성 날짜)
    json_data['posts'] = posts_detail

    # 크롤링한 게시글 수
    json_data['crawling_post_count'] = len(post_urls)

    # 크롤링 기준 날짜에 작성된 게시글 수
    json_data['today_post_count'] = today_post_count

    # 점수화 => (크롤링 기준 날짜에 작성된 게시글 수 / 크롤링한 게시글 수) * 100
    json_data['keyword_score'] = round((today_post_count / len(post_urls)) * 100, 3) if today_post_count else 0

    # 오늘 게시글 수 시간대별 분포
    json_data['today_post_distribution_group_by_time'] = time_dict

    # Instagram 가이드라인에 의해 인기 게시물만 보여지는 경우
    json_data['unable_to_search_more_posts'] = check_instagram_hide_contents
    with open(f'./json/version1/{keyword}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_data, indent='\t', ensure_ascii=False))
    print('저장 완료')
    print('-----------------------------------------------------------------------------')
else:
    print('크롤링 실행 안 함')