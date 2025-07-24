import streamlit as st
import pandas as pd
import plotly.express as px
import pymysql
from db import load_env

st.markdown("# cafe-map")

# DB 연결
# .env 파일 불러오는 함수
def get_cafe_data():
    env = load_env(".env")
    conn = pymysql.connect(
        host=env["DB_HOST"],
        user=env["DB_USER"],
        password=env["DB_PASSWORD"],
        database=env["DB_DATABASE"],
        port=int(env["DB_PORT"]),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    query = "SELECT cafename, cafeaddress, latitude, longitude, blogdate FROM tb_cafe ORDER BY blogdate DESC"
    with conn.cursor() as cur:
        cur.execute(query)
        result = cur.fetchall()
    conn.close()
    return pd.DataFrame(result)

df = get_cafe_data()

# filtered_df = df[df['cafename'] == '바늘이야기 파주직영점']
# filtered_df

fig = px.scatter_map(df,
                        lat="latitude",
                        lon="longitude",
                        hover_name="cafename",
                        zoom=5,
                        height=700,)

fig.update_layout(mapbox_style="open-street-map")

st.plotly_chart(fig, use_container_width=True)
