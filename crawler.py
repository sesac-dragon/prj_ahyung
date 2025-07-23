from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json


# chrome driver 함수
def create_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(5)
    return driver


# 블로그 키워드 검색 링크 함수
def get_blog_links(driver, page_num, keyword):
    keyword_encoded = keyword.encode("utf-8")
    url = f"https://section.blog.naver.com/Search/Post.naver?pageNo={page_num}&rangeType=ALL&orderBy=recentdate&keyword={keyword}"
    driver.get(url)
    time.sleep(2)

    blog_links = []
    blog_cards = driver.find_elements(
        By.CSS_SELECTOR, "#content > section > div.area_list_search > div"
    )[:7]

    # 블로그 주소, id, no 추출
    for card in blog_cards:
        try:
            elem = card.find_element(
                By.CSS_SELECTOR, "div > div.info_post > div.desc > a.desc_inner"
            )
            blog_links.append(elem.get_attribute("href"))
        except:
            continue

    return blog_links


# 블로그 내용 크롤링 함수
def extract_blog_info(driver, blog_url):
    try:
        blogID = blog_url.split("/")[-2]
        logNo = blog_url.split("/")[-1]
        driver.get(
            f"https://blog.naver.com/PostView.naver?blogId={blogID}&logNo={logNo}"
        )
        time.sleep(2)

        try:
            # 지도 정보가 있는지 확인
            map_elem = driver.find_element(
                By.CSS_SELECTOR, "div.se-module.se-module-map-text > a"
            )
            map_data_raw = map_elem.get_attribute("data-linkdata")
            map_data = json.loads(map_data_raw)

            # 블로그 내용 크롤링
            blog = driver.find_element(
                By.CSS_SELECTOR, "#printPost1 > tbody > tr > td.bcc"
            ).text

            return {
                "logNo" : logNo,
                "카페이름": map_data["name"],
                "카페주소": map_data["address"],
                "위도": map_data["latitude"],
                "경도": map_data["longitude"],
                "블로그내용": blog,
            }
        except:
            print("지도정보 없음")

    except Exception as e:
        print(f"오류 발생: {e}")
        return None


# 최종 크롤링 함수
def crawl_pages(pages=10, keyword="뜨개카페"):
    driver = create_driver()
    cafe_list = []

    for i in range(1, pages + 1):
        print(f"[페이지 {i}] 블로그 링크 수집 중...")
        links = get_blog_links(driver, i, keyword)
        print(f" - 수집된 링크 {len(links)}개")

        for link in links:
            blog_info = extract_blog_info(driver, link)
            if blog_info:
                cafe_list.append(blog_info)

    driver.quit()
    return cafe_list
