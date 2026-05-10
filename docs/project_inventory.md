# Project Inventory — bmsg-dashboard

## 1. PJ概要

BMSG所属アーティストのライブ、イベント、FC先行、新曲、グッズ、SNS更新などを毎日自動で集約・表示するファンダッシュボード。

公開URL: https://rrr-bit.github.io/bmsg-dashboard/

## 2. 目的

- BE:FIRST / MAZZEL / HANA / SKY-HI などBMSG関連情報を一元管理する
- 毎朝自動更新されるファン向け情報ダッシュボードにする
- 将来的にはSNSバズ投稿、YouTube最新動画、FC先行情報なども一覧化する

## 3. 現在GitHub上で確認できた状態

- README.md は存在し、公開URLが記載されている
- GitHub Pagesで公開されている
- PR #1 `docs: プロジェクト実装状況の把握と方針ドキュメントを追加` が存在
- PR #1 は draft / open / mergeable=true
- PR #1 では CLAUDE.md / implementation_log.md / next_actions.md を追加している
- PR #1 上の調査では、GitHub Actions + Claude API による毎日自動更新構成とされている

## 4. 現在の主要論点

### 優先度A

- PR #1をレビューしてmainへマージするか判断する
- generate.py生成版と手動index.htmlの差異を解消する
- 特にSNSタブが自動生成で消える可能性を解消する
- ANTHROPIC_API_KEYがGitHub Secretsに設定されているか確認する

### 優先度B

- YouTube最新動画取得を実装するか判断する
- バズ投稿TOP10を実装するか判断する
- docs/配下に仕様を整理する

## 5. 未確認事項

- GitHub Actionsが直近で正常実行されているか
- ANTHROPIC_API_KEYが設定済みか
- 現在公開中のindex.htmlが手動版か自動生成版か
- YouTube APIキーを使うのか、Claudeのweb検索で代替するのか
- バズ投稿の取得対象をXにするのか、YouTube/ニュース/公式情報も含めるのか

## 6. 次アクション

1. PR #1をレビュー
2. PR #1をマージするか判断
3. SNSタブ維持のIssue化
4. GitHub Actionsの実行確認
5. バズ投稿/YouTube取得の要件定義
6. README.mdを運用実態に合わせて更新

## 7. 運用ルール

- GitHub Pagesで公開する静的ダッシュボードとして維持する
- index.htmlを直接編集する場合、自動生成で上書きされるリスクを明記する
- 永続変更はgenerate.py側へ反映する
- 実装アイデアはIssue化してから着手する
- Claude CodeはIssue単位で作業する
