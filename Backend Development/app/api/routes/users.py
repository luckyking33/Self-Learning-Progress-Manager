"""User management endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.auth import get_current_user_id
from models import User, Enrollment, Course, Chapter, KnowledgePoint, KnowledgePointProgress
from schemas import ApiEnvelope, CurrentUserOut, EnrolledCourseCardOut

router = APIRouter()


@router.get("/me", response_model=ApiEnvelope[CurrentUserOut])
def get_current_user(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """获取当前用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="未登录")
    
    enrolled_course_ids = [en.course_id for en in db.query(Enrollment).filter(Enrollment.user_id == user_id).all()]
    
    return ApiEnvelope(
        code=0,
        message="ok",
        data=CurrentUserOut(
            id=user.id,
            name=user.name,
            avatar=user.avatar,
            headline=user.headline,
            streakDays=user.streak_days,
            enrolledCourseIds=enrolled_course_ids
        )
    )


@router.get("/me/enrollments", response_model=ApiEnvelope[list[EnrolledCourseCardOut]])
def get_enrolled_courses(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """获取已报名课程"""
    enrollments = db.query(Enrollment).filter(Enrollment.user_id == user_id).all()
    result = []
    
    for e in enrollments:
        c = db.query(Course).filter(Course.id == e.course_id).first()
        if not c:
            continue
        
        done = db.query(KnowledgePointProgress).filter(
            KnowledgePointProgress.enrollment_id == e.id,
            KnowledgePointProgress.is_completed == True
        ).count()
        
        total = c.knowledge_point_count or 0
        pct = round(done / total * 100) if total else 0
        
        last_title = None
        ch_title = None
        if e.last_learning_knowledge_point_id:
            kp = db.query(KnowledgePoint).filter(KnowledgePoint.id == e.last_learning_knowledge_point_id).first()
            if kp:
                last_title = kp.title
                ch = db.query(Chapter).filter(Chapter.id == kp.chapter_id).first()
                if ch:
                    ch_title = ch.title
        
        result.append(EnrolledCourseCardOut(
            id=c.id,
            title=c.title,
            subtitle=c.subtitle,
            authorName=c.author_name,
            authorAvatar=c.author_avatar,
            coverTone=c.cover_tone,
            completedKnowledgePointCount=done,
            totalKnowledgePointCount=total,
            progressPercent=pct,
            lastLearningKnowledgePointId=e.last_learning_knowledge_point_id,
            lastLearningKnowledgePointTitle=last_title,
            lastLearningChapterTitle=ch_title
        ))
    
    return ApiEnvelope(code=0, message="ok", data=result)
