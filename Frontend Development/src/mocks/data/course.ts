import type {
  Chapter,
  CourseCard,
  CourseCategory,
  CourseDetail,
  CourseProgressState,
  EnrolledCourseCard,
  MockUser,
} from "@/types/course";

export const courseCategories: CourseCategory[] = ["CS自学", "考研", "职场提升"];

function cloneValue<T>(value: T): T {
  return structuredClone(value);
}

function createChapters(baseId: number, theme: string): Chapter[] {
  return [
    {
      id: baseId + 1,
      title: "第一章 · 方向建立",
      overview: `${theme} 的学习目标、工具链和知识边界。`,
      orderIndex: 1,
      knowledgePoints: [
        {
          id: baseId + 11,
          title: "搭建学习工作区",
          summary: `明确 ${theme} 的学习素材、环境与结果产物。`,
          content: `为 ${theme} 建立单独的学习工作区，拆分资料、练习与输出。这样后续无论是 fork 课程还是迁移版本，都能保持稳定结构。`,
          orderIndex: 1,
          estimatedMinutes: 20,
          keyActions: ["整理资料来源", "规划章节顺序", "确定输出习惯"],
        },
        {
          id: baseId + 12,
          title: "建立知识地图",
          summary: "先看全貌，再进入具体知识点。",
          content: `一门 ${theme} 课程最怕碎片化推进。先建立章节树和知识点关系，再决定先学什么、复习什么。`,
          orderIndex: 2,
          estimatedMinutes: 28,
          keyActions: ["按主题分层", "明确主干知识", "记录依赖关系"],
        },
      ],
      resources: [
        {
          id: baseId + 101,
          title: `${theme} 起步文档`,
          type: "docs",
          url: "https://example.com/start",
          description: `帮助你快速进入 ${theme} 的学习上下文。`,
        },
        {
          id: baseId + 102,
          title: `${theme} 学习案例集`,
          type: "article",
          url: "https://example.com/cases",
          description: "通过案例理解课程组织方式与目标。 ",
        },
      ],
    },
    {
      id: baseId + 2,
      title: "第二章 · 核心推进",
      overview: `围绕 ${theme} 的主线能力建立稳定节奏。`,
      orderIndex: 2,
      knowledgePoints: [
        {
          id: baseId + 21,
          title: "高频知识点拆分",
          summary: `把 ${theme} 中最常见的能力拆成可学习单元。`,
          content: `从常见应用场景倒推知识点，比单纯按教材顺序更容易建立真实语境。每个知识点应足够小，便于打勾、复习和迁移。`,
          orderIndex: 1,
          estimatedMinutes: 35,
          keyActions: ["识别高频场景", "定义学习单元", "建立复习标记"],
        },
        {
          id: baseId + 22,
          title: "练习与反馈闭环",
          summary: "把阅读、实践和反思连接起来。",
          content: `如果 ${theme} 只有输入而没有反馈，课程就很容易失效。资源、练习和知识点状态必须形成完整闭环。`,
          orderIndex: 2,
          estimatedMinutes: 32,
          keyActions: ["安排练习", "记录问题", "回写复盘结论"],
        },
      ],
      resources: [
        {
          id: baseId + 201,
          title: `${theme} 实战视频`,
          type: "video",
          url: "https://example.com/video",
          description: "用实际案例串起本章的重点能力。",
        },
      ],
    },
    {
      id: baseId + 3,
      title: "第三章 · 应用与沉淀",
      overview: `把 ${theme} 转成长期可复用的学习资产。`,
      orderIndex: 3,
      knowledgePoints: [
        {
          id: baseId + 31,
          title: "复盘与重构",
          summary: "学会把旧知识点重组为更好的版本。",
          content: `STAR 的课程价值不仅是记录，更是重构。复盘时把路径、资源和知识点重新组织，才能形成可持续的课程仓库。`,
          orderIndex: 1,
          estimatedMinutes: 24,
          keyActions: ["回看学习痕迹", "修正路径设计", "整理最终版本"],
        },
        {
          id: baseId + 32,
          title: "对外分享与 fork",
          summary: "把个人路径发布给社区并允许他人派生。",
          content: `完成一门课程之后，把它作为公开版本发布出去。派生关系和学习关系分离，才能保证社区传播与个人进度都不混乱。`,
          orderIndex: 2,
          estimatedMinutes: 18,
          keyActions: ["准备公开版本", "补齐说明文案", "建立后续迭代节奏"],
        },
      ],
      resources: [
        {
          id: baseId + 301,
          title: `${theme} 输出模板`,
          type: "repo",
          url: "https://example.com/template",
          description: "帮助你把课程沉淀成结构化成果。",
        },
      ],
    },
  ];
}

