import pymysql
import pymysql.cursors


# .env 파일 불러오는 함수
def load_env(path=".env"):
    envs = {}
    with open(path, "r") as f:
        for line in f.readlines():
            key, value = line.rstrip().split("=")
            envs[key] = value
    return envs


# DB 저장 함수
def insert_cafe_data(blog_data, env_path=".env"):
    envs = load_env(env_path)

    conn = pymysql.connect(
        host=envs["DB_HOST"],
        port=int(envs["DB_PORT"]),
        user=envs["DB_USER"],
        password=envs["DB_PASSWORD"],
        database=envs["DB_DATABASE"],
        charset="utf8mb4",
    )

    with conn.cursor() as cur:
        sql = "INSERT INTO tb_cafe (logNo,cafename,cafeaddress,latitude,longitude,blogtext) VALUES (%s,%s,%s,%s,%s,%s)"

        values = [
            (
                data['logNo'],
                data["카페이름"],
                data["카페주소"],
                float(data["위도"]),
                float(data["경도"]),
                data["블로그내용"],
            )
            for data in blog_data
        ]

        cur.executemany(sql, values)
    conn.commit()

