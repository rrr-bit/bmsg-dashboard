# Next Actions

## 方針

現在のシステムの**作り直しではなく**、既存実装の整備・安定稼働を目的とする。

---

## 優先度：高

### 1. generate.py にSNSタブを追加する（手動版との統合）

**背景**: 現在の `index.html`（手動版）にはSNSタブ（Xタイムライン・YouTube）があるが、`generate.py` が生成するHTMLには含まれていない。次回の自動更新でSNSタブが消える。

**対応方針**:
- `generate.py` のHTML生成部分にSNSタブのコードを追加（静的コンテンツとして埋め込み）
- XタイムラインはAPIキー不要のtwitter-timeline埋め込みで維持

**未確認事項**: 自動更新が実際に正常稼働しているか（`ANTHROPIC_API_KEY` が設定されているか）

---

### 2. ANTHROPIC_API_KEY の設定確認

**背景**: GitHub Actions ワークフローは設定済みだが、`ANTHROPIC_API_KEY` シークレットが実際にリポジトリに設定されているか未確認。キーがなければ毎日の自動更新は失敗している。

**対応方針**:
- GitHub リポジトリの Settings > Secrets and variables > Actions で確認・設定
- ワークフローの手動実行（workflow_dispatch）で動作確認

---

## 優先度：中

### 3. generate.py の出力HTMLにバズ投稿欄を追加

**背景**: 手動版 `index.html` には「直近24h バズ投稿 TOP10」欄があるが、現在は静的プレースホルダーのみ。`generate.py` のClaudeプロンプトにバズ投稿収集を追加すれば実現可能。

**対応方針**:
- `generate.py` のJSONスキーマに `buzz` セクションを追加
- Claudeプロンプトにバズ投稿収集指示を追加
- HTMLテンプレートにbuzzセクションを追加

---

### 4. コンテンツの最新性確認

**背景**: 現在公開中の `index.html` には2026年2月時点のコンテンツが手動入力されている。自動更新が正常稼働していれば最新のはずだが、未確認。

**対応方針**:
- GitHub Actions の実行履歴を確認
- 自動更新が機能していない場合は手動で `generate.py` を実行して更新

---

## 優先度：低

### 5. YouTube最新動画の自動取得

**背景**: YouTube情報は「APIキー設定後...」の静的表示になっている。実装するにはYouTube Data API v3のキーが必要。

**対応方針**:
- YouTube Data API v3 キーを取得（Google Cloud Console）
- `generate.py` にYouTube API呼び出しを追加
- または、Claudeのweb検索でYouTube最新動画タイトルを取得する方法も検討

**未確認事項**: YouTube APIキー取得の意思決定が必要

---

### 6. docs/ ディレクトリの整備

**背景**: 現在 `docs/` ディレクトリは存在しない。今後の設計・仕様ドキュメントを整理する場合に作成。

**対応方針**: 必要に応じて作成。現時点では不要。

---

## 実施しないこと（スコープ外）

- システムの全面作り直し
- GASの導入（現在GitHub Actionsで完結しており不要）
- フレームワーク導入（React/Vue等 — 静的HTMLで十分）
- DBの導入（JSONで十分）
