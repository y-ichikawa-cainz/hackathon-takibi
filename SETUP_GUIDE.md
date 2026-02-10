# セットアップガイド

## 1. OpenAI API キーの取得

1. [OpenAI Platform](https://platform.openai.com/) にアクセス
2. アカウントにログイン（なければ作成）
3. 左メニューから "API keys" を選択
4. "Create new secret key" をクリック
5. キーに名前をつけて作成
6. **重要**: キーは一度しか表示されないので、安全な場所にコピーしてください

## 2. Jira API トークンの取得

1. [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens) にアクセス
2. "Create API token" をクリック
3. トークンに名前をつける（例: "GitHub Automation"）
4. トークンをコピーして安全な場所に保存

### Jira プロジェクトキーの確認

1. Jira にログイン
2. 使用したいプロジェクトを開く
3. URLを確認: `https://your-domain.atlassian.net/browse/PROJ-123`
4. `PROJ` の部分がプロジェクトキーです

## 3. Confluence API トークンの取得

Confluence は Jira と同じ Atlassian アカウントを使用するため、上記の Jira API トークンと同じものを使用できます。

### Confluence スペースキーの確認

1. Confluence にログイン
2. 使用したいスペースを開く
3. "Space settings" をクリック
4. "Space details" でスペースキーを確認できます

## 4. GitHub Secrets の設定

1. GitHubリポジトリのページを開く
2. "Settings" タブをクリック
3. 左メニューから "Secrets and variables" > "Actions" を選択
4. "New repository secret" をクリックして以下を追加:

### 必須のシークレット

| シークレット名 | 説明 | 例 |
|--------------|------|-----|
| `OPENAI_API_KEY` | OpenAI APIキー | `sk-...` |
| `JIRA_URL` | JiraインスタンスURL | `https://yourcompany.atlassian.net` |
| `JIRA_EMAIL` | Jiraアカウントのメール | `your.email@example.com` |
| `JIRA_API_TOKEN` | Jira APIトークン | `ATATT3xFfGF0...` |
| `JIRA_PROJECT_KEY` | プロジェクトキー | `PROJ` |
| `CONFLUENCE_URL` | Confluence URL | `https://yourcompany.atlassian.net/wiki` |
| `CONFLUENCE_EMAIL` | Confluenceメール | `your.email@example.com` |
| `CONFLUENCE_API_TOKEN` | Confluence APIトークン | `ATATT3xFfGF0...` |
| `CONFLUENCE_SPACE_KEY` | スペースキー | `TEAM` |

## 5. 動作確認

1. リポジトリで新しい Issue を作成
2. "Actions" タブを開く
3. "Issue to Jira and Confluence" ワークフローの実行を確認
4. 完了後、Jira と Confluence を確認

## トラブルシューティング

### ワークフローが実行されない

- GitHub Actions が有効になっているか確認
- ワークフローファイルが正しいパス (`.github/workflows/`) にあるか確認

### API エラーが発生する

- シークレットが正しく設定されているか確認
- API トークンの有効期限を確認
- Jira/Confluence の URL が正しいか確認（末尾の `/` に注意）

### OpenAI API エラー

- API キーが有効か確認
- アカウントに十分なクレジットがあるか確認
- [OpenAI Status](https://status.openai.com/) でサービス状態を確認

## ローカルでのテスト

```bash
# 依存関係をインストール
pip install -r requirements.txt

# .env ファイルを作成
cp .env.example .env
# .env ファイルを編集して実際の値を設定

# 環境変数を読み込んでスクリプトを実行
export $(cat .env | xargs)
python .github/scripts/process_issue.py
```
