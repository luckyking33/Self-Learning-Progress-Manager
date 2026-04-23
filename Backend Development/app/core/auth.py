"""Authentication utilities."""

from fastapi import Depends


def get_current_user_id() -> int:
    """获取当前用户ID（模拟登录）"""
    return 7
