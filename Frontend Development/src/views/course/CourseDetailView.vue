<script setup lang="ts">
import { computed, watch } from "vue";
import { storeToRefs } from "pinia";
import { useRoute } from "vue-router";

import ChapterTree from "@/components/course/ChapterTree.vue";
import JoinActionFab from "@/components/course/JoinActionFab.vue";
import ProgressHeader from "@/components/course/ProgressHeader.vue";
import { useCourseStore } from "@/stores/course";
import { useUserStore } from "@/stores/user";

const route = useRoute();
const courseStore = useCourseStore();
const userStore = useUserStore();

const {
  completedCount,
  course,
  isLoading,
  joinState,
  progress,
  progressPercent,
  selectedChapter,
  selectedKnowledgePoint,
} = storeToRefs(courseStore);

const currentChapterResources = computed(() => selectedChapter.value?.resources ?? []);
const enrolled = computed(() =>
  course.value ? userStore.isEnrolledInCourse(course.value.id) : false,
);
const canTrackProgress = computed(() => userStore.isAuthenticated && enrolled.value);

function resolvedCourseId() {
  const value = Number(route.params.id);
  return Number.isFinite(value) && value > 0 ? value : 1;
}

function resolvedKnowledgePointId() {
  const value = Number(route.query.kp);
  return Number.isFinite(value) && value > 0 ? value : null;
}

async function loadCourseByRoute() {
  await courseStore.loadCourse(resolvedCourseId(), resolvedKnowledgePointId());
}

async function handleSelectKnowledgePoint(payload: {
  chapterId: number;
  knowledgePointId: number;
}) {
  void payload.chapterId;
  await courseStore.selectKnowledgePoint(payload.knowledgePointId);
}

function handleToggleChapter(payload: { chapterId: number; expanded: boolean }) {
  void payload;
}

function handleToggleSidebar(payload: { collapsed: boolean }) {
  void payload;
}

async function markCurrentKnowledgePoint() {
  if (selectedKnowledgePoint.value) {
    await courseStore.toggleKnowledgePointCompleted(selectedKnowledgePoint.value.id);
  }
}

watch(
  () => [route.params.id, route.query.kp],
  async () => {
    await loadCourseByRoute();
  },
  { immediate: true },
);
</script>

