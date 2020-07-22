# Instagram Posts Crawling

<br>

## :one: Overview

- 인스타그램에서 특정 키워드를 해시태그로 포함하는 게시글을 최신순으로 약 100개를 크롤링하여 오늘 작성된 게시글이 몇 개인지 확인

<br>

## :two: Installation

- 사전 필수 설치

  - Python 3.7.x (recommended 3.7.3 or 3.7.4)
  - Selenium
    - Chrome에서 Selenium을 사용하기 위해 https://sites.google.com/a/chromium.org/chromedriver/downloads에서 본인 크롬 버전에 맞게 다운로드할 것

- Additional Library Installation

  ```basj
  pip install beautifulsoup4
  pip install python-dateutil
  pip install selenium
  ```

<br>

## :three: Getting Started

- python 파일 실행 후 검색할 키워드를 입력 후 `Enter`를 누르면 자동으로 실행
  - 키워드 검색할 때 크롤링을 하기 싫으면 아무 것도 입력하지 않고 `Enter`를 누르면 취소됨
- 크롤링해서 오늘 작성된 게시글 수 계산한 결과는 `json` 폴더 안에 검색한 키워드명으로 `json` 파일이 생성됨

<br>

## :four: Information

- `get_today_post_count_instagram.py`
  - 각 게시글 상세 페이지 URL 수집 후 각 URL에 접속해서 날짜 데이터 추출하는 방식 => `json/version1` 폴더에 저장
  - 페이지 로딩 시간이 길어짐에 따라 오래 걸리는 현상은 비교적 적지만 전체 크롤링 시간이 다소 김
- `get_today_post_count_instagram2.py`
  - 첫 번째 게시글 클릭 후 우측 화살표 버튼을 누르면서 하나씩 게시글 이동하면서 날짜 데이터 추출하는 방식 => `json/version2` 폴더에 저장
  - 전체 크롤링 시간은 확실히 줄었으나 간헐적인 페이지 로딩 지연이 길어짐에 따라 데이터를 못 불러오는 현상이 발생해서 불안함
- 인터넷 연결이 원활하지 않아서 Timeout이 발생하는 경우 잠깐 쉬었다가 다시 크롤링 시작