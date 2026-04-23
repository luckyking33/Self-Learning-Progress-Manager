from models import Base
from SQLconnet import engine

# 创建所有表
Base.metadata.create_all(bind=engine)
print("✅ 数据库表创建成功！")