<template>
  <div class="space-y-6">
    <div class="flex min-h-[calc(100vh-176px)] gap-6">
      <ChapterTree
        :chapters="course?.chapters ?? []"
        :selected-knowledge-point-id="progress?.selectedKnowledgePointId ?? null"
        :completed-knowledge-point-ids="progress?.completedKnowledgePointIds ?? []"
        @select-knowledge-point="handleSelectKnowledgePoint"
        @toggle-chapter="handleToggleChapter"
        @toggle-sidebar="handleToggleSidebar"
      />

      <main class="min-w-0 flex-1">
        <div class="space-y-6">
          <ProgressHeader
            v-if="course"
            :course="course"
            :progress-percent="progressPercent"
            :completed-count="completedCount"
            :streak-days="userStore.streakDays"
            :is-enrolled="enrolled"
          />

          <section class="grid gap-6 xl:grid-cols-[1.3fr_0.9fr]">
            <div class="rounded-[32px] bg-white px-6 py-6 shadow-[0_20px_60px_rgba(15,23,42,0.08)] sm:px-8">
              <div v-if="isLoading" class="space-y-4">
                <div class="h-7 w-1/3 animate-pulse rounded-full bg-slate-100" />
                <div class="h-5 w-2/3 animate-pulse rounded-full bg-slate-100" />
                <div class="h-32 animate-pulse rounded-[28px] bg-slate-50" />
              </div>

              <Transition name="content-fade" mode="out-in">
                <div v-if="selectedKnowledgePoint && selectedChapter" :key="selectedKnowledgePoint.id">
                  <p class="text-xs uppercase tracking-[0.24em] text-slate-400">
                    {{ selectedChapter.title }}
                  </p>
                  <div class="mt-4 flex flex-wrap items-start justify-between gap-4">
                    <div>
                      <h2 class="text-3xl font-semibold tracking-tight text-slate-900">
                        {{ selectedKnowledgePoint.title }}
                      </h2>
                      <p class="mt-3 max-w-2xl text-base leading-8 text-slate-500">
                        {{ selectedKnowledgePoint.summary }}
                      </p>
                    </div>
                    <button
                      v-if="canTrackProgress"
                      class="rounded-full bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700 transition-all duration-300 ease-in-out hover:-translate-y-0.5 hover:bg-slate-900 hover:text-white"
                      @click="markCurrentKnowledgePoint"
                    >
                      {{
                        progress?.completedKnowledgePointIds.includes(selectedKnowledgePoint.id)
                          ? "标记为未完成"
                          : "标记为已完成"
                      }}
                    </button>
                  </div>

                  <p
                    v-if="!canTrackProgress"
                    class="mt-4 rounded-[20px] bg-slate-50 px-4 py-3 text-sm leading-6 text-slate-500"
                  >
                    登录并加入学习后，你的知识点进度和上次学习位置会自动保存。
                  </p>

                  <div class="mt-8 rounded-[28px] bg-slate-50/80 p-6">
                    <p class="text-sm leading-8 text-slate-600">
                      {{ selectedKnowledgePoint.content }}
                    </p>
                  </div>

                  <div class="mt-8 grid gap-4 md:grid-cols-3">
                    <div class="rounded-[28px] bg-slate-50 px-5 py-5">
                      <p class="text-xs uppercase tracking-[0.2em] text-slate-400">Estimated</p>
                      <p class="mt-3 text-2xl font-semibold text-slate-900">
                        {{ selectedKnowledgePoint.estimatedMinutes }} min
                      </p>
                    </div>
                    <div class="rounded-[28px] bg-slate-50 px-5 py-5 md:col-span-2">
                      <p class="text-xs uppercase tracking-[0.2em] text-slate-400">Key Actions</p>
                      <div class="mt-3 flex flex-wrap gap-2">
                        <span
                          v-for="action in selectedKnowledgePoint.keyActions"
                          :key="action"
                          class="rounded-full bg-white px-3 py-2 text-sm text-slate-600 shadow-[0_10px_18px_rgba(15,23,42,0.04)]"
                        >
                          {{ action }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </Transition>
            </div>

            <div class="space-y-6">
              <section class="rounded-[32px] bg-white px-6 py-6 shadow-[0_20px_60px_rgba(15,23,42,0.08)]">
                <div class="flex items-center justify-between gap-3">
                  <div>
                    <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Resources</p>
                    <h3 class="mt-2 text-2xl font-semibold text-slate-900">课程资源</h3>
                  </div>
                  <span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-500">
                    {{ currentChapterResources.length }} items
                  </span>
                </div>

                <div class="mt-5 space-y-3">
                  <a
                    v-for="resource in currentChapterResources"
                    :key="resource.id"
                    :href="resource.url"
                    target="_blank"
                    rel="noreferrer"
                    class="group block rounded-[26px] bg-slate-50 px-5 py-5 transition-all duration-300 ease-in-out hover:-translate-y-1 hover:shadow-[0_24px_42px_rgba(15,23,42,0.08)]"
                  >
                    <div class="flex items-start justify-between gap-3">
                      <div>
                        <p class="text-sm font-semibold text-slate-900">{{ resource.title }}</p>
                        <p class="mt-2 text-sm leading-7 text-slate-500">{{ resource.description }}</p>
                      </div>
                      <span
                        class="rounded-full bg-white px-3 py-1 text-[11px] uppercase tracking-[0.18em] text-slate-400 transition-colors duration-300 group-hover:text-slate-700"
                      >
                        {{ resource.type }}
                      </span>
                    </div>
                  </a>
                </div>
              </section>

              <section
                class="rounded-[32px] bg-[linear-gradient(180deg,#ffffff_0%,#f8fafc_100%)] px-6 py-6 shadow-[0_20px_60px_rgba(15,23,42,0.08)]"
              >
                <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Page Notes</p>
                <ul class="mt-4 space-y-3 text-sm leading-7 text-slate-500">
                  <li>左侧章节树支持折叠，适合在全局浏览与专注阅读之间切换。</li>
                  <li>知识点是主要学习单元，整体进度按知识点完成率计算。</li>
                  <li>资源卡片只聚焦当前章节，避免右侧内容区信息过载。</li>
                </ul>
              </section>
            </div>
          </section>
        </div>
      </main>
    </div>

    <JoinActionFab :join-state="joinState" :is-enrolled="enrolled" @join="courseStore.joinCourse()" />
  </div>
</template>

<style scoped>
.content-fade-enter-active,
.content-fade-leave-active {
  transition:
    opacity 0.28s ease-in-out,
    transform 0.28s ease-in-out;
}

.content-fade-enter-from,
.content-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
