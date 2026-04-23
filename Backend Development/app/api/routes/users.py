"""User profile and enrollment endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.auth import get_current_active_user
from app.db.models import Chapter, Course, Enrollment, User
from app.db.session import get_db_session
from app.schemas import ApiEnvelope, CurrentUserOut, EnrolledCourseCardOut


router = APIRouter()


def _resolve_last_learning_meta(enrollment: Enrollment) -> tuple[int, str, str]:
    course = enrollment.course
    if course is None:
        return 0, "Start learning", "Overview"

    fallback_chapter_title = course.chapters[0].title if course.chapters else "Overview"
    fallback_point_title = (
        course.chapters[0].knowledge_points[0].title
        if course.chapters and course.chapters[0].knowledge_points
        else "Start learning"
    )
    last_id = enrollment.last_learning_knowledge_point_id or 0

    if last_id == 0:
        return 0, fallback_point_title, fallback_chapter_title

    for chapter in course.chapters:
        for point in chapter.knowledge_points:
            if point.id == last_id:
                return last_id, point.title, chapter.title

    return last_id, fallback_point_title, fallback_chapter_title


@router.get("/me", response_model=ApiEnvelope[CurrentUserOut])
async def get_current_user_profile(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
) -> ApiEnvelope[CurrentUserOut]:
    enrolled_ids_result = await session.execute(
        select(Enrollment.course_id)
        .where(Enrollment.user_id == current_user.id)
        .order_by(Enrollment.course_id)
    )
    enrolled_course_ids = list(enrolled_ids_result.scalars())

    payload = CurrentUserOut(
        id=current_user.id,
        name=current_user.username,
        avatar=current_user.avatar,
        headline=current_user.headline,
        streakDays=current_user.streak_days,
        enrolledCourseIds=enrolled_course_ids,
    )
    return ApiEnvelope(code=0, message="ok", data=payload)


@router.get("/me/enrollments", response_model=ApiEnvelope[list[EnrolledCourseCardOut]])
async def get_enrolled_courses(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
) -> ApiEnvelope[list[EnrolledCourseCardOut]]:
    result = await session.execute(
        select(Enrollment)
        .where(Enrollment.user_id == current_user.id)
        .options(
            selectinload(Enrollment.course).selectinload(Course.author),
            selectinload(Enrollment.course).selectinload(Course.chapters).selectinload(Chapter.knowledge_points),
            selectinload(Enrollment.knowledge_point_progress),
        )
        .order_by(Enrollment.course_id)
    )
    enrollments = list(result.scalars().unique())

    cards: list[EnrolledCourseCardOut] = []
    for enrollment in enrollments:
        course = enrollment.course
        if course is None:
            continue

        total_points = sum(len(chapter.knowledge_points) for chapter in course.chapters)
        completed_count = sum(1 for item in enrollment.knowledge_point_progress if item.is_completed)
        progress_percent = 0 if total_points == 0 else round((completed_count / total_points) * 100)
        last_id, last_title, chapter_title = _resolve_last_learning_meta(enrollment)
        author_name = course.author.username if course.author else "STAR Author"
        author_avatar = course.author.avatar if course.author else "ST"

        cards.append(
            EnrolledCourseCardOut(
                id=course.id,
                title=course.title,
                subtitle=course.subtitle,
                authorName=author_name,
                authorAvatar=author_avatar,
                coverTone=course.cover_tone,
                completedKnowledgePointCount=completed_count,
                totalKnowledgePointCount=total_points,
                progressPercent=progress_percent,
                lastLearningKnowledgePointId=last_id,
                lastLearningKnowledgePointTitle=last_title,
                lastLearningChapterTitle=chapter_title,
            )
        )

    return ApiEnvelope(code=0, message="ok", data=cards)
