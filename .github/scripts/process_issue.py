#!/usr/bin/env python3
"""
GitHub Issue を処理して Jira チケットと Confluence ページを自動生成するスクリプト
"""
import os
import sys
import json
import requests
from pathlib import Path


def read_source_code():
    """src/ ディレクトリ内のコードを読み取る"""
    src_dir = Path("src")
    code_content = {}
    
    if not src_dir.exists():
        print("警告: src/ ディレクトリが見つかりません")
        return code_content
    
    for file_path in src_dir.glob("**/*.py"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                relative_path = str(file_path.relative_to(src_dir))
                code_content[relative_path] = f.read()
        except Exception as e:
            print(f"ファイル読み込みエラー: {file_path} - {e}")
    
    return code_content


def generate_spec_with_openai(issue_title, issue_body, code_content):
    """OpenAI API を使って実装仕様と Jira チケット案を生成"""
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY が設定されていません")
    
    # コード情報を整形
    MAX_CODE_PREVIEW_LENGTH = 500
    code_summary = "\n\n".join([
        f"=== {filename} ===\n{content[:MAX_CODE_PREVIEW_LENGTH]}..."
        for filename, content in code_content.items()
    ])
    
    prompt = f"""
以下のGitHub Issueの内容と既存コードを分析して、実装仕様とJiraチケット案を生成してください。

【Issue タイトル】
{issue_title}

【Issue 内容】
{issue_body}

【既存コード】
{code_summary}

以下の形式でJSON形式で出力してください：
{{
  "summary": "チケットのタイトル（1行）",
  "description": "詳細な実装仕様",
  "acceptance_criteria": [
    "受け入れ条件1",
    "受け入れ条件2",
    "受け入れ条件3"
  ],
  "confluence_content": "Confluence用の詳細ドキュメント（マークダウン形式）"
}}
"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "あなたは優秀なソフトウェアエンジニアです。Issue内容とコードから実装仕様を作成します。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "response_format": {"type": "json_object"}
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        return json.loads(content)
    except Exception as e:
        print(f"OpenAI API エラー: {e}")
        raise


def create_jira_ticket(spec):
    """Jira API を使ってチケットを作成"""
    jira_url = os.environ.get('JIRA_URL')
    jira_email = os.environ.get('JIRA_EMAIL')
    jira_token = os.environ.get('JIRA_API_TOKEN')
    project_key = os.environ.get('JIRA_PROJECT_KEY')
    
    if not all([jira_url, jira_email, jira_token, project_key]):
        print("警告: Jira設定が不完全です。スキップします。")
        return None
    
    # 受け入れ条件を整形
    acceptance_criteria = "\n".join([
        f"* {criterion}" for criterion in spec.get('acceptance_criteria', [])
    ])
    
    description = f"{spec['description']}\n\n*受け入れ条件:*\n{acceptance_criteria}"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    payload = {
        "fields": {
            "project": {
                "key": project_key
            },
            "summary": spec['summary'],
            "description": description,
            "issuetype": {
                "name": "Task"
            }
        }
    }
    
    try:
        response = requests.post(
            f"{jira_url}/rest/api/3/issue",
            headers=headers,
            auth=(jira_email, jira_token),
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        jira_key = result.get('key')
        print(f"✓ Jiraチケット作成成功: {jira_key}")
        return jira_key
    except Exception as e:
        print(f"Jira API エラー: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"レスポンス: {e.response.text}")
        return None


def create_confluence_page(spec, jira_key=None):
    """Confluence API を使ってページを作成"""
    confluence_url = os.environ.get('CONFLUENCE_URL')
    confluence_email = os.environ.get('CONFLUENCE_EMAIL')
    confluence_token = os.environ.get('CONFLUENCE_API_TOKEN')
    space_key = os.environ.get('CONFLUENCE_SPACE_KEY')
    
    if not all([confluence_url, confluence_email, confluence_token, space_key]):
        print("警告: Confluence設定が不完全です。スキップします。")
        return None
    
    # ページタイトル
    title = spec['summary']
    if jira_key:
        title = f"[{jira_key}] {title}"
    
    # コンテンツを整形
    content = spec.get('confluence_content', spec['description'])
    
    # 受け入れ条件を追加
    acceptance_html = "<ul>" + "".join([
        f"<li>{criterion}</li>"
        for criterion in spec.get('acceptance_criteria', [])
    ]) + "</ul>"
    
    body_html = f"""
    <h2>概要</h2>
    <p>{content.replace('\n', '<br/>')}</p>
    
    <h2>受け入れ条件</h2>
    {acceptance_html}
    """
    
    if jira_key:
        body_html += f"""
        <h2>関連チケット</h2>
        <p>Jira: <a href="{os.environ.get('JIRA_URL')}/browse/{jira_key}">{jira_key}</a></p>
        """
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    payload = {
        "type": "page",
        "title": title,
        "space": {
            "key": space_key
        },
        "body": {
            "storage": {
                "value": body_html,
                "representation": "storage"
            }
        }
    }
    
    try:
        response = requests.post(
            f"{confluence_url}/rest/api/content",
            headers=headers,
            auth=(confluence_email, confluence_token),
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        page_id = result.get('id')
        print(f"✓ Confluenceページ作成成功: {page_id}")
        return page_id
    except Exception as e:
        print(f"Confluence API エラー: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"レスポンス: {e.response.text}")
        return None


def main():
    """メイン処理"""
    print("=== Issue 処理開始 ===")
    
    # 環境変数から Issue 情報を取得
    issue_number = os.environ.get('ISSUE_NUMBER')
    issue_title = os.environ.get('ISSUE_TITLE', '')
    issue_body = os.environ.get('ISSUE_BODY', '')
    
    print(f"Issue #{issue_number}: {issue_title}")
    
    # 1. ソースコードを読み取る
    print("\n[1/4] ソースコード読み取り中...")
    code_content = read_source_code()
    print(f"  ✓ {len(code_content)} ファイル読み込み完了")
    
    # 2. OpenAI で仕様を生成
    print("\n[2/4] OpenAI APIで仕様生成中...")
    try:
        spec = generate_spec_with_openai(issue_title, issue_body, code_content)
        print(f"  ✓ 仕様生成完了: {spec['summary']}")
    except Exception as e:
        print(f"  ✗ エラー: {e}")
        sys.exit(1)
    
    # 3. Jira チケット作成
    print("\n[3/4] Jiraチケット作成中...")
    jira_key = create_jira_ticket(spec)
    
    # 4. Confluence ページ作成
    print("\n[4/4] Confluenceページ作成中...")
    create_confluence_page(spec, jira_key)
    
    print("\n=== 処理完了 ===")
    if jira_key:
        print(f"Jiraチケット: {jira_key}")


if __name__ == "__main__":
    main()
