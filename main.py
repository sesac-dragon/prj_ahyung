from crawler import crawl_pages
from db import insert_cafe_data, get_recent_logNos
import pandas as pd

# 최신 logNo 5개 가져오기 
recent_lognos = get_recent_logNos(limit=5)

cafe_data = crawl_pages(pages=2, keyword="뜨개카페", recent_lognos=recent_lognos)
print(cafe_data)
# df = pd.DataFrame(cafe_data)
# df.to_csv("뜨개카페.csv", index=False, encoding="utf-8-sig")
if cafe_data:
    cafe_data.sort(key=lambda x: x['logNo']) # 최신글 마지막 저장
    print(f"수집된 글 {len(cafe_data)}개 저장")
    insert_cafe_data(blog_data=cafe_data, env_path=".env")
else:
    print("신규 글 없음,종료 ")

