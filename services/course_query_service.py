from sqlalchemy.orm import Session, selectinload
from models import Course, Chapter, KnowledgePoint, Resource, Enrollment, KnowledgePointProgress, User
from schemas import CourseCardOut, CourseDetailOut, EnrolledCourseCardOut
from sqlalchemy import func

# 1. 获取课程广场列表
def get_course_list(db: Session, keyword: Optional[str] = None, category: Optional[str] = None):
    query = db.query(Course)
    # 关键词过滤（标题/副标题/作者/标签）
    if keyword:
        query = query.filter(
            (Course.title.ilike(f"%{keyword}%")) |
            (Course.subtitle.ilike(f"%{keyword}%")) |
            (Course.author_name.ilike(f"%{keyword}%")) |
            (Course.tags.any(keyword))
        )
    # 分类过滤
    if category:
        query = query.filter(Course.category == category)
    # 只返回公开课程
    query = query.filter(Course.is_public == True)
    courses = query.all()
    return [CourseCardOut.from_orm(course) for course in courses]

# 2. 获取课程详情
def get_course_detail(db: Session, course_id: int):
    course = db.query(Course).options(
        selectinload(Course.chapters).selectinload(Chapter.knowledge_points),
        selectinload(Course.chapters).selectinload(Chapter.resources)
    ).filter(Course.id == course_id).first()
    if not course:
        return None
    return CourseDetailOut.from_orm(course)

# 3. 获取用户已报名课程列表（聚合进度）
def get_enrolled_courses(db: Session, user_id: int):
    # 1. 查询用户报名记录
    enrollments = db.query(Enrollment).filter(Enrollment.user_id == user_id).all()
    enrolled_cards = []
    for enrollment in enrollments:
        # 2. 获取课程基础信息
        course = db.query(Course).filter(Course.id == enrollment.course_id).first()
        if not course:
            continue
        # 3. 计算已完成知识点数
        completed_kp_count = db.query(KnowledgePointProgress).filter(
            KnowledgePointProgress.enrollment_id == enrollment.id,
            KnowledgePointProgress.is_completed == True
        ).count()
        total_kp_count = course.knowledge_point_count or 0
        # 4. 计算进度百分比
        progress_percent = round((completed_kp_count / total_kp_count) * 100) if total_kp_count > 0 else 0
        # 5. 获取上次学习的知识点/章节标题
        last_kp_title = None
        last_chapter_title = None
        if enrollment.last_learning_knowledge_point_id:
            kp = db.query(KnowledgePoint).filter(KnowledgePoint.id == enrollment.last_learning_knowledge_point_id).first()
            if kp:
                last_kp_title = kp.title
                chapter = db.query(Chapter).filter(Chapter.id == kp.chapter_id).first()
                if chapter:
                    last_chapter_title = chapter.title
        # 6. 构造返回对象
        enrolled_card = EnrolledCourseCardOut(
            id=course.id,
            title=course.title,
            subtitle=course.subtitle,
            authorName=course.author_name,
            authorAvatar=course.author_avatar,
            coverTone=course.cover_tone,
            completedKnowledgePointCount=completed_kp_count,
            totalKnowledgePointCount=total_kp_count,
            progressPercent=progress_percent,
            lastLearningKnowledgePointId=enrollment.last_learning_knowledge_point_id,
            lastLearningKnowledgePointTitle=last_kp_title,
            lastLearningChapterTitle=last_chapter_title
        )
        enrolled_cards.append(enrolled_card)
    return enrolled_cards

# 4. 获取当前用户信息
def get_current_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    # 获取用户已报名课程ID
    enrolled_course_ids = db.query(Enrollment.course_id).filter(Enrollment.user_id == user_id).all()
    enrolled_course_ids = [item[0] for item in enrolled_course_ids]
    return CurrentUserOut(
        id=user.id,
        name=user.name,
        avatar=user.avatar,
        headline=user.headline,
        streakDays=user.streak_days,
        enrolledCourseIds=enrolled_course_ids
    )