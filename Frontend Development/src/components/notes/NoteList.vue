<script setup lang="ts">
import { computed } from "vue";

import AppIcon from "@/components/icons/AppIcon.vue";
import type { Note } from "@/types/note";

const props = defineProps<{
  notes: Note[];
  activeNoteId: number | null;
  isLoading: boolean;
}>();

const emit = defineEmits<{
  (event: "create"): void;
  (event: "select", noteId: number): void;
}>();

const sortedNotes = computed(() =>
  [...props.notes].sort(
    (left, right) => new Date(right.updatedAt).getTime() - new Date(left.updatedAt).getTime(),
  ),
);

function formatUpdatedAt(value: string) {
  return new Intl.DateTimeFormat("zh-CN", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}
</script>

<template>
  <aside class="flex h-full min-h-[680px] flex-col rounded-[32px] bg-white px-4 py-4 shadow-[0_20px_60px_rgba(15,23,42,0.08)]">
    <div class="flex items-center justify-between gap-3 px-3 py-2">
      <div>
        <p class="text-[11px] uppercase tracking-[0.28em] text-slate-400">My Notes</p>
        <h2 class="mt-2 text-2xl font-semibold tracking-tight text-slate-950">我的笔记</h2>
      </div>
      <button
        class="inline-flex items-center gap-2 rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white transition-all duration-300 hover:-translate-y-0.5 hover:shadow-[0_16px_30px_rgba(15,23,42,0.16)]"
        @click="emit('create')"
      >
        <AppIcon name="note" class="h-4 w-4" />
        <span>新建</span>
      </button>
    </div>

    <div v-if="isLoading" class="mt-5 space-y-3 px-2">
      <div
        v-for="item in 5"
        :key="item"
        class="h-20 animate-pulse rounded-[22px] bg-slate-50"
      />
    </div>

    <div v-else-if="sortedNotes.length === 0" class="mt-10 px-4 text-center">
      <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-[22px] bg-slate-50 text-slate-400">
        <AppIcon name="note" class="h-7 w-7" />
      </div>
      <p class="mt-5 text-sm font-medium text-slate-900">还没有任何笔记</p>
      <p class="mt-2 text-sm leading-7 text-slate-500">
        从课程详情页记录灵感，或者直接在这里新建一篇 Markdown 笔记。
      </p>
    </div>

    <div v-else class="mt-5 flex-1 overflow-y-auto px-2">
      <button
        v-for="note in sortedNotes"
        :key="note.id"
        :class="[
          'mb-3 w-full rounded-[24px] px-4 py-4 text-left transition-all duration-300 ease-in-out',
          activeNoteId === note.id
            ? 'bg-slate-950 text-white shadow-[0_18px_36px_rgba(15,23,42,0.16)]'
            : 'bg-slate-50 text-slate-700 hover:-translate-y-0.5 hover:bg-slate-100',
        ]"
        @click="emit('select', note.id)"
      >
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0">
            <p class="truncate text-sm font-semibold">{{ note.title || "Untitled Note" }}</p>
            <p
              class="mt-2 line-clamp-2 text-xs leading-6"
              :class="activeNoteId === note.id ? 'text-white/70' : 'text-slate-500'"
            >
              {{ note.content || "还没有正文内容。" }}
            </p>
          </div>
          <span
            class="shrink-0 rounded-full px-2 py-1 text-[11px]"
            :class="activeNoteId === note.id ? 'bg-white/10 text-white/70' : 'bg-white text-slate-400'"
          >
            {{ formatUpdatedAt(note.updatedAt) }}
          </span>
        </div>
      </button>
    </div>
  </aside>
</template>
