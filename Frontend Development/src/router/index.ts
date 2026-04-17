import { createRouter, createWebHistory } from "vue-router";

import MainLayout from "@/layouts/MainLayout.vue";
import CourseSquareView from "@/views/placeholders/CourseSquareView.vue";
import LearningDashboardView from "@/views/placeholders/LearningDashboardView.vue";
import SettingsView from "@/views/placeholders/SettingsView.vue";
import CourseDetailView from "@/views/course/CourseDetailView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: "/course/101",
    },
    {
      path: "/",
      component: MainLayout,
      children: [
        {
          path: "square",
          name: "course-square",
          component: CourseSquareView,
        },
        {
          path: "learning",
          name: "learning-dashboard",
          component: LearningDashboardView,
        },
        {
          path: "settings",
          name: "settings",
          component: SettingsView,
        },
        {
          path: "course/:id",
          name: "course-detail",
          component: CourseDetailView,
          props: true,
        },
      ],
    },
  ],
  scrollBehavior() {
    return { top: 0, behavior: "smooth" };
  },
});

export default router;
