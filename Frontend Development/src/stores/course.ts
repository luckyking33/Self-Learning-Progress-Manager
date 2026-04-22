import { defineStore } from "pinia";

import {
  fetchCourseDetail,
  fetchCourseList,
  fetchCourseProgress,
  joinCourse,
  updateCourseProgress,
} from "@/api/course";
import { useUserStore } from "@/stores/user";
import type {
  Chapter,
  CourseCard,
  CourseCategory,
  CourseDetail,
  CourseProgressState,
  JoinState,
  KnowledgePoint,
} from "@/types/course";

function normalizeTargetKnowledgePointId(
  course: CourseDetail,
  progress: CourseProgressState,
  preferredKnowledgePointId?: number | null,
): number {
  const allKnowledgePoints = course.chapters.flatMap((chapter) => chapter.knowledgePoints);
  const candidateId =
    preferredKnowledgePointId ??
    progress.lastLearningKnowledgePointId ??
    progress.selectedKnowledgePointId;

  return (
    allKnowledgePoints.find((knowledgePoint) => knowledgePoint.id === candidateId)?.id ??
    allKnowledgePoints[0]?.id ??
    0
  );
}

export const useCourseStore = defineStore("course", {
  state: (): {
    courseCatalog: CourseCard[];
    course: CourseDetail | null;
    progress: CourseProgressState | null;
    isCatalogLoading: boolean;
    isLoading: boolean;
    joinState: JoinState;
  } => ({
    courseCatalog: [],
    course: null,
    progress: null,
    isCatalogLoading: false,
    isLoading: false,
    joinState: "idle",
  }),
  getters: {
    allKnowledgePoints(state): KnowledgePoint[] {
      if (!state.course) {
        return [];
      }

      return state.course.chapters.flatMap((chapter) => chapter.knowledgePoints);
    },
    selectedKnowledgePoint(): KnowledgePoint | null {
      if (!this.progress) {
        return null;
      }

      return (
        this.allKnowledgePoints.find(
          (knowledgePoint) => knowledgePoint.id === this.progress?.selectedKnowledgePointId,
        ) ?? null
      );
    },
    selectedChapter(): Chapter | null {
      if (!this.progress || !this.course) {
        return null;
      }

      return (
        this.course.chapters.find((chapter) =>
          chapter.knowledgePoints.some(
            (knowledgePoint) => knowledgePoint.id === this.progress?.selectedKnowledgePointId,
          ),
        ) ?? null
      );
    },
    progressPercent(): number {
      if (!this.progress || this.allKnowledgePoints.length === 0) {
        return 0;
      }

      return Math.round(
        (this.progress.completedKnowledgePointIds.length / this.allKnowledgePoints.length) * 100,
      );
    },
    completedCount(): number {
      return this.progress?.completedKnowledgePointIds.length ?? 0;
    },
    availableCategories(): CourseCategory[] {
      return Array.from(new Set(this.courseCatalog.map((course) => course.category)));
    },
  },
  actions: {
    async loadCourseCatalog() {
      this.isCatalogLoading = true;
      this.courseCatalog = await fetchCourseList();
      this.isCatalogLoading = false;
      return this.courseCatalog;
    },
    async loadCourse(courseId = 101, preferredKnowledgePointId?: number | null) {
      this.isLoading = true;
      const [course, progress] = await Promise.all([
        fetchCourseDetail(courseId),
        fetchCourseProgress(courseId),
      ]);

      const selectedKnowledgePointId = normalizeTargetKnowledgePointId(
        course,
        progress,
        preferredKnowledgePointId,
      );

      this.course = course;
      this.progress = {
        ...progress,
        selectedKnowledgePointId,
        lastLearningKnowledgePointId: selectedKnowledgePointId,
      };
      this.isLoading = false;

      if (preferredKnowledgePointId) {
        await updateCourseProgress(courseId, {
          selectedKnowledgePointId,
          lastLearningKnowledgePointId: selectedKnowledgePointId,
        });
      }
    },
    async syncProgress() {
      if (!this.course || !this.progress) {
        return;
      }

      this.progress = await updateCourseProgress(this.course.id, {
        selectedKnowledgePointId: this.progress.selectedKnowledgePointId,
        lastLearningKnowledgePointId: this.progress.lastLearningKnowledgePointId,
        completedKnowledgePointIds: this.progress.completedKnowledgePointIds,
      });

      const selectedKnowledgePoint = this.selectedKnowledgePoint;
      const selectedChapter = this.selectedChapter;
      if (selectedKnowledgePoint && selectedChapter) {
        useUserStore().patchEnrolledCourseProgress({
          courseId: this.course.id,
          completedKnowledgePointCount: this.progress.completedKnowledgePointIds.length,
          totalKnowledgePointCount: this.course.knowledgePointCount,
          lastLearningKnowledgePointId: this.progress.lastLearningKnowledgePointId,
          lastLearningKnowledgePointTitle: selectedKnowledgePoint.title,
          lastLearningChapterTitle: selectedChapter.title,
        });
      }
    },
    async selectKnowledgePoint(knowledgePointId: number) {
      if (!this.progress) {
        return;
      }

      this.progress.selectedKnowledgePointId = knowledgePointId;
      this.progress.lastLearningKnowledgePointId = knowledgePointId;
      await this.syncProgress();
    },
    async toggleKnowledgePointCompleted(knowledgePointId: number) {
      if (!this.progress) {
        return;
      }

      const index = this.progress.completedKnowledgePointIds.indexOf(knowledgePointId);
      if (index >= 0) {
        this.progress.completedKnowledgePointIds.splice(index, 1);
      } else {
        this.progress.completedKnowledgePointIds.push(knowledgePointId);
      }

      await this.syncProgress();
    },
    async joinCourse() {
      if (!this.course || !this.progress || this.joinState === "loading") {
        return;
      }

      this.joinState = "loading";
      const response = await joinCourse(this.course.id);
      this.progress.joinedAt = response.joinedAt;
      await useUserStore().refreshEnrollmentState();
      this.joinState = "success";

      window.setTimeout(() => {
        this.joinState = "idle";
      }, 1600);
    },
  },
});
