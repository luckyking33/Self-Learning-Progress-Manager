import { defineStore } from "pinia";

import { fetchMe, login as loginRequest, register as registerRequest } from "@/api/auth";
import { fetchEnrolledCourses } from "@/api/course";
import type { EnrolledCourseCard, MockUser } from "@/types/course";
import type { RegisterPayload } from "@/types/auth";
import { clearAccessToken, getAccessToken, setAccessToken } from "@/utils/auth";

export const useUserStore = defineStore("user", {
  state: (): {
    token: string | null;
    currentUser: MockUser | null;
    enrolledCourses: EnrolledCourseCard[];
    isLoading: boolean;
    hasBootstrapped: boolean;
  } => ({
    token: getAccessToken(),
    currentUser: null,
    enrolledCourses: [],
    isLoading: false,
    hasBootstrapped: false,
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token && state.currentUser),
    isEnrolledInCourse: (state) => (courseId: number) =>
      state.currentUser?.enrolledCourseIds.includes(courseId) ?? false,
    streakDays: (state) => state.currentUser?.streakDays ?? 0,
  },
  actions: {
    setToken(token: string) {
      this.token = token;
      setAccessToken(token);
    },
    clearSession() {
      this.token = null;
      this.currentUser = null;
      this.enrolledCourses = [];
      clearAccessToken();
    },
    async fetchMe() {
      this.currentUser = await fetchMe();
      return this.currentUser;
    },
    async loadEnrolledCourses() {
      if (!this.token) {
        this.enrolledCourses = [];
        return this.enrolledCourses;
      }

      this.enrolledCourses = await fetchEnrolledCourses();
      return this.enrolledCourses;
    },
    async restoreSession(forceFetch = false) {
      if (!this.token) {
        this.token = getAccessToken();
      }

      if (!this.token) {
        this.currentUser = null;
        this.enrolledCourses = [];
        return false;
      }

      if (this.currentUser && !forceFetch) {
        return true;
      }

      try {
        await Promise.all([this.fetchMe(), this.loadEnrolledCourses()]);
        return true;
      } catch (error) {
        this.clearSession();
        throw error;
      }
    },
    async bootstrap(force = false) {
      if (this.hasBootstrapped && !force) {
        return;
      }

      this.isLoading = true;
      try {
        await this.restoreSession(force);
      } catch {
        this.clearSession();
      } finally {
        this.isLoading = false;
        this.hasBootstrapped = true;
      }
    },
    async login(identity: string, password: string) {
      this.isLoading = true;
      try {
        const auth = await loginRequest(identity, password);
        this.setToken(auth.access_token);
        await Promise.all([this.fetchMe(), this.loadEnrolledCourses()]);
      } finally {
        this.isLoading = false;
        this.hasBootstrapped = true;
      }
    },
    async register(payload: RegisterPayload) {
      this.isLoading = true;
      try {
        const auth = await registerRequest(payload);
        this.setToken(auth.access_token);
        await Promise.all([this.fetchMe(), this.loadEnrolledCourses()]);
      } finally {
        this.isLoading = false;
        this.hasBootstrapped = true;
      }
    },
    logout() {
      this.clearSession();
    },
    async refreshEnrollmentState() {
      if (!this.token) {
        this.enrolledCourses = [];
        return;
      }

      await Promise.all([this.fetchMe(), this.loadEnrolledCourses()]);
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
