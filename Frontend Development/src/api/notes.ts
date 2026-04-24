import client from "@/api/client";
import type { ApiEnvelope } from "@/types/course";
import type { Note, NoteDraft } from "@/types/note";

export async function fetchNotes(): Promise<Note[]> {
  const response = await client.get<ApiEnvelope<Note[]>>("/notes");
  return response.data.data;
}

export async function fetchNote(noteId: number): Promise<Note> {
  const response = await client.get<ApiEnvelope<Note>>(`/notes/${noteId}`);
  return response.data.data;
}

export async function createNote(payload: NoteDraft): Promise<Note> {
  const response = await client.post<ApiEnvelope<Note>>("/notes", {
    title: payload.title,
    content: payload.content,
    course_id: payload.courseId,
  });
  return response.data.data;
}

export async function updateNote(noteId: number, payload: NoteDraft): Promise<Note> {
  const response = await client.put<ApiEnvelope<Note>>(`/notes/${noteId}`, {
    title: payload.title,
    content: payload.content,
    course_id: payload.courseId,
  });
  return response.data.data;
}

export async function deleteNote(noteId: number): Promise<void> {
  await client.delete(`/notes/${noteId}`);
}
