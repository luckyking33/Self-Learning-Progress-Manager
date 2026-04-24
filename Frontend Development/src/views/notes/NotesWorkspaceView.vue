<script setup lang="ts">
import { computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { storeToRefs } from "pinia";

import NoteEditor from "@/components/notes/NoteEditor.vue";
import NoteList from "@/components/notes/NoteList.vue";
import { useCourseStore } from "@/stores/course";
import { useNoteStore } from "@/stores/notes";

const route = useRoute();
const router = useRouter();
const noteStore = useNoteStore();
const courseStore = useCourseStore();

const { currentNote, draft, isLoading, isSaving, notes } = storeToRefs(noteStore);

const activeNoteId = computed(() => currentNote.value?.id ?? null);
const courseTitle = computed(() => {
  if (!draft.value.courseId) {
    return null;
  }

  const fromCatalog = courseStore.courseCatalog.find((course) => course.id === draft.value.courseId);
  return fromCatalog?.title ?? currentNote.value?.courseTitle ?? null;
});

function resolvedNoteId() {
  const raw = Number(route.query.note);
  return Number.isFinite(raw) && raw > 0 ? raw : null;
}

function resolvedCourseId() {
  const raw = Number(route.query.courseId);
  return Number.isFinite(raw) && raw > 0 ? raw : null;
}

async function syncWorkspaceWithRoute() {
  if (courseStore.courseCatalog.length === 0) {
    await courseStore.loadCourseCatalog();
  }

  if (route.query.mode === "new") {
    noteStore.startDraft(resolvedCourseId());
    return;
  }

  const noteId = resolvedNoteId();
  if (noteId) {
    if (currentNote.value?.id !== noteId) {
      await noteStore.selectNote(noteId);
    }
    return;
  }

  if (noteStore.notes.length > 0) {
    await noteStore.selectNote(noteStore.notes[0].id);
  } else {
    noteStore.startDraft();
  }
}

async function handleCreate() {
  const courseId = resolvedCourseId();
  noteStore.startDraft(courseId);
  await router.replace({
    path: "/notes",
    query: courseId ? { mode: "new", courseId: String(courseId) } : { mode: "new" },
  });
}

async function handleSelect(noteId: number) {
  await noteStore.selectNote(noteId);
  await router.replace({
    path: "/notes",
    query: { note: String(noteId) },
  });
}

async function handleSave() {
  const saved = await noteStore.saveCurrentNote();
  await router.replace({
    path: "/notes",
    query: { note: String(saved.id) },
  });
}

async function handleDelete() {
  await noteStore.removeCurrentNote();
  if (noteStore.notes.length > 0) {
    await handleSelect(noteStore.notes[0].id);
    return;
  }

  noteStore.startDraft();
  await router.replace({ path: "/notes", query: { mode: "new" } });
}

onMounted(async () => {
  await noteStore.loadNotes();
  await syncWorkspaceWithRoute();
});

watch(
  () => route.fullPath,
  async () => {
    await syncWorkspaceWithRoute();
  },
);
</script>

<template>
  <section class="grid gap-6 xl:grid-cols-[360px_minmax(0,1fr)]">
    <NoteList
      :notes="notes"
      :active-note-id="activeNoteId"
      :is-loading="isLoading"
      @create="handleCreate"
      @select="handleSelect"
    />

    <NoteEditor
      :draft="draft"
      :active-note-id="activeNoteId"
      :course-title="courseTitle"
      :is-saving="isSaving"
      @update:title="noteStore.patchDraft({ title: $event })"
      @update:content="noteStore.patchDraft({ content: $event })"
      @save="handleSave"
      @delete="handleDelete"
    />
  </section>
</template>
