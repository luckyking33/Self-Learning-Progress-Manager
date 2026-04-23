from SQLconnet import SessionLocal
from models import User, Course

db = SessionLocal()

# 插入测试用户
db.add(User(
    id=7,
    name="林曜",
    avatar="LY",
    headline="正在把 STAR 做成一套真正能用的自学社区",
    streak_days=12
))

# 插入测试课程
db.add(Course(
    id=101,
    title="Vue 3 自学路线",
    subtitle="从组合式 API 到工程化交付的轻量课程仓库",
    author_name="沈清和",
    author_avatar="SQ",
    tags=["Vue 3", "Vite", "Pinia"],
    fork_count=184,
    enrollment_count=1260,
    category="CS自学",
    cover_tone="from-sky-100 via-white to-cyan-50",
    description="面向有JS基础的学习者",
    is_public=True,
    chapter_count=3,
    knowledge_point_count=6,
    estimated_hours=12
))

db.commit()
db.close()
print("✅ 测试数据插入完成！")