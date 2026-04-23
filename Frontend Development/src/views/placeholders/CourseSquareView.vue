<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";

import AppIcon from "@/components/icons/AppIcon.vue";
import { useCourseStore } from "@/stores/course";
import type { CourseCategory } from "@/types/course";

const router = useRouter();
const courseStore = useCourseStore();

const { availableCategories, courseCatalog, isCatalogLoading } = storeToRefs(courseStore);

const keyword = ref("");
const activeCategory = ref<CourseCategory | null>(null);

const filteredCourses = computed(() => {
  const normalizedKeyword = keyword.value.trim().toLowerCase();

  return courseCatalog.value.filter((course) => {
    const matchesKeyword =
      normalizedKeyword.length === 0 ||
      [course.title, course.subtitle, course.authorName, ...course.tags, course.category]
        .join(" ")
        .toLowerCase()
        .includes(normalizedKeyword);

    const matchesCategory = !activeCategory.value || course.category === activeCategory.value;
    return matchesKeyword && matchesCategory;
  });
});

function toggleCategory(category: CourseCategory) {
  activeCategory.value = activeCategory.value === category ? null : category;
}

function openCourse(courseId: number) {
  void router.push(`/course/${courseId}`);
}

onMounted(async () => {
  if (courseCatalog.value.length === 0) {
    await courseStore.loadCourseCatalog();
  }
});
</script>

<template>
  <section class="space-y-6">
    <div class="rounded-[32px] bg-white px-7 py-7 shadow-[0_20px_60px_rgba(15,23,42,0.08)]">
      <div class="flex flex-wrap items-start justify-between gap-5">
        <div>
          <p class="text-[11px] uppercase tracking-[0.28em] text-slate-400">Course Square</p>
          <h1 class="mt-3 text-4xl font-semibold tracking-tight text-slate-950">课程广场</h1>
          <p class="mt-4 max-w-2xl text-sm leading-7 text-slate-500">
            以 Gallery 视图浏览社区课程，找到适合自己的学习路径，再决定加入学习或继续深挖。
          </p>
        </div>
        <div
          class="flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-sm text-slate-500"
        >
          <AppIcon name="sparkles" class="h-4 w-4" />
          <span>{{ filteredCourses.length }} 门课程可探索</span>
        </div>
      </div>

      <div class="mt-7 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <label
          class="flex w-full max-w-[420px] items-center gap-3 rounded-[22px] border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-500 transition-all duration-300 focus-within:border-slate-300 focus-within:bg-white focus-within:shadow-[0_16px_32px_rgba(15,23,42,0.06)]"
        >
          <AppIcon name="search" class="h-4 w-4" />
          <input
            v-model="keyword"
            type="text"
            placeholder="搜索课程标题、作者、标签..."
            class="w-full bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
          />
        </label>

        <div class="flex flex-wrap gap-2">
          <button
            v-for="category in availableCategories"
            :key="category"
            :class="[
              'rounded-full px-4 py-2 text-sm font-medium transition-all duration-300 ease-in-out',
              activeCategory === category
                ? 'bg-slate-900 text-white shadow-[0_14px_30px_rgba(15,23,42,0.14)]'
                : 'bg-white text-slate-500 shadow-[0_10px_22px_rgba(15,23,42,0.05)] hover:-translate-y-0.5 hover:text-slate-900',
            ]"
            @click="toggleCategory(category)"
          >
            {{ category }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="isCatalogLoading" class="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
      <div
        v-for="skeleton in 6"
        :key="skeleton"
        class="h-[280px] animate-pulse rounded-[28px] bg-white shadow-[0_18px_45px_rgba(15,23,42,0.08)]"
      />
    </div>

    <div v-else class="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
      <article
        v-for="course in filteredCourses"
        :key="course.id"
        class="group cursor-pointer overflow-hidden rounded-[28px] bg-white shadow-[0_18px_45px_rgba(15,23,42,0.08)] transition-all duration-300 ease-in-out hover:-translate-y-1.5 hover:shadow-[0_28px_60px_rgba(15,23,42,0.12)]"
        @click="openCourse(course.id)"
      >
        <div :class="['h-24 bg-gradient-to-br', course.coverTone]" />
        <div class="px-6 pb-6 pt-5">
          <div class="flex items-center justify-between gap-3">
            <span
              class="rounded-full bg-slate-100 px-3 py-1 text-[11px] font-medium uppercase tracking-[0.2em] text-slate-500"
            >
              {{ course.category }}
            </span>
            <div class="flex items-center gap-2 text-xs text-slate-400">
              <AppIcon name="fork" class="h-4 w-4" />
              <span>{{ course.forkCount }}</span>
            </div>
          </div>

          <h2 class="mt-4 text-2xl font-semibold tracking-tight text-slate-950">
            {{ course.title }}
          </h2>
          <p class="mt-3 text-sm leading-7 text-slate-500">{{ course.subtitle }}</p>

          <div class="mt-5 flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-2xl bg-slate-900 text-xs font-semibold text-white">
              {{ course.authorAvatar }}
            </div>
            <div>
              <p class="text-sm font-medium text-slate-900">{{ course.authorName }}</p>
              <p class="text-xs text-slate-400">社区作者</p>
            </div>
          </div>

          <div class="mt-5 flex flex-wrap gap-2">
            <span
              v-for="tag in course.tags"
              :key="tag"
              class="rounded-full bg-slate-50 px-3 py-1 text-xs text-slate-500"
            >
              {{ tag }}
            </span>
          </div>

          <div class="mt-6 flex items-center justify-between border-t border-slate-100 pt-4 text-sm text-slate-500">
            <div class="flex items-center gap-2">
              <AppIcon name="people" class="h-4 w-4" />
              <span>{{ course.enrollmentCount }} 人加入</span>
            </div>
            <div class="flex items-center gap-2 text-slate-400 transition-transform duration-300 group-hover:translate-x-1">
              <span>查看详情</span>
              <span>→</span>
            </div>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>
