# CLAUDE.md — BMSG FAN DASHBOARD

## プロジェクト概要

BMSG（Be My Self Group）所属アーティスト（BE:FIRST / MAZZEL / HANA / SKY-HI / Novel Core / Aile The Shota / STARGLOW）の最新情報を毎日自動更新して表示するファンダッシュボード。

- **公開URL**: https://rrr-bit.github.io/bmsg-dashboard/
- **ホスティング**: GitHub Pages（mainブランチの `index.html` を直接配信）

## ファイル構成

```
bmsg-dashboard/
├── index.html              # 公開される静的HTMLダッシュボード
├── scripts/
│   └── generate.py         # Claude API + web検索でindex.htmlを自動生成するスクリプト
└── .github/
    └── workflows/
        └── update.yml      # 毎日9:00 JSTに generate.py を実行するCI/CDワークフロー
```

## 更新の仕組み

1. GitHub Actions（`update.yml`）が毎日UTC 00:00（JST 9:00）に起動
2. `generate.py` を実行
3. Claude API（claude-opus-4-5 + web_search_20250305 ツール）でBMSG最新情報をJSON取得
4. JSONからHTMLを生成し `index.html` を上書き
5. 変更をmainブランチにコミット・プッシュ
6. GitHub Pagesが自動的に更新を反映

## 必要なシークレット

| シークレット名 | 用途 |
|---|---|
| `ANTHROPIC_API_KEY` | GitHub Secrets に設定済みであること（未確認） |

## 開発上の注意

- `index.html` を直接編集しても、次回の自動更新で上書きされる
- コンテンツを永続的に変更したい場合は `generate.py` のプロンプトを修正する
- GAS（Google Apps Script）は使用していない
- YouTube APIキーは現在未設定（SNSタブのYouTude情報は静的プレースホルダー）
