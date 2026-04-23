from sqlalchemy.orm import Session
from models import Enrollment, KnowledgePointProgress, KnowledgePoint, Chapter, Course
from schemas import CourseProgressStateOut
from datetime import datetime

# 1. 获取用户课程学习进度
def get_course_progress(db: Session, user_id: int, course_id: int):
    # 1. 查询报名记录
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.course_id == course_id
    ).first()
    if not enrollment:
        return None
    # 2. 获取已完成知识点ID
    completed_kp_ids = db.query(KnowledgePointProgress.knowledge_point_id).filter(
        KnowledgePointProgress.enrollment_id == enrollment.id,
        KnowledgePointProgress.is_completed == True
    ).all()
    completed_kp_ids = [item[0] for item in completed_kp_ids]
    # 3. 构造进度对象（selected与last保持一致）
    return CourseProgressStateOut(
        courseId=course_id,
        selectedKnowledgePointId=enrollment.last_learning_knowledge_point_id,
        lastLearningKnowledgePointId=enrollment.last_learning_knowledge_point_id,
        completedKnowledgePointIds=completed_kp_ids,
        joinedAt=enrollment.joined_at
    )

# 2. 更新学习进度
def update_course_progress(db: Session, user_id: int, course_id: int, progress_in):
    # 1. 校验报名记录存在
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.course_id == course_id
    ).first()
    if not enrollment:
        return None
    # 2. 更新lastLearning/selected知识点
    if progress_in.lastLearningKnowledgePointId:
        # 校验知识点属于该课程
        kp = db.query(KnowledgePoint).join(Chapter).join(Course).filter(
            KnowledgePoint.id == progress_in.lastLearningKnowledgePointId,
            Course.id == course_id
        ).first()
        if not kp:
            return "知识点不属于该课程"
        enrollment.last_learning_knowledge_point_id = progress_in.lastLearningKnowledgePointId
    # 3. 更新已完成知识点（方案A：懒创建）
    if progress_in.completedKnowledgePointIds is not None:
        # 先删除该报名下所有已完成记录
        db.query(KnowledgePointProgress).filter(
            KnowledgePointProgress.enrollment_id == enrollment.id
        ).delete()
        # 新增已完成知识点记录
        for kp_id in progress_in.completedKnowledgePointIds:
            # 校验知识点归属
            kp = db.query(KnowledgePoint).join(Chapter).join(Course).filter(
                KnowledgePoint.id == kp_id,
                Course.id == course_id
            ).first()
            if not kp:
                return "知识点不属于该课程"
            # 创建进度记录
            kp_progress = KnowledgePointProgress(
                enrollment_id=enrollment.id,
                knowledge_point_id=kp_id,
                is_completed=True
            )
            db.add(kp_progress)
    # 4. 重新计算进度百分比
    total_kp_count = db.query(Course).filter(Course.id == course_id).first().knowledge_point_count or 0
    completed_kp_count = db.query(KnowledgePointProgress).filter(
        KnowledgePointProgress.enrollment_id == enrollment.id,
        KnowledgePointProgress.is_completed == True
    ).count()
    enrollment.progress_percent = round((completed_kp_count / total_kp_count) * 100) if total_kp_count > 0 else 0
    # 5. 提交事务
    db.commit()
    db.refresh(enrollment)
    # 6. 返回更新后的进度
    return get_course_progress(db, user_id, course_id)