const courseDetailSeed: CourseDetail[] = [
  {
    id: 101,
    title: "Vue 3 自学路线",
    subtitle: "从组合式 API 到工程化交付的轻量课程仓库",
    description:
      "面向已经具备 JavaScript 基础的学习者，通过章节、知识点与资源串联出一条可追踪、可 fork 的 Vue 3 学习路径。",
    authorName: "沈清和",
    authorRole: "社区课程作者",
    authorAvatar: "SQ",
    forkedFromTitle: "Frontend Guild Starter Path",
    isPublic: true,
    chapterCount: 3,
    knowledgePointCount: 6,
    estimatedHours: 12,
    tags: ["Vue 3", "Vite", "Pinia"],
    forkCount: 184,
    enrollmentCount: 1260,
    category: "CS自学",
    coverTone: "from-sky-100 via-white to-cyan-50",
    chapters: createChapters(1100, "Vue 3"),
  },
  {
    id: 102,
    title: "408 算法与数据结构冲刺",
    subtitle: "为考研复习建立章节化、可复盘的刷题路径",
    description:
      "把数据结构、算法设计与高频题型串成可追踪的考研冲刺路线，强调进度统计与重点节点回看。",
    authorName: "季北辰",
    authorRole: "考研路线整理者",
    authorAvatar: "JB",
    forkedFromTitle: null,
    isPublic: true,
    chapterCount: 3,
    knowledgePointCount: 6,
    estimatedHours: 16,
    tags: ["数据结构", "算法", "408"],
    forkCount: 96,
    enrollmentCount: 840,
    category: "考研",
    coverTone: "from-amber-100 via-white to-orange-50",
    chapters: createChapters(2100, "408 算法"),
  },
  {
    id: 103,
    title: "计算机英语阅读强化",
    subtitle: "把长难句与专业阅读拆成可逐步推进的知识点",
    description:
      "为考研和技术阅读场景设计的英语课程，强调句法拆解、词汇回收与阅读输出习惯。",
    authorName: "陆芷宁",
    authorRole: "语言学习路径维护者",
    authorAvatar: "LZ",
    forkedFromTitle: null,
    isPublic: true,
    chapterCount: 3,
    knowledgePointCount: 6,
    estimatedHours: 10,
    tags: ["英语", "阅读", "长难句"],
    forkCount: 58,
    enrollmentCount: 520,
    category: "考研",
    coverTone: "from-rose-100 via-white to-pink-50",
    chapters: createChapters(3100, "英语阅读"),
  },
  {
    id: 104,
    title: "程序员沟通与表达升级",
    subtitle: "把职场表达、汇报与协作整理成可执行课程",
    description:
      "面向进入团队协作阶段的工程师，通过表达、写作与协作场景建立长期可复用的职场能力课程。",
    authorName: "周闻川",
    authorRole: "工程经理",
    authorAvatar: "ZW",
    forkedFromTitle: "Team Communication Essentials",
    isPublic: true,
    chapterCount: 3,
    knowledgePointCount: 6,
    estimatedHours: 8,
    tags: ["表达", "沟通", "协作"],
    forkCount: 134,
    enrollmentCount: 1095,
    category: "职场提升",
    coverTone: "from-emerald-100 via-white to-teal-50",
    chapters: createChapters(4100, "职场沟通"),
  },
  {
    id: 105,
    title: "CS 自学总控台",
    subtitle: "把操作系统、网络与数据库汇成一套总览课程",
    description:
      "适合已经有一点基础的学习者，用仓库式视角统一管理多个 CS 子方向，并为后续 fork 和版本发布打基础。",
    authorName: "顾远之",
    authorRole: "学习系统设计者",
    authorAvatar: "GY",
    forkedFromTitle: null,
    isPublic: true,
    chapterCount: 3,
    knowledgePointCount: 6,
    estimatedHours: 18,
    tags: ["操作系统", "网络", "数据库"],
    forkCount: 212,
    enrollmentCount: 1430,
    category: "CS自学",
    coverTone: "from-slate-200 via-white to-indigo-50",
    chapters: createChapters(5100, "CS 自学"),
  },
];

const courseDetails = new Map<number, CourseDetail>(
  courseDetailSeed.map((course) => [course.id, cloneValue(course)]),
);

const courseProgressMap = new Map<number, CourseProgressState>([
  [
    101,
    {
      courseId: 101,
      selectedKnowledgePointId: 1122,
      lastLearningKnowledgePointId: 1122,
      completedKnowledgePointIds: [1111, 1112, 1121],
      joinedAt: null,
    },
  ],
  [
    102,
    {
      courseId: 102,
      selectedKnowledgePointId: 2121,
      lastLearningKnowledgePointId: 2121,
      completedKnowledgePointIds: [2111, 2112],
      joinedAt: null,
    },
  ],
  [
    103,
    {
      courseId: 103,
      selectedKnowledgePointId: 3112,
      lastLearningKnowledgePointId: 3112,
      completedKnowledgePointIds: [3111],
      joinedAt: null,
    },
  ],
  [
    104,
    {
      courseId: 104,
      selectedKnowledgePointId: 4121,
      lastLearningKnowledgePointId: 4121,
      completedKnowledgePointIds: [4111, 4112, 4121],
      joinedAt: null,
    },
  ],
  [
    105,
    {
      courseId: 105,
      selectedKnowledgePointId: 5112,
      lastLearningKnowledgePointId: 5112,
      completedKnowledgePointIds: [5111, 5112, 5121, 5122],
      joinedAt: null,
    },
  ],
]);

