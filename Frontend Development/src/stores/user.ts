import { defineStore } from "pinia";

import { fetchCurrentUser, fetchEnrolledCourses } from "@/api/course";
import type { EnrolledCourseCard, MockUser } from "@/types/course";

export const useUserStore = defineStore("user", {
  state: (): {
    currentUser: MockUser | null;
    enrolledCourses: EnrolledCourseCard[];
    isLoading: boolean;
    hasBootstrapped: boolean;
  } => ({
    currentUser: null,
    enrolledCourses: [],
    isLoading: false,
    hasBootstrapped: false,
  }),
  getters: {
    isEnrolledInCourse: (state) => (courseId: number) =>
      state.currentUser?.enrolledCourseIds.includes(courseId) ?? false,
    streakDays: (state) => state.currentUser?.streakDays ?? 0,
  },
  actions: {
    async loadCurrentUser() {
      this.currentUser = await fetchCurrentUser();
      return this.currentUser;
    },
    async loadEnrolledCourses() {
      this.enrolledCourses = await fetchEnrolledCourses();
      return this.enrolledCourses;
    },
    async bootstrap(force = false) {
      if (this.hasBootstrapped && !force) {
        return;
      }

      this.isLoading = true;
      await Promise.all([this.loadCurrentUser(), this.loadEnrolledCourses()]);
      this.isLoading = false;
      this.hasBootstrapped = true;
    },
    async refreshEnrollmentState() {
      await Promise.all([this.loadCurrentUser(), this.loadEnrolledCourses()]);
    },
    patchEnrolledCourseProgress(payload: {
      courseId: number;
      completedKnowledgePointCount: number;
      totalKnowledgePointCount: number;
      lastLearningKnowledgePointId: number;
      lastLearningKnowledgePointTitle: string;
      lastLearningChapterTitle: string;
    }) {
      const target = this.enrolledCourses.find((course) => course.id === payload.courseId);
      if (!target) {
        return;
      }

      target.completedKnowledgePointCount = payload.completedKnowledgePointCount;
      target.totalKnowledgePointCount = payload.totalKnowledgePointCount;
      target.progressPercent =
        payload.totalKnowledgePointCount === 0
          ? 0
          : Math.round((payload.completedKnowledgePointCount / payload.totalKnowledgePointCount) * 100);
      target.lastLearningKnowledgePointId = payload.lastLearningKnowledgePointId;
      target.lastLearningKnowledgePointTitle = payload.lastLearningKnowledgePointTitle;
      target.lastLearningChapterTitle = payload.lastLearningChapterTitle;
    },
  },
});
