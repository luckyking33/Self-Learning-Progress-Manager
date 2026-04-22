import type { MockMethod } from "vite-plugin-mock";

import {
  getCourseDetail,
  getCourseProgress,
  getCurrentUser,
  joinCourse,
  listCourseCards,
  listEnrolledCourseCards,
  updateCourseProgress,
} from "../src/mocks/data/course";

function resolveCourseId(url: string): number {
  const match = url.match(/\/courses\/(\d+)/);
  return match ? Number(match[1]) : 101;
}

export default [
  {
    url: "/api/mock/courses",
    method: "get",
    response: () => ({
      code: 0,
      message: "ok",
      data: listCourseCards(),
    }),
  },
  {
    url: /\/api\/mock\/courses\/\d+$/,
    method: "get",
    response: ({ url }: { url: string }) => ({
      code: 0,
      message: "ok",
      data: getCourseDetail(resolveCourseId(url)),
    }),
  },
  {
    url: /\/api\/mock\/courses\/\d+\/progress$/,
    method: "get",
    response: ({ url }: { url: string }) => ({
      code: 0,
      message: "ok",
      data: getCourseProgress(resolveCourseId(url)),
    }),
  },
  {
    url: /\/api\/mock\/courses\/\d+\/progress$/,
    method: "patch",
    response: ({ url, body }: { url: string; body?: Record<string, unknown> }) => ({
      code: 0,
      message: "updated",
      data: updateCourseProgress(resolveCourseId(url), body ?? {}),
    }),
  },
  {
    url: /\/api\/mock\/courses\/\d+\/enroll$/,
    method: "post",
    timeout: 700,
    response: ({ url }: { url: string }) => ({
      code: 0,
      message: "joined",
      data: joinCourse(resolveCourseId(url)),
    }),
  },
  {
    url: "/api/mock/users/me",
    method: "get",
    response: () => ({
      code: 0,
      message: "ok",
      data: getCurrentUser(),
    }),
  },
  {
    url: "/api/mock/users/me/enrollments",
    method: "get",
    response: () => ({
      code: 0,
      message: "ok",
      data: listEnrolledCourseCards(),
    }),
  },
] as MockMethod[];
