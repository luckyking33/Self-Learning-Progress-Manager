import { defineStore } from "pinia";

import { createNote, deleteNote, fetchNote, fetchNotes, updateNote } from "@/api/notes";
import type { Note, NoteDraft } from "@/types/note";

const EMPTY_DRAFT: NoteDraft = {
  title: "Untitled Note",
  content: "",
  courseId: null,
};

export const useNoteStore = defineStore("notes", {
  state: (): {
    notes: Note[];
    currentNote: Note | null;
    draft: NoteDraft;
    isLoading: boolean;
    isSaving: boolean;
  } => ({
    notes: [],
    currentNote: null,
    draft: { ...EMPTY_DRAFT },
    isLoading: false,
    isSaving: false,
  }),
  getters: {
    hasNotes: (state) => state.notes.length > 0,
  },
  actions: {
    async loadNotes() {
      this.isLoading = true;
      try {
        this.notes = await fetchNotes();
        return this.notes;
      } finally {
        this.isLoading = false;
      }
    },
    startDraft(courseId: number | null = null) {
      this.currentNote = null;
      this.draft = {
        ...EMPTY_DRAFT,
        courseId,
      };
    },
    async selectNote(noteId: number) {
      this.isLoading = true;
      try {
        const note = await fetchNote(noteId);
        this.currentNote = note;
        this.draft = {
          title: note.title,
          content: note.content,
          courseId: note.courseId,
        };
        return note;
      } finally {
        this.isLoading = false;
      }
    },
    patchDraft(payload: Partial<NoteDraft>) {
      this.draft = {
        ...this.draft,
        ...payload,
      };
    },
    async saveCurrentNote() {
      this.isSaving = true;
      try {
        const normalizedDraft: NoteDraft = {
          title: this.draft.title.trim() || "Untitled Note",
          content: this.draft.content,
          courseId: this.draft.courseId,
        };

        const saved = this.currentNote
          ? await updateNote(this.currentNote.id, normalizedDraft)
          : await createNote(normalizedDraft);

        const existingIndex = this.notes.findIndex((item) => item.id === saved.id);
        if (existingIndex >= 0) {
          this.notes.splice(existingIndex, 1, saved);
        } else {
          this.notes.unshift(saved);
        }

        this.notes.sort(
          (left, right) => new Date(right.updatedAt).getTime() - new Date(left.updatedAt).getTime(),
        );

        this.currentNote = saved;
        this.draft = {
          title: saved.title,
          content: saved.content,
          courseId: saved.courseId,
        };

        return saved;
      } finally {
        this.isSaving = false;
      }
    },
    async removeCurrentNote() {
      if (!this.currentNote) {
        return;
      }

      const deletedId = this.currentNote.id;
      await deleteNote(deletedId);
      this.notes = this.notes.filter((item) => item.id !== deletedId);
      this.currentNote = null;
      this.draft = { ...EMPTY_DRAFT };
    },
  },
});
