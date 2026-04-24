export interface Note {
  id: number;
  courseId: number | null;
  courseTitle: string | null;
  title: string;
  content: string;
  createdAt: string;
  updatedAt: string;
}

export interface NoteDraft {
  title: string;
  content: string;
  courseId: number | null;
}
