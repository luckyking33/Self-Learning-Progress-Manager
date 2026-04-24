<script setup lang="ts">
import { computed } from "vue";
import { RouterLink } from "vue-router";
import DOMPurify from "dompurify";
import { marked } from "marked";

import AppIcon from "@/components/icons/AppIcon.vue";
import type { NoteDraft } from "@/types/note";

const props = defineProps<{
  draft: NoteDraft;
  activeNoteId: number | null;
  courseTitle: string | null;
  isSaving: boolean;
}>();

const emit = defineEmits<{
  (event: "update:title", value: string): void;
  (event: "update:content", value: string): void;
  (event: "save"): void;
  (event: "delete"): void;
}>();

const previewHtml = computed(() => {
  const raw = props.draft.content.trim().length > 0 ? props.draft.content : "_开始记录你的笔记内容_";
  return DOMPurify.sanitize(marked.parse(raw) as string);
});

const saveLabel = computed(() => {
  if (props.isSaving) {
    return "保存中...";
  }
  return props.activeNoteId ? "保存修改" : "创建笔记";
});
</script>

<template>
  <section class="grid min-h-[680px] gap-6 xl:grid-cols-[1.05fr_0.95fr]">
    <div class="rounded-[32px] bg-white px-7 py-7 shadow-[0_20px_60px_rgba(15,23,42,0.08)]">
      <div class="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p class="text-[11px] uppercase tracking-[0.28em] text-slate-400">Editor</p>
          <h1 class="mt-3 text-4xl font-semibold tracking-tight text-slate-950">
            {{ draft.title || "Untitled Note" }}
          </h1>
        </div>
        <div class="flex items-center gap-2">
          <button
            v-if="activeNoteId"
            class="inline-flex items-center gap-2 rounded-full bg-slate-100 px-4 py-2 text-sm font-medium text-slate-600 transition-all duration-300 hover:-translate-y-0.5 hover:bg-rose-50 hover:text-rose-600"
            @click="emit('delete')"
          >
            <AppIcon name="trash" class="h-4 w-4" />
            <span>删除</span>
          </button>
          <button
            class="inline-flex items-center gap-2 rounded-full bg-slate-900 px-5 py-2.5 text-sm font-medium text-white transition-all duration-300 hover:-translate-y-0.5 hover:shadow-[0_16px_34px_rgba(15,23,42,0.16)]"
            @click="emit('save')"
          >
            <AppIcon name="sparkles" class="h-4 w-4" />
            <span>{{ saveLabel }}</span>
          </button>
        </div>
      </div>

      <div class="mt-6 flex flex-wrap items-center gap-3">
        <span
          v-if="draft.courseId && courseTitle"
          class="inline-flex items-center gap-2 rounded-full bg-slate-100 px-4 py-2 text-sm font-medium text-slate-600"
        >
          <AppIcon name="course" class="h-4 w-4" />
          <RouterLink
            :to="`/course/${draft.courseId}`"
            class="transition-colors duration-300 hover:text-slate-900"
          >
            关联课程：{{ courseTitle }}
          </RouterLink>
        </span>
        <span
          v-else
          class="inline-flex items-center gap-2 rounded-full bg-slate-100 px-4 py-2 text-sm font-medium text-slate-500"
        >
          <AppIcon name="note" class="h-4 w-4" />
          <span>独立笔记</span>
        </span>
      </div>

      <div class="mt-8 space-y-5">
        <input
          :value="draft.title"
          type="text"
          placeholder="给这篇笔记一个标题"
          class="w-full border-0 bg-transparent px-0 text-4xl font-semibold tracking-tight text-slate-950 outline-none placeholder:text-slate-300"
          @input="emit('update:title', ($event.target as HTMLInputElement).value)"
        />

        <textarea
          :value="draft.content"
          placeholder="# 今天学到了什么？&#10;&#10;- 可以用 Markdown 记录结构化笔记&#10;- 右侧会实时预览排版效果"
          class="min-h-[520px] w-full resize-none border-0 bg-transparent px-0 text-base leading-8 text-slate-600 outline-none placeholder:text-slate-300"
          @input="emit('update:content', ($event.target as HTMLTextAreaElement).value)"
        />
      </div>
    </div>

    <div class="rounded-[32px] bg-white px-7 py-7 shadow-[0_20px_60px_rgba(15,23,42,0.08)]">
      <div class="flex items-center justify-between gap-3">
        <div>
          <p class="text-[11px] uppercase tracking-[0.28em] text-slate-400">Preview</p>
          <h2 class="mt-3 text-2xl font-semibold tracking-tight text-slate-950">Markdown 预览</h2>
        </div>
        <span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-500">
          实时同步
        </span>
      </div>

      <article
        class="note-preview prose prose-slate mt-8 max-w-none text-slate-700 prose-headings:tracking-tight prose-p:leading-8 prose-li:leading-8"
        v-html="previewHtml"
      />
    </div>
  </section>
</template>

<style scoped>
.note-preview :deep(pre) {
  overflow-x: auto;
  border-radius: 24px;
  background: rgb(15 23 42 / 0.96);
  padding: 1rem 1.25rem;
  color: white;
}

.note-preview :deep(code) {
  border-radius: 10px;
  background: rgb(241 245 249);
  padding: 0.15rem 0.45rem;
}

.note-preview :deep(blockquote) {
  border-left: 3px solid rgb(203 213 225);
  margin-left: 0;
  padding-left: 1rem;
  color: rgb(71 85 105);
}
</style>
