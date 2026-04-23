"""Course progress management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.auth import get_current_user_id
from models import Enrollment, KnowledgePoint, Chapter, Course, KnowledgePointProgress
from schemas import ApiEnvelope, CourseProgressStateOut, CourseProgressPatchIn

router = APIRouter()


@router.get("/{courseId}/progress", response_model=ApiEnvelope[CourseProgressStateOut])
def get_course_progress(
    courseId: int = Path(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """获取用户课程学习进度"""
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.course_id == courseId
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="尚未加入学习")
    
    completed_ids = db.query(KnowledgePointProgress.knowledge_point_id).filter(
        KnowledgePointProgress.enrollment_id == enrollment.id,
        KnowledgePointProgress.is_completed == True
    ).all()
    
    return ApiEnvelope(
        code=0,
        message="ok",
        data=CourseProgressStateOut(
            courseId=courseId,
            selectedKnowledgePointId=enrollment.last_learning_knowledge_point_id,
            lastLearningKnowledgePointId=enrollment.last_learning_knowledge_point_id,
            completedKnowledgePointIds=[x[0] for x in completed_ids],
            joinedAt=enrollment.joined_at
        )
    )


@router.patch("/{courseId}/progress", response_model=ApiEnvelope[CourseProgressStateOut])
def patch_course_progress(
    courseId: int = Path(...),
    progress_in: CourseProgressPatchIn = Depends(),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """更新学习进度"""
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.course_id == courseId
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="尚未加入学习")
    
    if progress_in.lastLearningKnowledgePointId:
        enrollment.last_learning_knowledge_point_id = progress_in.lastLearningKnowledgePointId
    
    if progress_in.completedKnowledgePointIds is not None:
        db.query(KnowledgePointProgress).filter(
            KnowledgePointProgress.enrollment_id == enrollment.id
        ).delete()
        
        for kid in progress_in.completedKnowledgePointIds:
            db.add(KnowledgePointProgress(
                enrollment_id=enrollment.id,
                knowledge_point_id=kid,
                is_completed=True
            ))
    
    db.commit()
    db.refresh(enrollment)
    return get_course_progress(courseId, db, user_id)


@router.post("/{courseId}/enroll", response_model=ApiEnvelope[dict])
def enroll_course(
    courseId: int = Path(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """加入学习（报名）"""
    course = db.query(Course).filter(Course.id == courseId, Course.is_public == True).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    exists = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.course_id == courseId
    ).first()
    
    if exists:
        raise HTTPException(status_code=409, detail="已加入学习")
    
    first_chapter = db.query(Chapter).filter(Chapter.course_id == courseId).order_by(Chapter.order_index).first()
    first_kid = None
    if first_chapter:
        first_kp = db.query(KnowledgePoint).filter(KnowledgePoint.chapter_id == first_chapter.id).order_by(KnowledgePoint.order_index).first()
        if first_kp:
            first_kid = first_kp.id
    
    enroll = Enrollment(
        user_id=user_id,
        course_id=courseId,
        last_learning_knowledge_point_id=first_kid
    )
    db.add(enroll)
    course.enrollment_count += 1
    db.commit()
    
    return ApiEnvelope(code=0, message="joined", data={"joinedAt": enroll.joined_at})
