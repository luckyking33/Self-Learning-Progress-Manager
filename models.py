from sqlalchemy import Column, Integer, String, Boolean, ARRAY, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# 课程分类枚举（对应需求中的CourseCategory）
CourseCategoryEnum = ["CS自学", "考研", "职场提升"]

# 1. 用户模型
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    avatar = Column(String, nullable=False)
    headline = Column(String, nullable=True)
    streak_days = Column(Integer, default=0)
    enrollments = relationship("Enrollment", back_populates="user")

# 2. 课程模型
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    subtitle = Column(String, nullable=True)
    author_name = Column(String, nullable=False)
    author_avatar = Column(String, nullable=False)
    tags = Column(ARRAY(String), nullable=False)
    fork_count = Column(Integer, default=0)
    enrollment_count = Column(Integer, default=0)
    category = Column(String, nullable=False)  # 限制为CourseCategoryEnum
    cover_tone = Column(String, nullable=False)
    description = Column(String, nullable=True)
    author_role = Column(String, nullable=True)
    forked_from_title = Column(String, nullable=True)
    is_public = Column(Boolean, default=True)
    chapter_count = Column(Integer, default=0)
    knowledge_point_count = Column(Integer, default=0)
    estimated_hours = Column(Integer, default=0)
    chapters = relationship("Chapter", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")

# 3. 章节模型
class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    overview = Column(String, nullable=True)
    order_index = Column(Integer, nullable=False)
    course = relationship("Course", back_populates="chapters")
    knowledge_points = relationship("KnowledgePoint", back_populates="chapter")
    resources = relationship("Resource", back_populates="chapter")

# 4. 知识点模型
class KnowledgePoint(Base):
    __tablename__ = "knowledge_points"
    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=True)
    content = Column(String, nullable=True)
    order_index = Column(Integer, nullable=False)
    estimated_minutes = Column(Integer, nullable=False)
    key_actions = Column(ARRAY(String), nullable=True)
    chapter = relationship("Chapter", back_populates="knowledge_points")
    progress_records = relationship("KnowledgePointProgress", back_populates="knowledge_point")

# 5. 资源模型
class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)  # docs/link/video等
    url = Column(String, nullable=False)
    description = Column(String, nullable=True)
    chapter = relationship("Chapter", back_populates="resources")

# 6. 学习关系（报名）模型
class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
    last_learning_knowledge_point_id = Column(Integer, nullable=True)
    progress_percent = Column(Integer, default=0)
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    knowledge_progress = relationship("KnowledgePointProgress", back_populates="enrollment")

# 7. 知识点进度模型
class KnowledgePointProgress(Base):
    __tablename__ = "knowledge_point_progress"
    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False)
    knowledge_point_id = Column(Integer, ForeignKey("knowledge_points.id"), nullable=False)
    is_completed = Column(Boolean, default=False)
    enrollment = relationship("Enrollment", back_populates="knowledge_progress")
    knowledge_point = relationship("KnowledgePoint", back_populates="progress_records")