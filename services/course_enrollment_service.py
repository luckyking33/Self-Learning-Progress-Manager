from sqlalchemy.orm import Session
from models import Enrollment, Course, Chapter, KnowledgePoint
from datetime import datetime

# 1. 加入学习（报名）
def enroll_course(db: Session, user_id: int, course_id: int):
    # 1. 校验课程存在且公开
    course = db.query(Course).filter(Course.id == course_id, Course.is_public == True).first()
    if not course:
        return "课程不存在"
    # 2. 校验是否已报名
    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.course_id == course_id
    ).first()
    if existing_enrollment:
        return "已加入学习"
    # 3. 获取课程第一个知识点（初始化学习位置）
    first_chapter = db.query(Chapter).filter(Chapter.course_id == course_id).order_by(Chapter.order_index).first()
    first_kp_id = None
    if first_chapter:
        first_kp = db.query(KnowledgePoint).filter(KnowledgePoint.chapter_id == first_chapter.id).order_by(KnowledgePoint.order_index).first()
        if first_kp:
            first_kp_id = first_kp.id
    # 4. 创建报名记录
    enrollment = Enrollment(
        user_id=user_id,
        course_id=course_id,
        joined_at=datetime.utcnow(),
        last_learning_knowledge_point_id=first_kp_id,
        progress_percent=0
    )
    db.add(enrollment)
    # 5. 更新课程报名数
    course.enrollment_count += 1
    # 6. 提交事务
    db.commit()
    db.refresh(enrollment)
    return {
        "joinedAt": enrollment.joined_at
    }