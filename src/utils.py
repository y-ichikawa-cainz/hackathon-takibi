"""
ユーティリティ関数
共通処理をまとめたモジュール
"""
from datetime import datetime


def get_timestamp():
    """現在のタイムスタンプを取得"""
    return datetime.now().isoformat()


def format_message(message, level="INFO"):
    """メッセージをフォーマット"""
    timestamp = get_timestamp()
    return f"[{timestamp}] {level}: {message}"


def validate_email(email):
    """メールアドレスを検証"""
    if not email or '@' not in email:
        return False
    return True


def sanitize_input(text):
    """入力をサニタイズ"""
    if not text:
        return ""
    
    # 危険な文字を除去
    dangerous_chars = ['<', '>', '&', '"', "'"]
    sanitized = text
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()
