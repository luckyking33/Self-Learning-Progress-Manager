import os
os.environ["PYTHONUNBUFFERED"] = "1"
from fastapi import FastAPI, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from SQLconnet import SessionLocal, engine
from models import Base, User, Course, Enrollment, Chapter, KnowledgePoint, KnowledgePointProgress, Resource
from schemas import (
    ApiEnvelope,
    CourseCardOut,
    CourseDetailOut,
    CourseProgressStateOut,
    CurrentUserOut,
    EnrolledCourseCardOut,
    CourseProgressPatchIn
)

# 延迟初始化数据库表，只在首次使用时创建
_db_initialized = False
def init_db():
    global _db_initialized
    if not _db_initialized:
        Base.metadata.create_all(bind=engine)
        _db_initialized = True

app = FastAPI(title="STAR 自学进度管理器 API", version="1.0")

# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 模拟用户登录
def get_current_user_id():
    return 7

# ===================== 首页自动跳转到接口文档 =====================
@app.get("/")
def home():
    init_db()  # 初始化数据库
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")

# ===================== 3.1 获取当前用户信息 =====================
@app.get("/users/me", response_model=ApiEnvelope[CurrentUserOut])
def read_current_user(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
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

# ===================== 3.2 获取课程广场列表 =====================
@app.get("/courses", response_model=ApiEnvelope[list[CourseCardOut]])
def read_course_list(
    keyword: str | None = Query(None),
    category: str | None = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Course)
    if keyword:
        query = query.filter(
            Course.title.ilike(f"%{keyword}%") |
            Course.subtitle.ilike(f"%{keyword}%") |
            Course.author_name.ilike(f"%{keyword}%") |
            Course.tags.any(keyword)
        )
    if category:
        query = query.filter(Course.category == category)
    
    query = query.filter(Course.is_public == True)
    courses = query.all()
    
    return ApiEnvelope(code=0, message="ok", data=courses)

# ===================== 3.3 获取课程详情 =====================
@app.get("/courses/{courseId}", response_model=ApiEnvelope[CourseDetailOut])
def read_course_detail(
    courseId: int = Path(...),
    db: Session = Depends(get_db)
):
    from sqlalchemy.orm import selectinload
    course = db.query(Course).options(
        selectinload(Course.chapters).selectinload(Chapter.knowledge_points),
        selectinload(Course.chapters).selectinload(Chapter.resources)
    ).filter(Course.id == courseId).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    return ApiEnvelope(code=0, message="ok", data=course)

# ===================== 3.4 获取课程学习进度 =====================
@app.get("/courses/{courseId}/progress", response_model=ApiEnvelope[CourseProgressStateOut])
def read_course_progress(
    courseId: int = Path(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
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

# ===================== 3.5 更新学习进度 =====================
@app.patch("/courses/{courseId}/progress", response_model=ApiEnvelope[CourseProgressStateOut])
def patch_course_progress(
    courseId: int = Path(...),
    progress_in: CourseProgressPatchIn = Depends(),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
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
    return read_course_progress(courseId, db, user_id)

# ===================== 3.6 加入学习 =====================
@app.post("/courses/{courseId}/enroll", response_model=ApiEnvelope[dict])
def post_course_enroll(
    courseId: int = Path(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
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
        first_kp = db.query(KnowledgePoint).filter(KnowledgePoint.chapter_id == first_chapter.id).first()
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

# ===================== 3.7 获取已报名课程 =====================
@app.get("/users/me/enrollments", response_model=ApiEnvelope[list[EnrolledCourseCardOut]])
def read_enrolled_courses(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    enrollments = db.query(Enrollment).filter(Enrollment.user_id == user_id).all()
    result = []
    
    for e in enrollments:
        c = db.query(Course).filter(Course.id == e.course_id).first()
        if not c: continue
        
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