const currentUserState: MockUser = {
  id: 7,
  name: "林曜",
  avatar: "LY",
  headline: "正在把 STAR 做成一套真正能用的自学社区",
  streakDays: 12,
  enrolledCourseIds: [],
};

function getCourseDetailInternal(courseId: number): CourseDetail {
  return cloneValue(courseDetails.get(courseId) ?? cloneValue(courseDetailSeed[0]));
}

function getCourseProgressInternal(courseId: number): CourseProgressState {
  const found = courseProgressMap.get(courseId);
  if (found) {
    return cloneValue(found);
  }

  const fallbackDetail = getCourseDetailInternal(courseId);
  const firstKnowledgePointId = fallbackDetail.chapters[0]?.knowledgePoints[0]?.id ?? 0;
  return {
    courseId,
    selectedKnowledgePointId: firstKnowledgePointId,
    lastLearningKnowledgePointId: firstKnowledgePointId,
    completedKnowledgePointIds: [],
    joinedAt: null,
  };
}

function writeCourseProgress(progress: CourseProgressState) {
  courseProgressMap.set(progress.courseId, cloneValue(progress));
}

function findKnowledgePointMeta(courseId: number, knowledgePointId: number) {
  const course = getCourseDetailInternal(courseId);
  for (const chapter of course.chapters) {
    const knowledgePoint = chapter.knowledgePoints.find((item) => item.id === knowledgePointId);
    if (knowledgePoint) {
      return {
        chapterTitle: chapter.title,
        knowledgePointTitle: knowledgePoint.title,
      };
    }
  }

  return {
    chapterTitle: "起始章节",
    knowledgePointTitle: "开始学习",
  };
}

export function listCourseCards(): CourseCard[] {
  return Array.from(courseDetails.values()).map((course) => ({
    id: course.id,
    title: course.title,
    subtitle: course.subtitle,
    authorName: course.authorName,
    authorAvatar: course.authorAvatar,
    tags: cloneValue(course.tags),
    forkCount: course.forkCount,
    enrollmentCount: course.enrollmentCount,
    category: course.category,
    coverTone: course.coverTone,
  }));
}

export function getCourseDetail(courseId: number): CourseDetail {
  return getCourseDetailInternal(courseId);
}

export function getCourseProgress(courseId: number): CourseProgressState {
  return getCourseProgressInternal(courseId);
}

export function getCurrentUser(): MockUser {
  return cloneValue(currentUserState);
}

export function joinCourse(courseId: number) {
  if (!currentUserState.enrolledCourseIds.includes(courseId)) {
    currentUserState.enrolledCourseIds.push(courseId);
  }

  const progress = getCourseProgressInternal(courseId);
  if (!progress.joinedAt) {
    progress.joinedAt = new Date().toISOString();
    writeCourseProgress(progress);
  }

  const currentCourse = courseDetails.get(courseId);
  if (currentCourse) {
    currentCourse.enrollmentCount += 1;
    courseDetails.set(courseId, currentCourse);
  }

  return {
    joinedAt: progress.joinedAt,
  };
}

export function updateCourseProgress(
  courseId: number,
  payload: Partial<
    Pick<
      CourseProgressState,
      "selectedKnowledgePointId" | "lastLearningKnowledgePointId" | "completedKnowledgePointIds"
    >
  >,
): CourseProgressState {
  const current = getCourseProgressInternal(courseId);
  const nextProgress: CourseProgressState = {
    ...current,
    ...payload,
    courseId,
  };
  writeCourseProgress(nextProgress);
  return nextProgress;
}

export function listEnrolledCourseCards(): EnrolledCourseCard[] {
  return currentUserState.enrolledCourseIds.map((courseId) => {
    const course = getCourseDetailInternal(courseId);
    const progress = getCourseProgressInternal(courseId);
    const lastPosition = findKnowledgePointMeta(courseId, progress.lastLearningKnowledgePointId);

    return {
      id: course.id,
      title: course.title,
      subtitle: course.subtitle,
      authorName: course.authorName,
      authorAvatar: course.authorAvatar,
      coverTone: course.coverTone,
      completedKnowledgePointCount: progress.completedKnowledgePointIds.length,
      totalKnowledgePointCount: course.knowledgePointCount,
      progressPercent:
        course.knowledgePointCount === 0
          ? 0
          : Math.round((progress.completedKnowledgePointIds.length / course.knowledgePointCount) * 100),
      lastLearningKnowledgePointId: progress.lastLearningKnowledgePointId,
      lastLearningKnowledgePointTitle: lastPosition.knowledgePointTitle,
      lastLearningChapterTitle: lastPosition.chapterTitle,
    };
  });
}
