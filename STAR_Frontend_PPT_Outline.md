# STAR 前端开发成果展示 — PPT 汇报大纲

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

## 二、分页面 / 功能展示方案（Slide by Slide）

---

### Slide 1 — 封面

| 项目 | 内容 |
|---|---|
| **页面标题** | **STAR · 自学社区 — 前端开发成果展示** |
| **展示重点** | 项目定位、技术栈一览、团队角色 |
| **文本内容** | `Vue 3 · Vite 6 · TypeScript · Pinia · Tailwind CSS` / "一个让自学者管理课程、追踪进度、沉淀笔记的 Notion 风格学习工作区" |
| **视觉建议** | 深色全屏背景 + STAR Logo 居中 + 技术栈图标横排；底部标注团队成员与日期 |

---

### Slide 2 — 前端架构总览

| 项目 | 内容 |
|---|---|
| **页面标题** | **Architecture · 三层解耦 × 领域化状态管理** |
| **展示重点** | Layout → View → Component 分层、Pinia 三 Store 领域划分、API 模块化 |
| **文本内容** | "Layout 统管骨架 · View 消费路由 · Component 纯 UI 原子" / "User / Course / Notes 三 Store 各司其职，跨 Store 进度同步" |
| **视觉建议** | 左侧放一张**目录树截图**（`src/` 结构），右侧放架构分层示意图（Mermaid 或手绘风）：`MainLayout → [CourseSquareView, CourseDetailView, NotesWorkspaceView, LearningDashboardView] → [ChapterTree, ProgressHeader, NoteEditor, NoteList, JoinActionFab]`；底部列出 Store 关系图 |

> **可用代码片段：** `stores/index.ts` 的 Pinia 初始化 + `router/index.ts` 的路由配置（展示嵌套路由结构）

---

### Slide 3 — Notion 风格全局布局

| 项目 | 内容 |
|---|---|
| **页面标题** | **Global Layout · Notion 风格极简工作区** |
| **展示重点** | 毛玻璃侧边栏、导航高亮联动、双形态响应式、路由动画 |
| **文本内容** | "backdrop-blur-2xl 毛玻璃侧边栏" / "lg:fixed-sidebar ↔ mobile:top-grid 双形态" / "route-shell × route-page 双层穿越动画" |
| **视觉建议** | 截取**桌面端全局布局**（侧边栏 + 内容区），旁边放一张**移动端布局**对比截图；底部代码片段展示 `MainLayout.vue` 中毛玻璃 CSS：`bg-white/55 backdrop-blur-2xl shadow-[0_24px_60px_rgba(15,23,42,0.08)]` |

> **可用代码片段：** `main.css` 中 `route-shell` / `route-page` Transition 动画定义

---

### Slide 4 — 课程广场

| 项目 | 内容 |
|---|---|
| **页面标题** | **Course Square · Gallery 视图 × 实时检索** |
| **展示重点** | 多维度搜索过滤（关键词 + 分类）、卡片悬浮动效、Skeleton Loading |
| **文本内容** | "关键词搜索覆盖标题 / 作者 / 标签 / 分类" / "Category Toggle 一键筛选" / "6 卡骨架屏平滑过渡" |
| **视觉建议** | 截取课程广场全景截图；标注搜索框、分类按钮、课程卡片三个区域；右下角放卡片悬浮效果的动态截图（`hover:-translate-y-1.5`） |

> **可用代码片段：** `CourseSquareView.vue` 中 `filteredCourses` computed（展示多字段模糊匹配逻辑）

---

### Slide 5 — 课程详情页（核心页面）

| 项目 | 内容 |
|---|---|
| **页面标题** | **Course Detail · 章节树 × 知识点聚焦 × 进度追踪** |
| **展示重点** | 三栏布局（ChapterTree + 知识点内容 + 资源/笔记）、侧边栏折叠、知识点完成标记 |
| **文本内容** | "章节树 → 知识点选中 → 内容展示 → 进度同步" 数据流 / "sidebarCollapsed 94px ↔ 360px 流动切换" / "content-fade Transition 焦点平滑过渡" |
| **视觉建议** | 截取课程详情页全景截图（侧边栏展开 + 知识点内容 + 资源列表）；旁边放侧边栏折叠态截图；底部代码高亮 `content-fade` Transition 动画 |

> **可用代码片段：** `ChapterTree.vue` 核心交互逻辑（expandedChapterIds + selectKnowledgePoint）

---

### Slide 6 — 进度追踪与 Dashboard

| 项目 | 内容 |
|---|---|
| **页面标题** | **Progress Tracking · 渐变进度条 × URL 精准恢复** |
| **展示重点** | ProgressHeader 渐变进度条、跨 Store 进度同步、Dashboard "继续学习"一键跳转 |
| **文本内容** | "bg-[linear-gradient(90deg,#0f172a,#5a8dee,#7cc8ff)] 三段式渐变" / "Dashboard 记录上次学习章节 + 知识点，`?kp=` 参数精准恢复" / "completedKnowledgePointIds 增量同步" |
| **视觉建议** | 截取 ProgressHeader 进度条区域 + LearningDashboardView "继续学习"卡片；用箭头标注从 Dashboard 卡片 → `?kp=` 参数 → CourseDetailView 精准定位的完整链路 |

