import { createRouter, createWebHistory } from "vue-router";

import MainLayout from "@/layouts/MainLayout.vue";
import { pinia } from "@/stores";
import { useUserStore } from "@/stores/user";
import CourseDetailView from "@/views/course/CourseDetailView.vue";
import LoginView from "@/views/auth/LoginView.vue";
import RegisterView from "@/views/auth/RegisterView.vue";
import LearningDashboardView from "@/views/placeholders/LearningDashboardView.vue";
import CourseSquareView from "@/views/placeholders/CourseSquareView.vue";
import SettingsView from "@/views/placeholders/SettingsView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: "/course/1",
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
      meta: {
        guestOnly: true,
      },
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
      meta: {
        guestOnly: true,
      },
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
          meta: {
            requiresAuth: true,
          },
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

router.beforeEach(async (to) => {
  const userStore = useUserStore(pinia);
  await userStore.bootstrap();

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  if (requiresAuth && !userStore.isAuthenticated) {
    return {
      path: "/login",
      query: { redirect: to.fullPath },
    };
  }

  const guestOnly = to.matched.some((record) => record.meta.guestOnly);
  if (guestOnly && userStore.isAuthenticated) {
    const redirectTarget =
      typeof to.query.redirect === "string" && to.query.redirect.length > 0
        ? to.query.redirect
        : "/learning";
    return redirectTarget;
  }

  return true;
});

export default router;
