"""Course catalog and detail endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Chapter, Course, KnowledgePoint, Resource
from app.db.session import get_db_session
from app.schemas import (
    ApiEnvelope,
    ChapterOut,
    CourseCardOut,
    CourseCategory,
    CourseDetailOut,
    CourseResourceOut,
    KnowledgePointOut,
)
from app.services.course_service import get_course, list_public_courses


router = APIRouter()


def _map_resource_type(resource: Resource) -> str:
    value = resource.resource_type.lower()
    if value in {"video", "repo", "docs", "article"}:
        return value
    if value == "link":
        return "docs"
    return "article"


def _build_author_name(course: Course) -> str:
    return course.author.username if course.author else "STAR Author"


def _build_author_avatar(course: Course) -> str:
    return course.author.avatar if course.author else "ST"


def _build_author_role(course: Course) -> str:
    if course.author and course.author.headline:
        return course.author.headline
    return "Community course author"


def _normalize_category(course: Course) -> CourseCategory:
    if course.category in {"CS自学", "考研", "职场提升"}:
        return course.category
    return "CS自学"


def _build_course_card(course: Course) -> CourseCardOut:
    return CourseCardOut(
        id=course.id,
        title=course.title,
        subtitle=course.subtitle,
        authorName=_build_author_name(course),
        authorAvatar=_build_author_avatar(course),
        tags=course.tags,
        forkCount=len(course.forks),
        enrollmentCount=len(course.enrollments),
        category=_normalize_category(course),
        coverTone=course.cover_tone,
    )


def _build_knowledge_point(point: KnowledgePoint) -> KnowledgePointOut:
    summary = point.description or f"Summary for {point.title}."
    content = point.description or f"Detailed content for {point.title} is pending."
    return KnowledgePointOut(
        id=point.id,
        title=point.title,
        summary=summary,
        content=content,
        orderIndex=point.order_index,
        estimatedMinutes=20,
        keyActions=["Read", "Practice", "Review"],
    )


def _build_chapter(chapter: Chapter) -> ChapterOut:
    return ChapterOut(
        id=chapter.id,
        title=chapter.title,
        overview=chapter.description or f"Overview for {chapter.title}.",
        orderIndex=chapter.order_index,
        knowledgePoints=[_build_knowledge_point(point) for point in chapter.knowledge_points],
        resources=[
            CourseResourceOut(
                id=resource.id,
                title=resource.title,
                type=_map_resource_type(resource),
                url=resource.url,
                description=resource.description or f"Resource for {resource.title}.",
            )
            for resource in chapter.resources
        ],
    )


def _build_course_detail(course: Course) -> CourseDetailOut:
    course_card = _build_course_card(course)
    knowledge_point_count = sum(len(chapter.knowledge_points) for chapter in course.chapters)
    return CourseDetailOut(
        **course_card.model_dump(),
        description=course.description or f"Description for {course.title} is pending.",
        authorRole=_build_author_role(course),
        forkedFromTitle=course.forked_from.title if course.forked_from else None,
        isPublic=course.is_public,
        chapterCount=len(course.chapters),
        knowledgePointCount=knowledge_point_count,
        estimatedHours=max(1, knowledge_point_count // 2 or len(course.chapters)),
        chapters=[_build_chapter(chapter) for chapter in course.chapters],
    )


@router.get("", response_model=ApiEnvelope[list[CourseCardOut]])
async def get_course_list(
    keyword: str | None = Query(default=None),
    category: CourseCategory | None = Query(default=None),
    session: AsyncSession = Depends(get_db_session),
) -> ApiEnvelope[list[CourseCardOut]]:
    courses = await list_public_courses(session)
    cards = [_build_course_card(course) for course in courses]

    if keyword:
        keyword_lower = keyword.lower()
        cards = [
            card
            for card in cards
            if keyword_lower in card.title.lower()
            or keyword_lower in card.subtitle.lower()
            or keyword_lower in card.authorName.lower()
            or keyword_lower in " ".join(card.tags).lower()
        ]

    if category:
        cards = [card for card in cards if card.category == category]

    return ApiEnvelope(code=0, message="ok", data=cards)


@router.get("/{course_id}", response_model=ApiEnvelope[CourseDetailOut])
async def get_course_detail(
    course_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> ApiEnvelope[CourseDetailOut]:
    course = await get_course(session, course_id)
    if course is None or not course.is_public:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found.",
        )

    return ApiEnvelope(code=0, message="ok", data=_build_course_detail(course))
