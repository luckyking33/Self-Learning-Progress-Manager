@echo off
REM STAR API 快速测试脚本 (Windows)
REM 这个脚本将自动启动应用并运行测试

setlocal enabledelayedexpansion

echo.
echo ========================================================================
echo  STAR API 快速测试启动脚本
echo ========================================================================
echo.

REM 检查是否在项目目录
if not exist "main.py" (
    echo 错误: 当前目录不是STAR项目目录
    echo 请确保在 d:\STAR 目录中运行此脚本
    pause
    exit /b 1
)

echo 步骤 1: 检查PostgreSQL数据库...
docker ps | findstr "postgres" >nul
if %errorlevel% neq 0 (
    echo [!] PostgreSQL 未启动，正在启动...
    docker-compose up -d
    timeout /t 5 /nobreak
    echo [OK] PostgreSQL 已启动
) else (
    echo [OK] PostgreSQL 已在运行
)

echo.
echo 步骤 2: 启动FastAPI应用...
echo [INFO] 应用将在 http://localhost:8000 启动
echo [INFO] API文档将在 http://localhost:8000/docs
echo.

REM 使用start命令在新窗口启动应用
start "STAR API Server" cmd /k python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

REM 等待服务启动
timeout /t 5 /nobreak

echo.
echo 步骤 3: 运行测试脚本...
echo.

REM 运行测试
python test_api.py

if %errorlevel% equ 0 (
    echo.
    echo ========================================================================
    echo  测试完成！所有API功能正常运行
    echo ========================================================================
    echo.
    echo 可以在以下地址访问:
    echo  - Swagger UI: http://localhost:8000/docs
    echo  - ReDoc: http://localhost:8000/redoc
    echo.
) else (
    echo.
    echo ========================================================================
    echo  测试失败，请查看上面的错误信息
    echo ========================================================================
    echo.
)

pause
