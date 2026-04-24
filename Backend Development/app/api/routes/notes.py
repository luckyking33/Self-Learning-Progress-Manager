"""Protected CRUD routes for user notes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.auth import get_current_active_user
from app.db.models import Course, Note, User
from app.db.session import get_db_session
from app.schemas import ApiEnvelope, NoteCreateIn, NoteOut, NoteUpdateIn


router = APIRouter()


def _build_note_payload(note: Note) -> NoteOut:
    return NoteOut(
        id=note.id,
        courseId=note.course_id,
        courseTitle=note.course.title if note.course else None,
        title=note.title,
        content=note.content,
        createdAt=note.created_at,
        updatedAt=note.updated_at,
    )


async def _get_note_for_user(
    session: AsyncSession,
    *,
    note_id: int,
    user_id: int,
) -> Note | None:
    result = await session.execute(
        select(Note)
        .where(Note.id == note_id, Note.user_id == user_id)
        .options(selectinload(Note.course))
    )
    return result.scalar_one_or_none()


async def _validate_course(
    session: AsyncSession,
    *,
    course_id: int | None,
) -> Course | None:
    if course_id is None:
        return None
    course = await session.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found.")
    return course


@router.get("", response_model=ApiEnvelope[list[NoteOut]])
async def list_notes(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
) -> ApiEnvelope[list[NoteOut]]:
    result = await session.execute(
        select(Note)
        .where(Note.user_id == current_user.id)
        .options(selectinload(Note.course))
        .order_by(Note.updated_at.desc(), Note.id.desc())
    )
    notes = list(result.scalars())
    return ApiEnvelope(
        code=0,
        message="ok",
        data=[_build_note_payload(note) for note in notes],
    )


@router.get("/{note_id}", response_model=ApiEnvelope[NoteOut])
async def get_note(
    note_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
) -> ApiEnvelope[NoteOut]:
    note = await _get_note_for_user(session, note_id=note_id, user_id=current_user.id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found.")

    return ApiEnvelope(code=0, message="ok", data=_build_note_payload(note))


@router.post("", response_model=ApiEnvelope[NoteOut], status_code=status.HTTP_201_CREATED)
async def create_note(
    payload: NoteCreateIn,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
) -> ApiEnvelope[NoteOut]:
    await _validate_course(session, course_id=payload.course_id)

    note = Note(
        user_id=current_user.id,
        course_id=payload.course_id,
        title=payload.title,
        content=payload.content,
    )
    session.add(note)
    await session.commit()

    created_note = await _get_note_for_user(session, note_id=note.id, user_id=current_user.id)
    if created_note is None:
        raise RuntimeError("Note creation succeeded but reload failed.")

    return ApiEnvelope(code=0, message="created", data=_build_note_payload(created_note))


@router.put("/{note_id}", response_model=ApiEnvelope[NoteOut])
async def update_note(
    note_id: int,
    payload: NoteUpdateIn,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
) -> ApiEnvelope[NoteOut]:
    note = await _get_note_for_user(session, note_id=note_id, user_id=current_user.id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found.")

    if payload.course_id is not None:
        await _validate_course(session, course_id=payload.course_id)
        note.course_id = payload.course_id

    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content

    await session.commit()

    updated_note = await _get_note_for_user(session, note_id=note_id, user_id=current_user.id)
    if updated_note is None:
        raise RuntimeError("Note update succeeded but reload failed.")

    return ApiEnvelope(code=0, message="updated", data=_build_note_payload(updated_note))


@router.delete("/{note_id}", response_model=ApiEnvelope[dict[str, bool]])
async def delete_note(
    note_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
) -> ApiEnvelope[dict[str, bool]]:
    note = await _get_note_for_user(session, note_id=note_id, user_id=current_user.id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found.")

    await session.delete(note)
    await session.commit()
    return ApiEnvelope(code=0, message="deleted", data={"success": True})
