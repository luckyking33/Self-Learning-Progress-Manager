export type CourseCategory = "CS自学" | "考研" | "职场提升";

export type JoinState = "idle" | "loading" | "success";

export interface CourseResource {
  id: number;
  title: string;
  type: "article" | "video" | "docs" | "repo";
  url: string;
  description: string;
}

export interface KnowledgePoint {
  id: number;
  title: string;
  summary: string;
  content: string;
  orderIndex: number;
  estimatedMinutes: number;
  keyActions: string[];
}

export interface Chapter {
  id: number;
  title: string;
  overview: string;
  orderIndex: number;
  knowledgePoints: KnowledgePoint[];
  resources: CourseResource[];
}

export interface CourseCard {
  id: number;
  title: string;
  subtitle: string;
  authorName: string;
  authorAvatar: string;
  tags: string[];
  forkCount: number;
  enrollmentCount: number;
  category: CourseCategory;
  coverTone: string;
}

export interface CourseDetail extends CourseCard {
  description: string;
  authorRole: string;
  forkedFromTitle: string | null;
  isPublic: boolean;
  chapterCount: number;
  knowledgePointCount: number;
  estimatedHours: number;
  chapters: Chapter[];
}

export interface CourseProgressState {
  courseId: number;
  selectedKnowledgePointId: number;
  lastLearningKnowledgePointId: number;
  completedKnowledgePointIds: number[];
  joinedAt: string | null;
}

export interface EnrolledCourseCard {
  id: number;
  title: string;
  subtitle: string;
  authorName: string;
  authorAvatar: string;
  coverTone: string;
  completedKnowledgePointCount: number;
  totalKnowledgePointCount: number;
  progressPercent: number;
  lastLearningKnowledgePointId: number;
  lastLearningKnowledgePointTitle: string;
  lastLearningChapterTitle: string;
}

export interface MockUser {
  id: number;
  name: string;
  avatar: string;
  headline: string;
  streakDays: number;
  enrolledCourseIds: number[];
}

export interface ApiEnvelope<T> {
  code: number;
  message: string;
  data: T;
}
