# STAR 前端开发成果展示 大纲

> 项目：STAR · Self-Study Studio  
> 技术栈：Vue 3.5 + Vite 6 + TypeScript 5 + Pinia 3 + Tailwind CSS 3 + Axios  
> 前端规模：11 个目录、30+ 源文件、约 3 200 行核心代码  

---

## 一、前端技术亮点提炼（四维度）

### 1. 架构模式

| 关键词 | 说明 |
|---|---|
| **Layout → View → Component 三层解耦架构** | `MainLayout` 统管导航骨架与路由出口；View 层（CourseDetailView / NotesWorkspaceView 等）负责页面编排与路由参数消费；Component 层（ChapterTree / NoteEditor 等）为纯 UI 原子组件，通过 `Props / Emits` 契约与外部通信，不依赖任何业务状态 |
| **原子化组件设计** | ChapterTree、ProgressHeader、JoinActionFab、NoteEditor、NoteList 均为单职责原子组件；AppIcon 基于 SVG path 常量表实现零依赖图标系统，无需引入任何第三方图标库 |
| **基于 Pinia defineStore 的领域化状态拆分** | 三个 Store（`user` / `course` / `notes`）分别封装身份验证、课程进度和笔记 CRUD 领域逻辑；跨 Store 调用（`courseStore → userStore.patchEnrolledCourseProgress`）实现进度同步闭环 |
| **TypeScript 全量类型覆盖** | 独立 `types/` 目录定义 CourseDetail、Chapter、KnowledgePoint、Note、NoteDraft、ApiEnvelope 等 15+ 接口；API 层与 Store 层全部使用泛型约束，消除 `any` |

### 2. 工程化实践

| 关键词 | 说明 |
|---|---|
| **契约优先的 Mock 驱动开发流** | 使用 `vite-plugin-mock` + `mockPath: "mock"` 搭建与后端 API 契约完全一致的本地 Mock 服务，前端可在后端零就绪状态下独立开发、联调与演示 |
| **Axios 拦截器 × 全局状态管理** | 请求拦截器自动注入 `Bearer Token`；响应拦截器统一处理 401 未授权（清除令牌 + 带 redirect 参数跳转登录页）、统一错误消息提取（`detail → message → fallback`） |
| **路由守卫双向权限控制** | `beforeEach` 全局守卫实现 `requiresAuth`（未登录重定向登录页，携带 `redirect` 参数）与 `guestOnly`（已登录绕过认证页）双向拦截 |
| **模块化 API 层** | `api/client.ts` 封装 Axios 实例；`api/auth.ts`、`api/course.ts`、`api/notes.ts` 按领域拆分，每个函数返回纯业务类型（解包 `ApiEnvelope<T>`），上层完全不感知 HTTP 细节 |

### 3. 视觉与交互

| 关键词 | 说明 |
|---|---|
| **Notion 风格极简设计语境** | 统一超圆角（`rounded-[28px]` ~ `rounded-[36px]`）、极淡阴影（`shadow-[0_20px_60px_rgba(15,23,42,0.08)]`）、纸白卡片 + 暖灰背景（`#f5f5f2`） |
| **自定义 Webkit 极细滚动条** | `main.css` 中 8px 宽度、透明轨道、圆角缩进拇指块，悬停渐深，与整体极简风格融合 |
| **基于 CSS 变量与 radial-gradient 的氛围渲染** | ProgressHeader 背景使用双圆形径向渐变营造"呼吸感光晕"；登录/注册页左栏采用深色基底叠加径向高光 |
| **微动效体系** | 全站 `hover:-translate-y-0.5` 浮起反馈 + `transition-all duration-300 ease-in-out` 贯穿；进度条使用 `transition-all duration-700` 产生流畅增长动效 |
| **SVG 自治图标系统** | `constants/icons.ts` 以 `Record<string, string[]>` 存储 13 组 SVG path；`AppIcon.vue` 通过 `v-for` 渲染多路径，支持任意尺寸 / 颜色继承 |

### 4. 性能与体验

| 关键词 | 说明 |
|---|---|
| **双层路由级平滑动画** | App.vue 外壳使用 `route-shell` Transition（水平位移 18 → -12 px），MainLayout 内部使用 `route-page` Transition（相同时序），实现页面切换"穿越感" |
| **基于 URL 参数的精准进度恢复** | 课程详情页通过 `?kp=` 参数定位知识点；笔记工作区通过 `?note=` / `?mode=new&courseId=` 恢复编辑状态；Dashboard "继续学习"按钮一键跳转至上次学习位置 |
| **Skeleton Loading 占位** | CourseSquareView 6 卡骨架屏 + NoteList 5 行骨架屏 + CourseDetailView 内容区 3 级骨架屏，用 `animate-pulse` 保持视觉节奏 |
| **响应式双形态布局** | MainLayout 侧边栏 `lg:` 左侧固定 260px / 移动端顶部 2×2 网格；ChapterTree `sidebarCollapsed` 实现 94px 极简模式与 360px 展开模式间的 500ms 流动切换 |
| **Store Bootstrap 单次保障** | `userStore.bootstrap()` 内置 `hasBootstrapped` 标记，全局仅请求一次用户身份，避免路由守卫 + Layout onMounted 重复触发 |

---
