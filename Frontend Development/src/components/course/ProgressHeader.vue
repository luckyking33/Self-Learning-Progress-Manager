<script setup lang="ts">
import type { CourseDetail } from "@/types/course";

defineProps<{
  course: CourseDetail;
  progressPercent: number;
  completedCount: number;
  streakDays: number;
  isEnrolled: boolean;
}>();
</script>

<template>
  <section
    class="relative overflow-hidden rounded-[32px] bg-white px-6 py-6 shadow-[0_20px_60px_rgba(15,23,42,0.08)] sm:px-8"
  >
    <div
      class="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top_left,_rgba(232,244,255,0.92),_transparent_36%),radial-gradient(circle_at_bottom_right,_rgba(240,246,240,0.88),_transparent_28%)]"
    />

    <div class="relative">
      <div class="flex flex-wrap items-start justify-between gap-5">
        <div class="max-w-3xl">
          <div class="flex flex-wrap items-center gap-2">
            <span
              class="rounded-full bg-slate-100 px-3 py-1 text-[11px] font-medium uppercase tracking-[0.24em] text-slate-500"
            >
              Course Detail
            </span>
            <span
              v-for="tag in course.tags"
              :key="tag"
              class="rounded-full bg-[#eef4ff] px-3 py-1 text-xs font-medium text-slate-600"
            >
              {{ tag }}
            </span>
          </div>
          <h1 class="mt-5 text-3xl font-semibold tracking-tight text-slate-900 sm:text-[40px]">
            {{ course.title }}
          </h1>
          <p class="mt-3 max-w-2xl text-base leading-8 text-slate-600">
            {{ course.subtitle }}
          </p>
          <p class="mt-4 max-w-3xl text-sm leading-7 text-slate-500">
            {{ course.description }}
          </p>
        </div>

        <div class="rounded-[28px] bg-slate-50 px-5 py-5 shadow-[0_12px_32px_rgba(15,23,42,0.05)]">
          <div class="flex items-center gap-3">
            <div
              class="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-900 text-sm font-semibold text-white"
            >
              {{ course.authorAvatar }}
            </div>
            <div>
              <p class="text-sm font-semibold text-slate-900">{{ course.authorName }}</p>
              <p class="text-xs text-slate-500">{{ course.authorRole }}</p>
            </div>
          </div>
          <div class="mt-4 grid grid-cols-3 gap-3 text-center">
            <div class="rounded-2xl bg-white px-3 py-3">
              <p class="text-lg font-semibold text-slate-900">{{ course.chapterCount }}</p>
              <p class="mt-1 text-[11px] uppercase tracking-[0.18em] text-slate-400">Chapters</p>
            </div>
            <div class="rounded-2xl bg-white px-3 py-3">
              <p class="text-lg font-semibold text-slate-900">{{ course.knowledgePointCount }}</p>
              <p class="mt-1 text-[11px] uppercase tracking-[0.18em] text-slate-400">Nodes</p>
            </div>
            <div class="rounded-2xl bg-white px-3 py-3">
              <p class="text-lg font-semibold text-slate-900">{{ course.estimatedHours }}h</p>
              <p class="mt-1 text-[11px] uppercase tracking-[0.18em] text-slate-400">Effort</p>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-8 grid gap-5 xl:grid-cols-[1.4fr_0.8fr]">
        <div class="rounded-[28px] bg-slate-50/90 px-5 py-5">
          <div class="flex items-center justify-between gap-4">
            <div>
              <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Learning Progress</p>
              <p class="mt-2 text-2xl font-semibold text-slate-900">{{ progressPercent }}%</p>
            </div>
            <div class="text-right">
              <p class="text-sm text-slate-500">{{ completedCount }}/{{ course.knowledgePointCount }}</p>
              <p class="mt-1 text-xs text-slate-400">已完成知识点</p>
            </div>
          </div>
          <div class="mt-4 h-3 rounded-full bg-white shadow-inner">
            <div
              class="h-3 rounded-full bg-[linear-gradient(90deg,#0f172a_0%,#5a8dee_55%,#7cc8ff_100%)] transition-all duration-700 ease-in-out"
              :style="{ width: `${progressPercent}%` }"
            />
          </div>
          <div class="mt-4 flex flex-wrap gap-2">
            <span
              class="rounded-full bg-white px-3 py-1 text-xs font-medium text-slate-500 shadow-[0_8px_18px_rgba(15,23,42,0.04)]"
            >
              连续学习 {{ streakDays }} 天
            </span>
            <span
              class="rounded-full bg-white px-3 py-1 text-xs font-medium text-slate-500 shadow-[0_8px_18px_rgba(15,23,42,0.04)]"
            >
              {{ isEnrolled ? "已加入学习" : "尚未加入学习" }}
            </span>
            <span
              v-if="course.forkedFromTitle"
              class="rounded-full bg-white px-3 py-1 text-xs font-medium text-slate-500 shadow-[0_8px_18px_rgba(15,23,42,0.04)]"
            >
              Forked from {{ course.forkedFromTitle }}
            </span>
          </div>
        </div>

        <div class="rounded-[28px] bg-slate-900 px-5 py-5 text-white">
          <p class="text-xs uppercase tracking-[0.24em] text-white/50">Current Learner</p>
          <div class="mt-4 flex items-center gap-3">
            <div class="flex h-12 w-12 items-center justify-center rounded-2xl bg-white/10 text-sm font-semibold">
              {{ course.authorAvatar }}
            </div>
            <div>
              <p class="font-semibold">课程由 {{ course.authorName }} 维护</p>
              <p class="text-sm text-white/60">学习者绑定稳定版本，内容更新不会打断当前进度。</p>
            </div>
          </div>
          <p class="mt-5 text-sm leading-7 text-white/70">
            左侧章节树用于快速跳转，右侧内容区优先展示当前知识点，保证阅读和操作始终聚焦在一个核心单元上。
          </p>
        </div>
      </div>
    </div>
  </section>
</template>