> **可用代码片段：** `courseStore.syncProgress()` 中 `patchEnrolledCourseProgress` 跨 Store 同步逻辑

---

### Slide 7 — JWT 认证系统

| 项目 | 内容 |
|---|---|
| **页面标题** | **Authentication · JWT 全链路 × 双向路由守卫** |
| **展示重点** | 登录/注册双视觉页面、Axios 拦截器、路由守卫、Token 持久化 |
| **文本内容** | "请求拦截器自动注入 Bearer Token" / "响应拦截器 401 统一处理 + redirect 保留" / "beforeEach 守卫：requiresAuth × guestOnly 双向控制" / "localStorage 令牌持久化 × bootstrap 单次保障" |
| **视觉建议** | 左半截取登录页截图（深色左栏 + 表单右栏的双栏设计）；右半放认证流程图：`Login → setToken → localStorage → Axios Interceptor → API → 401 → clearToken → redirect` |

> **可用代码片段：** `api/client.ts` 请求拦截器与 401 响应拦截器

---

### Slide 8 — Markdown 笔记系统

| 项目 | 内容 |
|---|---|
| **页面标题** | **Notes Workspace · Notion 风格 Markdown 编辑器** |
| **展示重点** | 左侧笔记列表 + 右侧编辑器 / 预览双栏、实时 Markdown 渲染、课程关联、URL 参数恢复 |
| **文本内容** | "marked + DOMPurify：渲染 + 消毒一体化" / "NoteList 按 updatedAt 降序排列，激活态深色高亮" / "从课程详情页一键跳转新建关联笔记（`?mode=new&courseId=`）" |
| **视觉建议** | 截取笔记工作区全景（左侧列表 + 右侧编辑器 + Markdown 预览）；右下角放代码片段展示 `NoteEditor.vue` 中 `previewHtml` computed（marked + DOMPurify 管道） |

> **可用代码片段：** `NoteEditor.vue` 的 `previewHtml` computed + scoped style 中 `:deep(pre)` / `:deep(code)` / `:deep(blockquote)` 样式定制

---

### Slide 9 — 工程化 × 开发体验

| 项目 | 内容 |
|---|---|
| **页面标题** | **Engineering · Mock 驱动 × TypeScript × 自治图标** |
| **展示重点** | vite-plugin-mock 本地 Mock 服务、全量 TypeScript 类型覆盖、SVG path 自治图标系统 |
| **文本内容** | "Mock 服务与后端 API 契约同构，前端零依赖独立运行" / "15+ 接口类型 + 泛型 ApiEnvelope<T> 消除 any" / "AppIcon：13 组 SVG path，零第三方依赖" |
| **视觉建议** | 左侧截取 `mock/course.ts` 代码片段（展示 Mock 路由定义格式）；中间展示 `types/course.ts` 的类型定义截图；右侧放 AppIcon 渲染效果（13 个图标排列） |

> **可用代码片段：** `constants/icons.ts` 的 SVG path 字典 + `AppIcon.vue` 的 `v-for` 渲染逻辑

---

### Slide 10 — 总结与展望

| 项目 | 内容 |
|---|---|
| **页面标题** | **Summary · 前端成果回顾 × 未来方向** |
| **展示重点** | 核心数据指标、技术亮点回顾、后续可扩展方向 |
| **文本内容** | "6 大功能模块 · 30+ 源文件 · 3200+ 行核心代码 · 0 any" / "三层解耦 × 领域化状态 × 契约优先 Mock × JWT 全链路" / **展望**："懒加载路由分包 · WebSocket 实时协作 · 课程 Fork 可视化 · PWA 离线学习" |
| **视觉建议** | 上半放技术亮点关键词标签云；下半列出 4 条展望方向，每条配一个小图标 |

---

## 三、亮点功能深度解析

### A. 课程详情页 — 章节树（ChapterTree）

#### 逻辑复杂度分析

```
数据结构：CourseDetail → Chapter[] → KnowledgePoint[]（三级嵌套树）
状态维度：
  ├─ expandedChapterIds: number[]     — 哪些章节处于展开态
  ├─ selectedKnowledgePointId: number — 当前聚焦的知识点
  ├─ completedKnowledgePointIds: number[] — 已完成知识点集合
  └─ sidebarCollapsed: boolean        — 侧边栏折叠态
```

**核心交互逻辑（5 项联动）：**

