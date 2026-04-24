"""Pydantic schemas for STAR CRUD, auth, notes, and frontend-facing API responses."""

from __future__ import annotations

from datetime import datetime
from typing import Generic, Literal, TypeVar

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, EmailStr, Field


T = TypeVar("T")
CourseCategory = Literal["CS自学", "考研", "职场提升"]
CourseResourceType = Literal["article", "video", "docs", "repo"]


class InputSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ApiEnvelope(BaseModel, Generic[T]):
    code: int
    message: str
    data: T


class ResourceCreate(InputSchema):
    title: str = Field(min_length=1, max_length=255)
    url: AnyHttpUrl
    resource_type: str = Field(default="link", min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=5000)
    order_index: int = Field(default=0, ge=0)


class ResourceRead(ReadSchema):
    id: int
    chapter_id: int
    title: str
    url: AnyHttpUrl
    resource_type: str
    description: str | None
    order_index: int
    created_at: datetime
    updated_at: datetime


class NestedKnowledgePointCreate(InputSchema):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=5000)
    order_index: int = Field(ge=0)


class KnowledgePointCreate(NestedKnowledgePointCreate):
    chapter_id: int = Field(gt=0)


class KnowledgePointUpdate(InputSchema):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=5000)
    order_index: int | None = Field(default=None, ge=0)


class KnowledgePointRead(ReadSchema):
    id: int
    chapter_id: int
    title: str
    description: str | None
    order_index: int
    created_at: datetime
    updated_at: datetime


class ChapterCreate(InputSchema):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=5000)
    order_index: int = Field(ge=0)
    knowledge_points: list[NestedKnowledgePointCreate] = Field(default_factory=list)
    resources: list[ResourceCreate] = Field(default_factory=list)


class ChapterRead(ReadSchema):
    id: int
    course_id: int
    title: str
    description: str | None
    order_index: int
    created_at: datetime
    updated_at: datetime
    knowledge_points: list[KnowledgePointRead] = Field(default_factory=list)
    resources: list[ResourceRead] = Field(default_factory=list)


class CourseVersionRead(ReadSchema):
    id: int
    course_id: int
    version_tag: str
    snapshot_data: dict | None
    published_at: datetime


class CourseCreate(InputSchema):
    title: str = Field(min_length=1, max_length=255)
    subtitle: str = Field(default="", max_length=255)
    description: str | None = Field(default=None, max_length=10000)
    tags: list[str] = Field(default_factory=list, max_length=8)
    category: CourseCategory = "CS自学"
    cover_tone: str = Field(default="from-sky-100 via-white to-cyan-50", max_length=255)
    is_public: bool = False
    chapters: list[ChapterCreate] = Field(default_factory=list)


class CourseUpdate(InputSchema):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    subtitle: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=10000)
    tags: list[str] | None = None
    category: CourseCategory | None = None
    cover_tone: str | None = Field(default=None, max_length=255)
    is_public: bool | None = None


class CourseRead(ReadSchema):
    id: int
    author_id: int
    forked_from_id: int | None
    title: str
    subtitle: str
    description: str | None
    tags: list[str]
    category: CourseCategory
    cover_tone: str
    is_public: bool
    created_at: datetime
    updated_at: datetime
    versions: list[CourseVersionRead] = Field(default_factory=list)
    chapters: list[ChapterRead] = Field(default_factory=list)


class CourseResourceOut(BaseModel):
    id: int
    title: str
    type: CourseResourceType
    url: str
    description: str


class KnowledgePointOut(BaseModel):
    id: int
    title: str
    summary: str
    content: str
    orderIndex: int
    estimatedMinutes: int
    keyActions: list[str]


class ChapterOut(BaseModel):
    id: int
    title: str
    overview: str
    orderIndex: int
    knowledgePoints: list[KnowledgePointOut]
    resources: list[CourseResourceOut]


class CourseCardOut(BaseModel):
    id: int
    title: str
    subtitle: str
    authorName: str
    authorAvatar: str
    tags: list[str]
    forkCount: int
    enrollmentCount: int
    category: CourseCategory
    coverTone: str


class CourseDetailOut(CourseCardOut):
    description: str
    authorRole: str
    forkedFromTitle: str | None
    isPublic: bool
    chapterCount: int
    knowledgePointCount: int
    estimatedHours: int
    chapters: list[ChapterOut]


class CourseProgressStateOut(BaseModel):
    courseId: int
    selectedKnowledgePointId: int
    lastLearningKnowledgePointId: int
    completedKnowledgePointIds: list[int]
    joinedAt: datetime | None


class EnrolledCourseCardOut(BaseModel):
    id: int
    title: str
    subtitle: str
    authorName: str
    authorAvatar: str
    coverTone: str
    completedKnowledgePointCount: int
    totalKnowledgePointCount: int
    progressPercent: int
    lastLearningKnowledgePointId: int
    lastLearningKnowledgePointTitle: str
    lastLearningChapterTitle: str


class CurrentUserOut(BaseModel):
    id: int
    name: str
    avatar: str
    headline: str
    streakDays: int
    enrolledCourseIds: list[int]


class CourseProgressPatchIn(InputSchema):
    selectedKnowledgePointId: int | None = None
    lastLearningKnowledgePointId: int | None = None
    completedKnowledgePointIds: list[int] | None = None


class JoinCourseOut(BaseModel):
    joinedAt: datetime


class UserRegisterIn(InputSchema):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=5, max_length=128)


class AuthTokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int


class NoteCreateIn(InputSchema):
    course_id: int | None = Field(default=None, gt=0)
    title: str = Field(default="Untitled Note", min_length=1, max_length=255)
    content: str = Field(default="", max_length=100_000)


class NoteUpdateIn(InputSchema):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = Field(default=None, max_length=100_000)
    course_id: int | None = Field(default=None, gt=0)


class NoteOut(BaseModel):
    id: int
    courseId: int | None
    courseTitle: str | None
    title: str
    content: str
    createdAt: datetime
    updatedAt: datetime
