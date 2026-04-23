"""Course progress and enrollment endpoints."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.auth import get_current_active_user
from app.db.models import Chapter, CourseVersion, Enrollment, KnowledgePointProgress, User
from app.db.session import get_db_session
from app.schemas import ApiEnvelope, CourseProgressPatchIn, CourseProgressStateOut, JoinCourseOut
from app.services.course_service import get_course


router = APIRouter()


def _resolve_first_knowledge_point_id(course_chapters: list[Chapter]) -> int:
    for chapter in course_chapters:
        if chapter.knowledge_points:
            return chapter.knowledge_points[0].id
    return 0


async def _load_enrollment(
    session: AsyncSession,
    *,
    course_id: int,
    user_id: int,
) -> Enrollment | None:
    result = await session.execute(
        select(Enrollment)
        .where(Enrollment.course_id == course_id, Enrollment.user_id == user_id)
        .options(selectinload(Enrollment.knowledge_point_progress))
        .execution_options(populate_existing=True)
    )
    return result.scalar_one_or_none()


async def _ensure_course_version(
    session: AsyncSession,
    *,
    course_id: int,
) -> CourseVersion:
    result = await session.execute(
        select(CourseVersion)
        .where(CourseVersion.course_id == course_id)
        .order_by(CourseVersion.published_at.desc(), CourseVersion.id.desc())
        .limit(1)
    )
    course_version = result.scalar_one_or_none()
    if course_version is not None:
        return course_version

    course_version = CourseVersion(course_id=course_id, version_tag="v1", snapshot_data=None)
    session.add(course_version)
    await session.flush()
    return course_version


def _build_progress_payload(
    *,
    course_id: int,
    selected_id: int,
    last_learning_id: int,
    completed_ids: list[int],
    joined_at: datetime | None,
) -> CourseProgressStateOut:
    return CourseProgressStateOut(
        courseId=course_id,
        selectedKnowledgePointId=selected_id,
        lastLearningKnowledgePointId=last_learning_id,
        completedKnowledgePointIds=completed_ids,
        joinedAt=joined_at,
    )


@router.get("/{course_id}/progress", response_model=ApiEnvelope[CourseProgressStateOut])
async def get_course_progress(
    course_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
) -> ApiEnvelope[CourseProgressStateOut]:
    course = await get_course(session, course_id)
    if course is None or not course.is_public:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found.")

    first_knowledge_point_id = _resolve_first_knowledge_point_id(course.chapters)
    enrollment = await _load_enrollment(session, course_id=course_id, user_id=current_user.id)
    if enrollment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found for this course.",
        )

    completed_ids = sorted(
        progress.knowledge_point_id for progress in enrollment.knowledge_point_progress if progress.is_completed
    )
    last_learning_id = enrollment.last_learning_knowledge_point_id or first_knowledge_point_id
    payload = _build_progress_payload(
        course_id=course_id,
        selected_id=last_learning_id,
        last_learning_id=last_learning_id,
        completed_ids=completed_ids,
        joined_at=enrollment.joined_at,
    )
    return ApiEnvelope(code=0, message="ok", data=payload)


@router.patch("/{course_id}/progress", response_model=ApiEnvelope[CourseProgressStateOut])
async def patch_course_progress(
    course_id: int,
    payload: CourseProgressPatchIn = Body(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
) -> ApiEnvelope[CourseProgressStateOut]:
    course = await get_course(session, course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found.")

    enrollment = await _load_enrollment(session, course_id=course_id, user_id=current_user.id)
    if enrollment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found for this course.",
        )

    valid_knowledge_point_ids = {
        point.id for chapter in course.chapters for point in chapter.knowledge_points
    }
    first_knowledge_point_id = _resolve_first_knowledge_point_id(course.chapters)

    target_learning_id = (
        payload.lastLearningKnowledgePointId
        or payload.selectedKnowledgePointId
        or enrollment.last_learning_knowledge_point_id
        or first_knowledge_point_id
    )
    if target_learning_id and target_learning_id not in valid_knowledge_point_ids:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Knowledge point does not belong to this course.",
        )

    enrollment.last_learning_knowledge_point_id = target_learning_id

    if payload.completedKnowledgePointIds is not None:
        invalid_ids = set(payload.completedKnowledgePointIds) - valid_knowledge_point_ids
        if invalid_ids:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Knowledge point does not belong to this course.",
            )

        existing_by_id = {
            item.knowledge_point_id: item
            for item in enrollment.knowledge_point_progress
        }
        desired_ids = set(payload.completedKnowledgePointIds)

        for knowledge_point_id, item in list(existing_by_id.items()):
            if knowledge_point_id not in desired_ids:
                await session.delete(item)

        for knowledge_point_id in desired_ids:
            existing = existing_by_id.get(knowledge_point_id)
            if existing is None:
                session.add(
                    KnowledgePointProgress(
                        enrollment_id=enrollment.id,
                        knowledge_point_id=knowledge_point_id,
                        is_completed=True,
                        completed_at=datetime.now(timezone.utc),
                    )
                )
            else:
                existing.is_completed = True
                existing.completed_at = existing.completed_at or datetime.now(timezone.utc)

        total_points = len(valid_knowledge_point_ids)
        completed_count = len(desired_ids)
        enrollment.progress_percent = (
            Decimal("0.00")
            if total_points == 0
            else Decimal(str(round((completed_count / total_points) * 100, 2)))
        )

    await session.commit()

    completed_ids = (
        sorted(payload.completedKnowledgePointIds)
        if payload.completedKnowledgePointIds is not None
        else sorted(
            progress.knowledge_point_id
            for progress in enrollment.knowledge_point_progress
            if progress.is_completed
        )
    )
    last_learning_id = enrollment.last_learning_knowledge_point_id or first_knowledge_point_id
    response_payload = _build_progress_payload(
        course_id=course_id,
        selected_id=last_learning_id,
        last_learning_id=last_learning_id,
        completed_ids=completed_ids,
        joined_at=enrollment.joined_at,
    )
    return ApiEnvelope(code=0, message="updated", data=response_payload)


@router.post("/{course_id}/enroll", response_model=ApiEnvelope[JoinCourseOut])
async def enroll_course(
    course_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
) -> ApiEnvelope[JoinCourseOut]:
    course = await get_course(session, course_id)
    if course is None or not course.is_public:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found.")

    existing_enrollment = await _load_enrollment(session, course_id=course_id, user_id=current_user.id)
    if existing_enrollment is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Course already enrolled.")

    course_version = await _ensure_course_version(session, course_id=course.id)
    first_knowledge_point_id = _resolve_first_knowledge_point_id(course.chapters)
    enrollment = Enrollment(
        user_id=current_user.id,
        course_id=course_id,
        course_version_id=course_version.id,
        last_learning_knowledge_point_id=first_knowledge_point_id or None,
        progress_percent=Decimal("0.00"),
    )
    session.add(enrollment)
    await session.commit()
    await session.refresh(enrollment)

    return ApiEnvelope(
        code=0,
        message="joined",
        data=JoinCourseOut(joinedAt=enrollment.joined_at),
    )
