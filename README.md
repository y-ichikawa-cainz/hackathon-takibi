# hackason-takibi

GitHub Issueから自動的にJiraチケットとConfluenceページを生成するシステム

## 概要

このリポジトリは、GitHub Actionsを使用してIssueが作成されたときに自動的に以下の処理を実行します：

1. リポジトリ内の主要コード（`src/`）を読み取る
2. OpenAI APIを使用してIssue内容とコードを分析し、実装仕様とJiraチケット案を生成
3. Jira APIを使用してチケットを作成（受け入れ条件付き）
4. Confluence APIを使用してドキュメントページを作成

## セットアップ

### 必要な環境変数（GitHub Secrets）

リポジトリの Settings > Secrets and variables > Actions で以下のシークレットを設定してください：

#### OpenAI API
- `OPENAI_API_KEY`: OpenAI APIキー

#### Jira API
- `JIRA_URL`: JiraインスタンスのベースURL（例: `https://your-domain.atlassian.net`）
- `JIRA_EMAIL`: Jiraアカウントのメールアドレス
- `JIRA_API_TOKEN`: Jira APIトークン
- `JIRA_PROJECT_KEY`: チケットを作成するプロジェクトのキー（例: `PROJ`）

#### Confluence API
- `CONFLUENCE_URL`: ConfluenceインスタンスのベースURL（例: `https://your-domain.atlassian.net/wiki`）
- `CONFLUENCE_EMAIL`: Confluenceアカウントのメールアドレス
- `CONFLUENCE_API_TOKEN`: Confluence APIトークン
- `CONFLUENCE_SPACE_KEY`: ページを作成するスペースのキー

### API トークンの取得方法

#### OpenAI API キー
1. [OpenAI Platform](https://platform.openai.com/)にアクセス
2. API Keys ページでキーを作成

#### Jira/Confluence API トークン
1. [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)にアクセス
2. 「Create API token」をクリック
3. トークン名を入力して作成

## 使い方

1. このリポジトリで新しいIssueを作成
2. GitHub Actionsが自動的にトリガーされます
3. Actions タブで実行状況を確認できます
4. 完了後、Jiraチケットと Confluenceページが自動作成されます

## ディレクトリ構造

```
.
├── .github/
│   ├── workflows/
│   │   └── issue-automation.yml     # GitHub Actionsワークフロー
│   └── scripts/
│       └── process_issue.py         # メイン処理スクリプト
├── src/                              # アプリケーションのソースコード
│   ├── main.py                       # メインアプリケーション
│   ├── api.py                        # API処理
│   └── utils.py                      # ユーティリティ関数
└── README.md                         # このファイル
```

## 処理フロー

1. **Issueトリガー**: GitHub Issueが作成されると自動起動
2. **コード読み取り**: `src/`ディレクトリ内のPythonファイルを読み込み
3. **AI分析**: OpenAI APIでIssue内容とコードを分析
4. **仕様生成**: 実装仕様、受け入れ条件、ドキュメントを生成
5. **Jira連携**: 生成された内容でJiraチケットを作成
6. **Confluence連携**: ドキュメントページを作成

## ライセンス

MIT