1. **初始化自动展开**：`watch(chapters)` 监听数据到达，首次自动展开全部章节（`expandedChapterIds = chapters.map(c => c.id)`）
2. **折叠/展开**：`toggleChapter` 维护 `expandedChapterIds` 数组的增删，伴随 `fade-slide` Transition（opacity + translateY -8px）
3. **知识点选中**：`selectKnowledgePoint` 先确保所在章节展开，再 `emit` 事件驱动父组件更新 Store
4. **完成状态反馈**：每个知识点右侧显示 `✓`（翠绿色）或 `·`（灰色），完全由 `completedKnowledgePointIds.includes()` 驱动
5. **侧边栏折叠**：`sidebarCollapsed` 在 94px 极简模式与 360px 展开模式之间切换，`transition-all duration-500` 实现流动宽度变化

**实现优势：**

- **纯 Props/Emits 契约**：ChapterTree 不直接依赖任何 Store，所有业务状态通过 Props 注入、交互通过 Emits 上报，**可独立测试、可复用**
- **声明式完成态渲染**：完成状态完全由外部数组驱动，无需内部维护任何标记逻辑
- **渐进展开策略**：首次全部展开降低认知负担，用户可主动折叠聚焦，符合"先总览、再深入"的学习心理模型
- **CSS Transition 动画**：章节子节点使用 `fade-slide` 过渡（0.28s opacity + translateY），视觉上优雅且不影响性能

---

### B. Notion 风格笔记系统

#### 逻辑复杂度分析

```
数据流：
  NoteList ──select──▶ NotesWorkspaceView ──selectNote──▶ noteStore
                                              │
  NoteEditor ──save──▶ NotesWorkspaceView ──saveCurrentNote──▶ noteStore ──API──▶ Server
                                              │
  CourseDetailView ──"记录笔记"──▶ router.push("/notes?mode=new&courseId=X")
                                              │
  NotesWorkspaceView ──syncWorkspaceWithRoute()──▶ noteStore.startDraft(courseId)
```

**六层设计复杂度：**

1. **列表-编辑器双栏联动**：NoteList 选中 → URL 更新 → WorkspaceView 监听 route.fullPath → noteStore.selectNote → NoteEditor 响应式更新
2. **新建 / 编辑 / 删除三态切换**：
   - 新建：`noteStore.startDraft()` 置空 currentNote + 初始化 draft
   - 编辑：`noteStore.selectNote(id)` 加载完整笔记 → 填充 draft
   - 删除：`removeCurrentNote()` → 自动回退至列表第一条或新建态
3. **跨模块课程关联**：从 CourseDetailView "记录笔记"按钮跳转 → URL 携带 `courseId` → WorkspaceView 解析 → `startDraft(courseId)` → NoteEditor 展示"关联课程"标签
4. **Markdown 实时渲染管道**：`marked.parse(raw)` → `DOMPurify.sanitize(html)` 双重处理，防 XSS 同时保证渲染保真
5. **URL 状态恢复**：`?note=<id>` 恢复编辑状态 / `?mode=new&courseId=<id>` 恢复新建 + 关联状态，支持刷新后精准恢复
6. **乐观更新 + 排序**：保存后立即 `splice` 更新列表或 `unshift` 插入，再按 `updatedAt` 降序重排，用户无需等待列表刷新

**实现优势：**

- **Notion 风格无边框编辑器**：`border-0 bg-transparent outline-none` 的极简输入体验，标题使用 `text-4xl font-semibold tracking-tight` 产生与 Notion 一致的"大标题"质感
- **`:deep()` 穿透样式定制**：预览区通过 scoped `:deep(pre)` / `:deep(code)` / `:deep(blockquote)` 精确控制 Markdown 渲染产物的视觉效果，代码块使用深色圆角背景、引用块使用左侧细线
- **课程-笔记双向导航**：笔记中可通过 RouterLink 跳回关联课程，课程中可一键跳转新建关联笔记，形成学习闭环
- **安全优先**：强制通过 DOMPurify 消毒所有用户输入的 HTML，杜绝 XSS 风险

---

## 四、前端结项陈述（约 200 字）

> STAR 前端基于 **Vue 3 + Vite + TypeScript + Pinia** 构建了一套**三层解耦、领域化状态驱动**的自学工作区。我们以 **Notion 风格极简设计**为视觉基调，通过毛玻璃侧边栏、超圆角卡片、渐变进度条与微动效体系，打造了兼具专业感与亲和力的学习界面。在工程化层面，我们采用**契约优先的 Mock 驱动开发流**实现前后端并行开发，借助 **Axios 拦截器 + JWT 路由守卫**完成认证全链路闭环，并通过 **URL 参数精准恢复**让用户的学习进度与笔记状态在任意场景下无缝衔接。课程详情页的**可折叠章节树**与 Markdown 笔记系统的**实时渲染 + 安全消毒管道**是两大核心技术亮点。整体前端以零 `any`、全量类型覆盖的 TypeScript 代码交付，为后续迭代奠定了坚实的工程基础。
