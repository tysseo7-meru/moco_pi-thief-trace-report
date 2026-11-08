# 疑惑リスト作成時のアーカイブ（2024年）

Pi 疑惑アドレスリスト（findsp2.l_spam.txt、8,132件）を作成した当時のプログラムと
出力ファイルを保存したものです。2026年11月8日、作成者の Google ドライブにあった
アーカイブ（trace.tgz / trace2.tgz）を展開して収録しました。

## 中身

- `part1/` — trace.tgz の中身（part 1 の作業一式）
  - `sa2405.txt` — 芯のリスト（485行、重複を除くと278アドレス）
  - `findsp_resd_out.txt` — 途中版のリスト（7,967件）
  - `findsp.py`、`v3.05.py` ほか、作成に使ったプログラムとログ
- `part2/` — trace2.tgz の中身（part 2 の作業一式）
  - `findsp2.l_spam.txt` — part 1 の最終出力（8,132件。解析レポートの対象リストと完全一致）
  - `findsp3.l_spam.txt` — 物差しを 499 Pi に下げた版のリスト（12,932件）
  - `findsp2.py`、`findsp3.py`、`findsp_resd.py` ほか、プログラムとログ

作成方法の詳細は、解析レポート（pi_thief_trace_report.html）の付録に記録しています。
本リポジトリの解析の対象は、findsp2.l_spam.txt の 8,132 件のみです。

## 収録していないもの

- `*.l_pays.tcl`（4ファイル、各 83〜159 MB）— 取得した送金履歴の中間データ。
  GitHub のファイルサイズ制限を超えるため収録していません（作成者の手元に保管）。
- `from_GING.txt`、`from_GING_test.txt` — 関係者から提供されたアドレスのデータのため、
  公開には含めていません（アーカイブ原本には含まれています）。
