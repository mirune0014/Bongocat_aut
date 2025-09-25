# Bongocat Autoclicker

指定した座標を一定の間隔で自動クリックする、シンプルなGUIアプリです。クリック回数・連打間隔・繰り返し実行の間隔（分）を設定でき、記録はログファイルにも出力されます。PyAutoGUI のフェイルセーフ（画面左上にマウス移動で強制停止）に対応しています。

## 特長

- 座標取得ボタンで、5秒後のマウス位置を自動取得
- 1回あたりのクリック回数と連打間隔（秒）を指定
- 実行サイクルの間隔を分単位で指定（例: 31分ごと）
- フェイルセーフ（マウスを画面左上へ移動で即停止）
- 設定は `config.json` に自動保存、ログは `logs/bongo.log` に出力

## 画面項目

- クリック座標 (x, y)
- クリック回数
- 連打間隔（秒）
- 実行間隔（分）
- ボタン: Start / Stop / Exit / 位置を取得
- ログ表示欄

## 必要要件

- OS: Windows 10/11（他OSでも動作する可能性はありますが未検証）
- Python: 3.8 以上推奨
- 依存パッケージ: `pyautogui`（`tkinter`は標準同梱、PyAutoGUIの依存は自動で入ります）

## セットアップ

1) リポジトリのルートで仮想環境を作成（任意）

```powershell
python -m venv .venv
. .\.venv\Scripts\activate
```

2) 依存関係をインストール

```powershell
pip install -r requirements.txt
```

## 実行方法（ソースから）

```powershell
python src/app.py
```

手順:

1. 「位置を取得」を押すと、5秒後のマウス座標を自動取得します（カウント中に対象位置へマウスを移動してください）。
   - もしくは、x / y を手入力しても構いません。
2. 「クリック回数」「連打間隔（秒）」「実行間隔（分）」をお好みに設定します。
3. Start を押して開始します。Stop で停止できます。
4. 緊急停止したい場合は、マウスカーソルを画面左上へ移動してください（PyAutoGUI の FailSafe 機能）。
5. Exit でアプリを終了します。

## 設定ファイルとログ

- 設定: ルートの `config.json`

  ```json
  {
    "x": 100,
    "y": 200,
    "count": 3,
    "interval": 0.2,
    "period_min": 31
  }
  ```

- ログ: `logs/bongo.log`
  - クリック実行や開始/停止、エラーなどを記録します。

## ビルド（実行ファイルの作成）

PyInstaller を利用します。Windows では同梱のバッチでワンコマンドビルドが可能です。

- バッチを使う（推奨・Windows）

  ```powershell
  . .\.venv\Scripts\activate
  scripts\build_bongocat.bat
  ```

  成果物は `dist/Bongocat.exe` に生成されます。

- 直接コマンドで実行

  ```powershell
  pyinstaller --noconsole --onefile --clean --name "Bongocat" --icon assets\bongocat.ico src\app.py
  ```

プロジェクトには `Bongocat.spec` も同梱されています。PyInstaller の細かな調整が必要な場合に参照してください。

## フェイルセーフと注意事項

- フェイルセーフ: マウスを画面左上に移動すると即座に停止します（`pyautogui.FAILSAFE = True`）。
- 自動クリックは利用規約違反となるサービス・ゲームがあります。必ず自己責任でご利用ください。
- macOS や Linux で利用する場合、追加の権限（アクセシビリティ権限など）やライブラリが必要になることがあります。
