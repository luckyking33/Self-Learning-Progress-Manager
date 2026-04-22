import client from "@/api/client";
import type {
  ApiEnvelope,
  CourseCard,
  CourseDetail,
  CourseProgressState,
  CourseCategory,
  EnrolledCourseCard,
  MockUser,
} from "@/types/course";

export async function fetchCurrentUser(): Promise<MockUser> {
  const response = await client.get<ApiEnvelope<MockUser>>("/users/me");
  return response.data.data;
}

export async function fetchCourseList(params?: {
  keyword?: string;
  category?: CourseCategory | null;
}): Promise<CourseCard[]> {
  const response = await client.get<ApiEnvelope<CourseCard[]>>("/courses", {
    params,
  });
  return response.data.data;
}

export async function fetchCourseDetail(courseId: number): Promise<CourseDetail> {
  const response = await client.get<ApiEnvelope<CourseDetail>>(`/courses/${courseId}`);
  return response.data.data;
}

export async function fetchCourseProgress(courseId: number): Promise<CourseProgressState> {
  const response = await client.get<ApiEnvelope<CourseProgressState>>(`/courses/${courseId}/progress`);
  return response.data.data;
}

export async function updateCourseProgress(
  courseId: number,
  payload: Partial<
    Pick<
      CourseProgressState,
      "selectedKnowledgePointId" | "lastLearningKnowledgePointId" | "completedKnowledgePointIds"
    >
  >,
): Promise<CourseProgressState> {
  const response = await client.patch<ApiEnvelope<CourseProgressState>>(
    `/courses/${courseId}/progress`,
    payload,
  );
  return response.data.data;
}

export async function joinCourse(courseId: number): Promise<{ joinedAt: string | null }> {
  const response = await client.post<ApiEnvelope<{ joinedAt: string | null }>>(
    `/courses/${courseId}/enroll`,
  );
  return response.data.data;
}

export async function fetchEnrolledCourses(): Promise<EnrolledCourseCard[]> {
  const response = await client.get<ApiEnvelope<EnrolledCourseCard[]>>("/users/me/enrollments");
  return response.data.data;
}
