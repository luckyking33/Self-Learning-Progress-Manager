# STAR API 项目完整结构

## 📁 项目目录树

```
d:\STAR\
│
├── 📄 main.py ★                        # 主应用（所有API端点在此）
├── 📄 models.py                        # 数据库ORM模型
├── 📄 schemas.py                       # Pydantic数据验证
├── 📄 SQLconnet.py                     # 数据库连接配置
├── 📄 docker-compose.yml               # PostgreSQL Docker配置
│
├── 📋 API_INTERFACE_SUMMARY.md ★       # API完整文档
├── 📋 API_QUICK_REFERENCE.md ★         # 快速参考指南
│
├── 📂 services/                        # 业务逻辑服务
│   ├── course_query_service.py         # 课程查询逻辑
│   ├── course_enrollment_service.py    # 报名逻辑
│   └── course_progress_service.py      # 进度管理逻辑
│
├── 📂 Backend Development/             # 标准项目结构（备用）
│   ├── 📄 main.py                      # FastAPI应用入口
│   ├── 📂 app/
│   │   ├── 📄 main.py                  # 创建FastAPI应用
│   │   │
│   │   ├── 📂 api/
│   │   │   ├── 📄 router.py ★          # 所有路由聚合
│   │   │   └── 📂 routes/
│   │   │       ├── 📄 __init__.py
│   │   │       ├── 📄 health.py        # 健康检查
│   │   │       ├── 📄 courses.py ★     # 课程相关端点
│   │   │       ├── 📄 users.py ★       # 用户相关端点
│   │   │       └── 📄 progress.py ★    # 进度相关端点
│   │   │
│   │   ├── 📂 db/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 base.py              # SQLAlchemy基类
│   │   │   ├── 📄 models.py            # 数据库模型
│   │   │   └── 📄 session.py ★         # 数据库会话管理
│   │   │
│   │   └── 📂 core/
│   │       ├── 📄 __init__.py
│   │       ├── 📄 config.py ★          # 配置管理
│   │       └── 📄 auth.py ★            # 认证工具
│   │
│   └── 📄 alembic.ini / 📂 alembic/    # 数据库迁移配置
│
├── 📂 Frontend Development/            # 前端代码（非本次配置范围）
│
├── 📂 venv/                            # Python虚拟环境
│
├── 📄 requirements.txt                 # 依赖列表
└── 📄 README.md                        # 项目说明

★ = 本次配置创建或修改的文件
```

## 🔄 工作流程

### 用户工作流
```
用户来访 
    ↓
┌─→ 浏览课程 → GET /courses → 获取课程列表
│   ↓
│   GET /courses/{id} → 获取课程详情
│
├─→ 查看用户信息 → GET /users/me → 获取用户基本信息
│   ↓
│   GET /users/me/enrollments → 获取已报名课程
│
└─→ 学习课程
    ├─ POST /courses/{id}/enroll → 报名课程
    ├─ GET /courses/{id}/progress → 查看学习进度
    └─ PATCH /courses/{id}/progress → 更新学习进度
```

### 数据流程
```
HTTP Request
    ↓
FastAPI Router (main.py)
    ↓
Request Validation (schemas.py)
    ↓
Database Query (models.py + SQLAlchemy)
    ↓
Business Logic (services/*.py)
    ↓
Response Model (schemas.py)
    ↓
HTTP Response (JSON ApiEnvelope)
```

## 📊 数据库关系图

```
┌──────────┐         ┌──────────────┐
│  User    │         │  Course      │
│----------|         |--------------|
│ id (PK)  │         │ id (PK)      │
│ name     │         │ title        │
│ avatar   │         │ author_name  │
│ headline │         │ category     │
│ streak   │         │ is_public    │
└────┬─────┘         └──────┬───────┘
     │                      │
     │ 1:N (报名)          1:N (包含)
     │                      │
     └──→ ┌─────────────┐ ←─┘
         │ Enrollment  │
         |-------------|
         │ id          │
         │ user_id (FK)│
         │ course_id   │
         └────┬────────┘
              │
              │ 1:N (进度)
              │
          ┌───▼─────────────┐
          │Knowledge        │
          │PointProgress   │
          |─────────────────│
          │ id              │
          │ enrollment_id   │
          │ kp_id           │
          │ is_completed    │
          └─────────────────┘
```

## 🛠️ 技术栈

| 层级 | 技术 | 版本 |
|-----|------|------|
| 框架 | FastAPI | 最新 |
| ORM | SQLAlchemy | 2.x |
| 数据库 | PostgreSQL | 12+ |
| 验证 | Pydantic | 2.x |
| 服务器 | Uvicorn | 最新 |
| 文档 | Swagger/ReDoc | 自动生成 |

## 🚀 快速启动

### 一键启动脚本
```bash
# Windows PowerShell
cd d:\STAR
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 访问应用
- API文档: http://localhost:8000/docs
- 数据库: localhost:5432 (PostgreSQL)

## 🔗 接口汇总

| 功能 | 请求 | 响应 |
|-----|------|------|
| 获取用户信息 | GET /users/me | CurrentUserOut |
| 获取已报名课程 | GET /users/me/enrollments | List[EnrolledCourseCardOut] |
| 获取课程列表 | GET /courses?keyword=X&category=Y | List[CourseCardOut] |
| 获取课程详情 | GET /courses/{courseId} | CourseDetailOut |
| 报名课程 | POST /courses/{courseId}/enroll | {joinedAt} |
| 获取学习进度 | GET /courses/{courseId}/progress | CourseProgressStateOut |
| 更新学习进度 | PATCH /courses/{courseId}/progress | CourseProgressStateOut |

## ✅ 配置清单

### 文件修改
- [x] main.py - 添加缺失导入，实现7个API端点
- [x] schemas.py - 更新Pydantic v2配置
- [x] SQLconnet.py - 确保连接配置正确
- [x] Backend Development/app/db/session.py - 改为同步
- [x] Backend Development/app/core/config.py - 更新配置
- [x] Backend Development/app/api/router.py - 集成路由

### 文件创建
- [x] Backend Development/app/api/routes/courses.py
- [x] Backend Development/app/api/routes/users.py
- [x] Backend Development/app/api/routes/progress.py
- [x] Backend Development/app/core/auth.py
- [x] API_INTERFACE_SUMMARY.md
- [x] API_QUICK_REFERENCE.md
- [x] PROJECT_STRUCTURE.md (本文件)

## 📝 接下来的步骤

1. **启动数据库**
   ```bash
   docker-compose up -d
   ```

2. **运行应用**
   ```bash
   python -m uvicorn main:app --reload
   ```

3. **测试API**
   - 打开 http://localhost:8000/docs
   - 在Swagger UI中测试各个端点

4. **初始化数据** (可选)
   - 运行 init_data.py 或 create_tables.py 插入测试数据

5. **前端集成**
   - 配置前端项目的API基础URL
   - 实现用户认证

## 📚 文档位置

- **接口完整说明**: `d:\STAR\API_INTERFACE_SUMMARY.md`
- **快速参考指南**: `d:\STAR\API_QUICK_REFERENCE.md`
- **项目结构说明**: `d:\STAR\PROJECT_STRUCTURE.md` (本文件)
- **API实现**: `d:\STAR\main.py`

---

**状态**: ✅ 配置完成，可进行集成测试
**最后更新**: 2024年
