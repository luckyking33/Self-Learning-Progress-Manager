# STAR Frontend Skeleton

Suggested project structure for a Vue 3 + Vite + Tailwind + Pinia frontend:

```text
Frontend Development/
├─ mock/
│  └─ course.ts
├─ src/
│  ├─ mocks/
│  │  └─ data/
│  │     └─ course.ts
│  ├─ stores/
│  │  ├─ course.ts
│  │  └─ user.ts
│  ├─ types/
│  │  └─ course.ts
│  └─ views/
│     └─ course/
│        └─ CourseDetailView.vue
├─ package.json
└─ vite.config.ts
```

Recommended packages:

- `vue`
- `pinia`
- `tailwindcss`
- `vite-plugin-mock`
- `@vitejs/plugin-vue`

Recommended Vite plugin setup:

- Use `vite-plugin-mock` during local development.
- Keep the mock path at project-root `mock/`.
- Move shared mock payloads into `src/mocks/data/` so stores and mock APIs can reuse the same data source.

