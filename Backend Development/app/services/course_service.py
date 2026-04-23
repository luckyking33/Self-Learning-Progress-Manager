"""Course service helpers."""

from __future__ import annotations

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Chapter, Course, CourseVersion, KnowledgePoint, Resource
from app.schemas import CourseCreate


def _public_course_list_query() -> Select[tuple[Course]]:
    return (
        select(Course)
        .where(Course.is_public.is_(True))
        .options(
            selectinload(Course.author),
            selectinload(Course.chapters).selectinload(Chapter.knowledge_points),
            selectinload(Course.forks),
            selectinload(Course.enrollments),
        )
        .order_by(Course.id)
    )


def _course_detail_query(course_id: int) -> Select[tuple[Course]]:
    return (
        select(Course)
        .where(Course.id == course_id)
        .options(
            selectinload(Course.author),
            selectinload(Course.versions),
            selectinload(Course.forks),
            selectinload(Course.enrollments),
            selectinload(Course.chapters).selectinload(Chapter.knowledge_points),
            selectinload(Course.chapters).selectinload(Chapter.resources),
            selectinload(Course.forked_from),
        )
    )


async def list_public_courses(session: AsyncSession) -> list[Course]:
    result = await session.execute(_public_course_list_query())
    return list(result.scalars().unique())


async def get_course(session: AsyncSession, course_id: int) -> Course | None:
    """Load a course with author, versions, chapters, knowledge points, and resources."""

    result = await session.execute(_course_detail_query(course_id))
    return result.scalar_one_or_none()


async def get_course_version_for_enrollment(
    session: AsyncSession,
    course: Course,
) -> CourseVersion | None:
    """Return the latest published version for enrollment binding."""

    if course.versions:
        return course.versions[-1]

    result = await session.execute(
        select(CourseVersion)
        .where(CourseVersion.course_id == course.id)
        .order_by(CourseVersion.published_at.desc(), CourseVersion.id.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def create_course(
    session: AsyncSession,
    *,
    author_id: int,
    payload: CourseCreate,
) -> Course:
    """Create a course draft with nested chapters, knowledge points, and resources."""

    course = Course(
        author_id=author_id,
        title=payload.title,
        subtitle=payload.subtitle,
        description=payload.description,
        tags=payload.tags,
        category=payload.category,
        cover_tone=payload.cover_tone,
        is_public=payload.is_public,
    )

    for chapter_payload in payload.chapters:
        chapter = Chapter(
            title=chapter_payload.title,
            description=chapter_payload.description,
            order_index=chapter_payload.order_index,
        )

        for knowledge_point_payload in chapter_payload.knowledge_points:
            chapter.knowledge_points.append(
                KnowledgePoint(
                    title=knowledge_point_payload.title,
                    description=knowledge_point_payload.description,
                    order_index=knowledge_point_payload.order_index,
                )
            )

        for resource_payload in chapter_payload.resources:
            chapter.resources.append(
                Resource(
                    title=resource_payload.title,
                    url=str(resource_payload.url),
                    resource_type=resource_payload.resource_type,
                    description=resource_payload.description,
                    order_index=resource_payload.order_index,
                )
            )

        course.chapters.append(chapter)

    session.add(course)
    await session.commit()
    await session.refresh(course)

    created_course = await get_course(session, course.id)
    if created_course is None:
        raise RuntimeError("Course creation succeeded but reload failed.")

    return created_course


async def fork_course(
    session: AsyncSession,
    *,
    source_course_id: int,
    source_version_id: int,
    target_author_id: int,
    is_public: bool = False,
) -> Course:
    """TODO: Implement deep-copy forking from a published course version.

    Recommended flow for the follow-up implementation:
    1. Validate that `source_version_id` belongs to `source_course_id`.
    2. Load the published version snapshot, not the author's live draft.
    3. Create a new `Course` with `forked_from_id=source_course_id`.
    4. Deep-copy chapters, knowledge points, and resources with fresh primary keys.
    5. Do not copy `Enrollment` or `KnowledgePointProgress`.
    6. Optionally create an initial version for the forked course after the structure is copied.
    """

    raise NotImplementedError("fork_course is intentionally left as a template placeholder.")
