from pydantic import BaseModel
from typing import List, Optional, Generic, TypeVar
from datetime import datetime

# 通用响应包装器（对应ApiEnvelope）
T = TypeVar('T')
class ApiEnvelope(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None

# 2.1 CourseCategory（直接用字符串枚举）
CourseCategory = str  # "CS自学" | "考研" | "职场提升"

# 2.2 CourseCard
class CourseCardOut(BaseModel):
    id: int
    title: str
    subtitle: Optional[str]
    authorName: str
    authorAvatar: str
    tags: List[str]
    forkCount: int
    enrollmentCount: int
    category: CourseCategory
    coverTone: str

    class Config:
        from_attributes = True

# 2.3 CourseDetail（包含章节/知识点/资源）
class ResourceOut(BaseModel):
    id: int
    title: str
    type: str
    url: str
    description: Optional[str]

    class Config:
        from_attributes = True

class KnowledgePointOut(BaseModel):
    id: int
    title: str
    summary: Optional[str]
    content: Optional[str]
    orderIndex: int
    estimatedMinutes: int
    keyActions: Optional[List[str]]

    class Config:
        from_attributes = True

class ChapterOut(BaseModel):
    id: int
    title: str
    overview: Optional[str]
    orderIndex: int
    knowledgePoints: List[KnowledgePointOut]
    resources: List[ResourceOut]

    class Config:
        from_attributes = True

class CourseDetailOut(BaseModel):
    id: int
    title: str
    subtitle: Optional[str]
    authorName: str
    authorAvatar: str
    tags: List[str]
    forkCount: int
    enrollmentCount: int
    category: CourseCategory
    coverTone: str
    description: Optional[str]
    authorRole: Optional[str]
    forkedFromTitle: Optional[str]
    isPublic: bool
    chapterCount: int
    knowledgePointCount: int
    estimatedHours: int
    chapters: List[ChapterOut]

    class Config:
        from_attributes = True

# 2.4 CourseProgressState
class CourseProgressStateOut(BaseModel):
    courseId: int
    selectedKnowledgePointId: Optional[int]
    lastLearningKnowledgePointId: Optional[int]
    completedKnowledgePointIds: List[int]
    joinedAt: datetime

    class Config:
        from_attributes = True

# 2.5 EnrolledCourseCard
class EnrolledCourseCardOut(BaseModel):
    id: int
    title: str
    subtitle: Optional[str]
    authorName: str
    authorAvatar: str
    coverTone: str
    completedKnowledgePointCount: int
    totalKnowledgePointCount: int
    progressPercent: int
    lastLearningKnowledgePointId: Optional[int]
    lastLearningKnowledgePointTitle: Optional[str]
    lastLearningChapterTitle: Optional[str]

    class Config:
        from_attributes = True

# 2.6 MockUser（当前用户信息）
class CurrentUserOut(BaseModel):
    id: int
    name: str
    avatar: str
    headline: Optional[str]
    streakDays: int
    enrolledCourseIds: List[int]

    class Config:
        from_attributes = True

# 进度更新请求模型
class CourseProgressPatchIn(BaseModel):
    selectedKnowledgePointId: Optional[int] = None
    lastLearningKnowledgePointId: Optional[int] = None
    completedKnowledgePointIds: Optional[List[int]] = None