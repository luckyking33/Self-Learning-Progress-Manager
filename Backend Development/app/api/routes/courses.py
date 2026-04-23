"""Course management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from models import Course, Chapter, KnowledgePoint, Enrollment, KnowledgePointProgress
from schemas import ApiEnvelope, CourseCardOut, CourseDetailOut

router = APIRouter()


@router.get("", response_model=ApiEnvelope[list[CourseCardOut]])
def get_course_list(
    keyword: str | None = Query(None),
    category: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """获取课程广场列表"""
    query = db.query(Course)
    if keyword:
        query = query.filter(
            (Course.title.ilike(f"%{keyword}%")) |
            (Course.subtitle.ilike(f"%{keyword}%")) |
            (Course.author_name.ilike(f"%{keyword}%")) |
            (Course.tags.any(keyword))
        )
    if category:
        query = query.filter(Course.category == category)
    
    query = query.filter(Course.is_public == True)
    courses = query.all()
    
    return ApiEnvelope(code=0, message="ok", data=courses)


@router.get("/{courseId}", response_model=ApiEnvelope[CourseDetailOut])
def get_course_detail(
    courseId: int = Path(...),
    db: Session = Depends(get_db),
):
    """获取课程详情"""
    course = db.query(Course).options(
        selectinload(Course.chapters).selectinload(Chapter.knowledge_points),
        selectinload(Course.chapters).selectinload(Chapter.resources)
    ).filter(Course.id == courseId).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    return ApiEnvelope(code=0, message="ok", data=course)
