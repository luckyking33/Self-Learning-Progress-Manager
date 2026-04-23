from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://star_user:star_password@localhost:5432/star_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("✅ Python 连接 Docker 数据库成功！")
        db.close()
    except Exception as e:
        print("❌ 连接失败：", e)

if __name__ == "__main__":
    test_connection()