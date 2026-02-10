"""
メインアプリケーション
ユーザー管理とデータ処理を行う
"""


class UserManager:
    """ユーザー管理クラス"""
    
    def __init__(self):
        self.users = {}
    
    def add_user(self, user_id, name, email):
        """ユーザーを追加"""
        self.users[user_id] = {
            'name': name,
            'email': email
        }
        return True
    
    def get_user(self, user_id):
        """ユーザー情報を取得"""
        return self.users.get(user_id)
    
    def delete_user(self, user_id):
        """ユーザーを削除"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False


class DataProcessor:
    """データ処理クラス"""
    
    def process_data(self, data):
        """データを処理"""
        if not data:
            return None
        
        processed = []
        for item in data:
            processed.append({
                'value': item.get('value', 0) * 2,
                'processed': True
            })
        return processed
    
    def validate_data(self, data):
        """データを検証"""
        if not isinstance(data, list):
            return False
        
        for item in data:
            if not isinstance(item, dict):
                return False
            if 'value' not in item:
                return False
        
        return True


def main():
    """メイン関数"""
    manager = UserManager()
    manager.add_user(1, "太郎", "taro@example.com")
    manager.add_user(2, "花子", "hanako@example.com")
    
    processor = DataProcessor()
    data = [
        {'value': 10},
        {'value': 20},
        {'value': 30}
    ]
    
    if processor.validate_data(data):
        result = processor.process_data(data)
        print(f"処理結果: {result}")


if __name__ == "__main__":
    main()
