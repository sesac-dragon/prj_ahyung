from crawler import crawl_pages
from db import insert_cafe_data
import pandas as pd

cafe_data = crawl_pages(pages=2, keyword="뜨개카페")
# df = pd.DataFrame(cafe_data)
# df.to_csv("뜨개카페.csv", index=False, encoding="utf-8-sig")

sorted_cafes = insert_cafe_data(blog_data=cafe_data, env_path=".env")


