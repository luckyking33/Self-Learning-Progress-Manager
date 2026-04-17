<script setup lang="ts">
import { ref, watch } from "vue";

import type { Chapter } from "@/types/course";

const props = defineProps<{
  chapters: Chapter[];
  selectedKnowledgePointId: number | null;
  completedKnowledgePointIds: number[];
}>();

const emit = defineEmits<{
  (event: "select-knowledge-point", payload: { chapterId: number; knowledgePointId: number }): void;
  (event: "toggle-chapter", payload: { chapterId: number; expanded: boolean }): void;
  (event: "toggle-sidebar", payload: { collapsed: boolean }): void;
}>();

const sidebarCollapsed = ref(false);
const expandedChapterIds = ref<number[]>([]);

watch(
  () => props.chapters,
  (chapters) => {
    if (chapters.length > 0 && expandedChapterIds.value.length === 0) {
      expandedChapterIds.value = chapters.map((chapter) => chapter.id);
    }
  },
  { immediate: true },
);

function toggleSidebar() {
  sidebarCollapsed.value = !sidebarCollapsed.value;
  emit("toggle-sidebar", { collapsed: sidebarCollapsed.value });
}

function toggleChapter(chapterId: number) {
  const isExpanded = expandedChapterIds.value.includes(chapterId);
  if (isExpanded) {
    expandedChapterIds.value = expandedChapterIds.value.filter((id) => id !== chapterId);
  } else {
    expandedChapterIds.value = [...expandedChapterIds.value, chapterId];
  }

  emit("toggle-chapter", { chapterId, expanded: !isExpanded });
}

function selectKnowledgePoint(chapterId: number, knowledgePointId: number) {
  if (!expandedChapterIds.value.includes(chapterId)) {
    expandedChapterIds.value = [...expandedChapterIds.value, chapterId];
    emit("toggle-chapter", { chapterId, expanded: true });
  }

  emit("select-knowledge-point", { chapterId, knowledgePointId });
}
</script>

<template>
  <aside
    :class="[
      'relative shrink-0 overflow-hidden rounded-[28px] bg-white/92 shadow-[0_24px_60px_rgba(15,23,42,0.08)] transition-all duration-500 ease-in-out',
      sidebarCollapsed ? 'w-[94px]' : 'w-full max-w-[360px]',
    ]"
  >
    <div class="flex items-center justify-between px-5 pb-4 pt-5">
      <div v-if="!sidebarCollapsed" class="space-y-1">
        <p class="text-[11px] uppercase tracking-[0.28em] text-slate-400">STAR Course Map</p>
        <h2 class="text-lg font-semibold text-slate-900">章节导航</h2>
      </div>
      <button
        class="group flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-100 text-slate-500 transition-all duration-300 ease-in-out hover:-translate-y-0.5 hover:bg-slate-900 hover:text-white"
        @click="toggleSidebar"
      >
        <span class="text-lg transition-transform duration-300 group-hover:scale-110">
          {{ sidebarCollapsed ? "→" : "←" }}
        </span>
      </button>
    </div>

    <div v-if="sidebarCollapsed" class="px-3 pb-5">
      <div
        v-for="chapter in chapters"
        :key="chapter.id"
        class="mb-3 rounded-2xl bg-slate-50 px-3 py-4 text-center text-[11px] font-medium text-slate-500 shadow-[0_12px_30px_rgba(15,23,42,0.05)]"
      >
        {{ chapter.orderIndex }}
      </div>
    </div>

    <div v-else class="h-[calc(100vh-90px)] overflow-y-auto px-3 pb-4">
      <div
        v-for="chapter in chapters"
        :key="chapter.id"
        class="mb-3 rounded-3xl border border-slate-100 bg-slate-50/80 p-2 transition-all duration-300 ease-in-out hover:-translate-y-0.5 hover:shadow-[0_18px_45px_rgba(15,23,42,0.07)]"
      >
        <button
          class="flex w-full items-start justify-between gap-3 rounded-[22px] px-3 py-3 text-left"
          @click="toggleChapter(chapter.id)"
        >
          <div>
            <p class="text-xs font-medium uppercase tracking-[0.24em] text-slate-400">
              Chapter {{ chapter.orderIndex }}
            </p>
            <h3 class="mt-1 text-sm font-semibold text-slate-900">{{ chapter.title }}</h3>
            <p class="mt-1 text-xs leading-5 text-slate-500">{{ chapter.overview }}</p>
          </div>
          <span
            :class="[
              'mt-1 text-sm text-slate-400 transition-transform duration-300',
              expandedChapterIds.includes(chapter.id) ? 'rotate-90' : '',
            ]"
          >
            ›
          </span>
        </button>

        <Transition name="fade-slide">
          <div v-if="expandedChapterIds.includes(chapter.id)" class="space-y-2 px-2 pb-2">
            <button
              v-for="knowledgePoint in chapter.knowledgePoints"
              :key="knowledgePoint.id"
              :class="[
                'group flex w-full items-center justify-between rounded-2xl px-3 py-3 text-left transition-all duration-300 ease-in-out',
                selectedKnowledgePointId === knowledgePoint.id
                  ? 'bg-white text-slate-900 shadow-[0_14px_32px_rgba(15,23,42,0.09)]'
                  : 'bg-transparent text-slate-500 hover:bg-white/90 hover:text-slate-900 hover:shadow-[0_12px_24px_rgba(15,23,42,0.06)]',
              ]"
              @click="selectKnowledgePoint(chapter.id, knowledgePoint.id)"
            >
              <div class="min-w-0">
                <p class="truncate text-sm font-medium">{{ knowledgePoint.title }}</p>
                <p class="mt-1 truncate text-xs text-slate-400">{{ knowledgePoint.estimatedMinutes }} min</p>
              </div>
              <span
                :class="[
                  'ml-3 flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-[11px] font-semibold transition-all duration-300',
                  completedKnowledgePointIds.includes(knowledgePoint.id)
                    ? 'bg-emerald-100 text-emerald-600'
                    : 'bg-slate-100 text-slate-400',
                ]"
              >
                {{ completedKnowledgePointIds.includes(knowledgePoint.id) ? "✓" : "·" }}
              </span>
            </button>
          </div>
        </Transition>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition:
    opacity 0.28s ease-in-out,
    transform 0.28s ease-in-out;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
