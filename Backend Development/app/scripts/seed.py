"""Reset the local database and seed STAR demo data."""

from __future__ import annotations

import asyncio
from decimal import Decimal

from sqlalchemy import text

from app.core.security import get_password_hash
from app.db.models import Chapter, Course, CourseVersion, Enrollment, KnowledgePoint, KnowledgePointProgress, Resource, User
from app.db.session import AsyncSessionLocal


async def reset_database() -> None:
    async with AsyncSessionLocal() as session:
        await session.execute(
            text(
                """
                TRUNCATE TABLE
                    knowledge_point_progress,
                    enrollments,
                    resources,
                    knowledge_points,
                    chapters,
                    course_versions,
                    courses,
                    users
                RESTART IDENTITY CASCADE
                """
            )
        )
        await session.commit()


def build_course(
    *,
    author_id: int,
    title: str,
    subtitle: str,
    description: str,
    tags: list[str],
    category: str,
    cover_tone: str,
    chapter_specs: list[dict],
) -> Course:
    course = Course(
        author_id=author_id,
        title=title,
        subtitle=subtitle,
        description=description,
        tags=tags,
        category=category,
        cover_tone=cover_tone,
        is_public=True,
    )

    for chapter_index, chapter_spec in enumerate(chapter_specs, start=1):
        chapter = Chapter(
            title=chapter_spec["title"],
            description=chapter_spec["description"],
            order_index=chapter_index,
        )
        for point_index, point_spec in enumerate(chapter_spec["knowledge_points"], start=1):
            chapter.knowledge_points.append(
                KnowledgePoint(
                    title=point_spec["title"],
                    description=point_spec["description"],
                    order_index=point_index,
                )
            )

        for resource_index, resource_spec in enumerate(chapter_spec["resources"], start=1):
            chapter.resources.append(
                Resource(
                    title=resource_spec["title"],
                    url=resource_spec["url"],
                    resource_type=resource_spec["resource_type"],
                    description=resource_spec["description"],
                    order_index=resource_index,
                )
            )

        course.chapters.append(chapter)

    return course


