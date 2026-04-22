<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";

import AppIcon from "@/components/icons/AppIcon.vue";
import { useUserStore } from "@/stores/user";

const router = useRouter();
const userStore = useUserStore();
const { enrolledCourses, isLoading } = storeToRefs(userStore);

const hasCourses = computed(() => enrolledCourses.value.length > 0);

function goToSquare() {
  void router.push("/square");
}

function continueLearning(courseId: number, knowledgePointId: number) {
  void router.push(`/course/${courseId}?kp=${knowledgePointId}`);
}

onMounted(async () => {
  await userStore.bootstrap();
});
</script>

<template>
  <section class="space-y-6">
    <div class="rounded-[32px] bg-white px-7 py-7 shadow-[0_20px_60px_rgba(15,23,42,0.08)]">
      <div class="flex flex-wrap items-start justify-between gap-5">
        <div>
          <p class="text-[11px] uppercase tracking-[0.28em] text-slate-400">My Learning</p>
          <h1 class="mt-3 text-4xl font-semibold tracking-tight text-slate-950">我的学习</h1>
          <p class="mt-4 max-w-2xl text-sm leading-7 text-slate-500">
            这里聚合你已经加入的课程、当前进度和上一次学习位置，让回到学习状态这件事足够轻。
          </p>
        </div>
        <div
          class="flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-sm text-slate-500"
        >
          <AppIcon name="clock" class="h-4 w-4" />
          <span>{{ enrolledCourses.length }} 门课程正在推进</span>
        </div>
      </div>
    </div>

    <div v-if="isLoading" class="grid gap-5 md:grid-cols-2">
      <div
        v-for="skeleton in 2"
        :key="skeleton"
        class="h-[240px] animate-pulse rounded-[28px] bg-white shadow-[0_18px_45px_rgba(15,23,42,0.08)]"
      />
    </div>

    <section
      v-else-if="!hasCourses"
      class="rounded-[32px] bg-white px-8 py-12 text-center shadow-[0_20px_60px_rgba(15,23,42,0.08)]"
    >
      <div class="mx-auto flex max-w-md flex-col items-center">
        <div class="relative flex h-24 w-24 items-center justify-center rounded-[28px] bg-slate-50 text-slate-500">
          <AppIcon name="folder" class="h-10 w-10" />
          <div class="absolute -right-1 -top-1 flex h-9 w-9 items-center justify-center rounded-2xl bg-white text-slate-900 shadow-[0_16px_28px_rgba(15,23,42,0.08)]">
            <AppIcon name="sparkles" class="h-4 w-4" />
          </div>
        </div>
        <h2 class="mt-6 text-3xl font-semibold tracking-tight text-slate-950">你的学习仓库还是空的</h2>
        <p class="mt-4 text-sm leading-7 text-slate-500">
          去课程广场看看，先加入一门你真正愿意学下去的课程。加入之后，这里会显示你的进度、最近学习节点和继续学习入口。
        </p>
        <button
          class="mt-8 inline-flex items-center gap-2 rounded-full bg-slate-900 px-5 py-3 text-sm font-medium text-white transition-all duration-300 ease-in-out hover:-translate-y-0.5 hover:shadow-[0_20px_45px_rgba(15,23,42,0.18)]"
          @click="goToSquare"
        >
          <AppIcon name="course" class="h-4 w-4" />
          <span>去广场看看</span>
        </button>
      </div>
    </section>

    <div v-else class="grid gap-5 md:grid-cols-2">
      <article
        v-for="course in enrolledCourses"
        :key="course.id"
        class="overflow-hidden rounded-[28px] bg-white shadow-[0_18px_45px_rgba(15,23,42,0.08)] transition-all duration-300 ease-in-out hover:-translate-y-1 hover:shadow-[0_24px_55px_rgba(15,23,42,0.12)]"
      >
        <div :class="['h-20 bg-gradient-to-br', course.coverTone]" />
        <div class="px-6 pb-6 pt-5">
          <div class="flex items-start justify-between gap-4">
            <div>
              <h2 class="text-2xl font-semibold tracking-tight text-slate-950">{{ course.title }}</h2>
              <p class="mt-2 text-sm leading-7 text-slate-500">{{ course.subtitle }}</p>
            </div>
            <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-900 text-xs font-semibold text-white">
              {{ course.authorAvatar }}
            </div>
          </div>

          <div class="mt-5 flex items-center gap-2 text-sm text-slate-500">
            <AppIcon name="user" class="h-4 w-4" />
            <span>{{ course.authorName }}</span>
          </div>

          <div class="mt-5">
            <div class="flex items-center justify-between text-sm text-slate-500">
              <span>学习进度</span>
              <span>已学习 {{ course.completedKnowledgePointCount }}/{{ course.totalKnowledgePointCount }} 知识点</span>
            </div>
            <div class="mt-3 h-2 rounded-full bg-slate-100">
              <div
                class="h-2 rounded-full bg-[linear-gradient(90deg,#0f172a_0%,#5a8dee_60%,#7cc8ff_100%)] transition-all duration-500 ease-in-out"
                :style="{ width: `${course.progressPercent}%` }"
              />
            </div>
          </div>

          <div class="mt-5 rounded-[24px] bg-slate-50 px-4 py-4">
            <div class="flex items-center gap-2 text-sm text-slate-500">
              <AppIcon name="clock" class="h-4 w-4" />
              <span>上次学习位置</span>
            </div>
            <p class="mt-2 text-sm font-medium text-slate-900">{{ course.lastLearningKnowledgePointTitle }}</p>
            <p class="mt-1 text-xs text-slate-400">{{ course.lastLearningChapterTitle }}</p>
          </div>

          <button
            class="mt-5 inline-flex items-center gap-2 rounded-full bg-slate-900 px-5 py-3 text-sm font-medium text-white transition-all duration-300 ease-in-out hover:-translate-y-0.5 hover:shadow-[0_18px_36px_rgba(15,23,42,0.16)]"
            @click="continueLearning(course.id, course.lastLearningKnowledgePointId)"
          >
            <AppIcon name="sparkles" class="h-4 w-4" />
            <span>继续学习</span>
          </button>
        </div>
      </article>
    </div>
  </section>
</template>
