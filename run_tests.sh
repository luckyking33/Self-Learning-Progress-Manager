#!/bin/bash
# STAR API 快速测试脚本 (Linux/Mac)
# 这个脚本将自动启动应用并运行测试

echo ""
echo "========================================================================"
echo "  STAR API 快速测试启动脚本"
echo "========================================================================"
echo ""

# 检查是否在项目目录
if [ ! -f "main.py" ]; then
    echo "错误: 当前目录不是STAR项目目录"
    echo "请确保在 STAR 项目目录中运行此脚本"
    exit 1
fi

echo "步骤 1: 检查PostgreSQL数据库..."
if ! docker ps | grep -q postgres; then
    echo "[!] PostgreSQL 未启动，正在启动..."
    docker-compose up -d
    sleep 5
    echo "[OK] PostgreSQL 已启动"
else
    echo "[OK] PostgreSQL 已在运行"
fi

echo ""
echo "步骤 2: 启动FastAPI应用..."
echo "[INFO] 应用将在 http://localhost:8000 启动"
echo "[INFO] API文档将在 http://localhost:8000/docs"
echo ""

# 在后台启动应用
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
APP_PID=$!

# 等待服务启动
sleep 5

echo ""
echo "步骤 3: 运行测试脚本..."
echo ""

# 运行测试
python test_api.py
TEST_RESULT=$?

echo ""

if [ $TEST_RESULT -eq 0 ]; then
    echo "========================================================================"
    echo "  测试完成！所有API功能正常运行"
    echo "========================================================================"
    echo ""
    echo "可以在以下地址访问:"
    echo "  - Swagger UI: http://localhost:8000/docs"
    echo "  - ReDoc: http://localhost:8000/redoc"
    echo ""
    echo "按 Ctrl+C 停止应用"
else
    echo "========================================================================"
    echo "  测试失败，请查看上面的错误信息"
    echo "========================================================================"
    echo ""
fi

# 保持应用运行（直到用户中断）
wait $APP_PID