async def seed() -> None:
    await reset_database()

    async with AsyncSessionLocal() as session:
        user1 = User(
            username="user1",
            email="user1@example.com",
            password_hash=get_password_hash("pw123"),
            avatar="U1",
            headline="正在把自学流程整理成可复用课程",
            streak_days=12,
            is_active=True,
        )
        user2 = User(
            username="user2",
            email="user2@example.com",
            password_hash=get_password_hash("pw123"),
            avatar="U2",
            headline="关注考研复习与长期职业成长",
            streak_days=5,
            is_active=True,
        )
        session.add_all([user1, user2])
        await session.flush()

        courses = [
            build_course(
                author_id=user1.id,
                title="Vue 3 自学路线",
                subtitle="从组合式 API 到工程化交付的轻量课程仓库",
                description="面向已经具备 JavaScript 基础的学习者，通过章节、知识点与资源串联出一条可追踪、可 fork 的 Vue 3 学习路径。",
                tags=["Vue 3", "Vite", "Pinia"],
                category="CS自学",
                cover_tone="from-sky-100 via-white to-cyan-50",
                chapter_specs=[
                    {
                        "title": "第一章 · 方向建立",
                        "description": "搭建环境、明确学习边界，并理解 Vue 3 的核心价值。",
                        "knowledge_points": [
                            {
                                "title": "搭建学习工作区",
                                "description": "准备 Vite、编辑器、插件和学习记录方式。",
                            },
                            {
                                "title": "组合式 API 的心智模型",
                                "description": "理解 setup、响应式状态与副作用拆分方式。",
                            },
                        ],
                        "resources": [
                            {
                                "title": "Vue 3 官方文档",
                                "url": "https://cn.vuejs.org/",
                                "resource_type": "docs",
                                "description": "官方入门和 API 说明。",
                            }
                        ],
                    },
                    {
                        "title": "第二章 · 核心推进",
                        "description": "把状态、组件通信和页面组织真正串起来。",
                        "knowledge_points": [
                            {
                                "title": "状态拆分与 Pinia",
                                "description": "使用 Pinia 管理课程与用户状态。",
                            },
                            {
                                "title": "练习与反馈闭环",
                                "description": "通过任务化练习来巩固响应式和路由协作。",
                            },
                        ],
                        "resources": [
                            {
                                "title": "Pinia 文档",
                                "url": "https://pinia.vuejs.org/",
                                "resource_type": "docs",
                                "description": "状态管理设计与最佳实践。",
                            }
                        ],
                    },
                ],
            ),
            build_course(
                author_id=user1.id,
                title="FastAPI 后端工程实践",
                subtitle="从路由、依赖注入到异步 ORM 的完整串联",
                description="把 FastAPI、SQLAlchemy 2.0 async、Alembic 和 Pydantic v2 连成一条稳定后端开发线。",
                tags=["FastAPI", "SQLAlchemy", "Alembic"],
                category="CS自学",
                cover_tone="from-indigo-100 via-white to-sky-50",
                chapter_specs=[
                    {
                        "title": "第一章 · API 基础",
                        "description": "先搭起能稳定扩展的 FastAPI 项目骨架。",
                        "knowledge_points": [
                            {
                                "title": "依赖注入与路由拆分",
                                "description": "用 Depends 组织数据库、认证和服务依赖。",
                            },
                            {
                                "title": "Pydantic v2 输入输出模型",
                                "description": "明确请求体和响应体边界。",
                            },
                        ],
                        "resources": [
                            {
                                "title": "FastAPI 文档",
                                "url": "https://fastapi.tiangolo.com/",
                                "resource_type": "docs",
                                "description": "FastAPI 官方文档。",
                            }
                        ],
                    },
                    {
                        "title": "第二章 · 数据层落地",
                        "description": "让模型、迁移和事务习惯稳定下来。",
                        "knowledge_points": [
                            {
                                "title": "异步 Session 使用",
                                "description": "理解 AsyncSession 生命周期与事务边界。",
                            },
                            {
                                "title": "Alembic 迁移习惯",
                                "description": "维护数据库结构演进而不是在启动时建表。",
                            },
                        ],
                        "resources": [
                            {
                                "title": "SQLAlchemy 2.0 文档",
                                "url": "https://docs.sqlalchemy.org/en/20/",
                                "resource_type": "docs",
                                "description": "SQLAlchemy 官方文档。",
                            }
                        ],
                    },
                ],
            ),
            build_course(
                author_id=user2.id,
                title="408 计算机考研复习地图",
                subtitle="把数据结构、组成原理与操作系统复习拆成可追踪节点",
                description="适合考研用户的 408 复习路线，强调章节推进、例题资源和阶段性复盘。",
                tags=["408", "考研", "复习"],
                category="考研",
                cover_tone="from-amber-100 via-white to-orange-50",
                chapter_specs=[
                    {
                        "title": "第一章 · 数据结构主线",
                        "description": "建立线性结构、树和图的解题骨架。",
                        "knowledge_points": [
                            {
                                "title": "线性表与栈队列",
                                "description": "明确时间复杂度和常见题型。",
                            },
                            {
                                "title": "树与二叉树遍历",
                                "description": "把递归、非递归和线索二叉树整理清楚。",
                            },
                        ],
                        "resources": [
                            {
                                "title": "408 数据结构复习笔记",
                                "url": "https://example.com/408-ds",
                                "resource_type": "article",
                                "description": "适合快速回顾重点知识点。",
                            }
                        ],
                    },
                    {
                        "title": "第二章 · 系统部分推进",
                        "description": "把组成原理与操作系统错题聚合起来。",
                        "knowledge_points": [
                            {
                                "title": "CPU 与存储层次",
                                "description": "配合例题复习性能与层级关系。",
                            },
                            {
                                "title": "进程调度与同步",
                                "description": "梳理常见同步模型和调度算法。",
                            },
                        ],
                        "resources": [
                            {
                                "title": "408 操作系统精选题",
                                "url": "https://example.com/408-os",
                                "resource_type": "repo",
                                "description": "题目整理与简要解析。",
                            }
                        ],
                    },
                ],
            ),
            build_course(
                author_id=user2.id,
                title="程序员沟通与表达升级",
                subtitle="把职场表达、汇报与协作整理成可执行课程",
                description="面向开发者的表达训练路线，帮助你在汇报、协作和文档写作中减少摩擦。",
                tags=["表达", "沟通", "协作"],
                category="职场提升",
                cover_tone="from-emerald-100 via-white to-teal-50",
                chapter_specs=[
                    {
                        "title": "第一章 · 表达骨架",
                        "description": "学会把问题、判断和建议分开说清楚。",
                        "knowledge_points": [
                            {
                                "title": "结论先行的汇报方式",
                                "description": "先给结论，再补上下文和证据。",
                            },
                            {
                                "title": "技术方案的对比表达",
                                "description": "把方案 tradeoff 讲清楚，而不是只报结论。",
                            },
                        ],
                        "resources": [
                            {
                                "title": "结构化表达 checklist",
                                "url": "https://example.com/communication",
                                "resource_type": "article",
                                "description": "会议和文档都能复用的表达清单。",
                            }
                        ],
                    },
                    {
                        "title": "第二章 · 协作现场",
                        "description": "把沟通动作落到 PR、评审和复盘里。",
                        "knowledge_points": [
                            {
                                "title": "PR 描述写法",
                                "description": "帮助 reviewer 更快理解变更边界和风险。",
                            },
                            {
                                "title": "复盘中的问题归因",
                                "description": "避免归责叙事，转向可执行改进。",
                            },
                        ],
                        "resources": [
                            {
                                "title": "高质量 PR 说明示例",
                                "url": "https://example.com/pr-writing",
                                "resource_type": "docs",
                                "description": "适合工程团队直接参考。",
                            }
                        ],
                    },
                ],
            ),
        ]

        session.add_all(courses)
        await session.flush()

        versions = [
            CourseVersion(course_id=course.id, version_tag="v1", snapshot_data=None)
            for course in courses
        ]
        session.add_all(versions)
        await session.flush()

        course_version_by_course_id = {
            version.course_id: version
            for version in versions
        }

        vue_course = courses[0]
        fastapi_course = courses[1]
        user1_vue_kps = vue_course.chapters[0].knowledge_points + vue_course.chapters[1].knowledge_points
        user1_fastapi_first_kp = fastapi_course.chapters[0].knowledge_points[0]

        enrollment1 = Enrollment(
            user_id=user1.id,
            course_id=vue_course.id,
            course_version_id=course_version_by_course_id[vue_course.id].id,
            last_learning_knowledge_point_id=user1_vue_kps[2].id,
            progress_percent=Decimal("50.00"),
        )
        enrollment2 = Enrollment(
            user_id=user1.id,
            course_id=fastapi_course.id,
            course_version_id=course_version_by_course_id[fastapi_course.id].id,
            last_learning_knowledge_point_id=user1_fastapi_first_kp.id,
            progress_percent=Decimal("25.00"),
        )
        enrollment3 = Enrollment(
            user_id=user2.id,
            course_id=courses[2].id,
            course_version_id=course_version_by_course_id[courses[2].id].id,
            last_learning_knowledge_point_id=courses[2].chapters[0].knowledge_points[1].id,
            progress_percent=Decimal("50.00"),
        )
        session.add_all([enrollment1, enrollment2, enrollment3])
        await session.flush()

        session.add_all(
            [
                KnowledgePointProgress(
                    enrollment_id=enrollment1.id,
                    knowledge_point_id=user1_vue_kps[0].id,
                    is_completed=True,
                ),
                KnowledgePointProgress(
                    enrollment_id=enrollment1.id,
                    knowledge_point_id=user1_vue_kps[1].id,
                    is_completed=True,
                ),
                KnowledgePointProgress(
                    enrollment_id=enrollment2.id,
                    knowledge_point_id=user1_fastapi_first_kp.id,
                    is_completed=True,
                ),
                KnowledgePointProgress(
                    enrollment_id=enrollment3.id,
                    knowledge_point_id=courses[2].chapters[0].knowledge_points[0].id,
                    is_completed=True,
                ),
                KnowledgePointProgress(
                    enrollment_id=enrollment3.id,
                    knowledge_point_id=courses[2].chapters[0].knowledge_points[1].id,
                    is_completed=True,
                ),
            ]
        )

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
