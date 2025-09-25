# src/app.py
import threading
import time
import json
import logging
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui

APP_TITLE = "Bongocat Autoclicker"
CFG_PATH = Path(__file__).resolve().parent.parent / "config.json"
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "bongo.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

class BongoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("420x260")
        self.resizable(False, False)

        pyautogui.FAILSAFE = True  # 左上で強制停止

        # 状態
        self.running = False
        self.worker = None
        self.click_x = tk.IntVar(value=0)
        self.click_y = tk.IntVar(value=0)
        self.click_count = tk.IntVar(value=3)      # 1回あたりのクリック数
        self.click_interval = tk.DoubleVar(value=0.2)  # 連打間隔（秒）
        self.period_min = tk.DoubleVar(value=31)   # 繰り返し間隔（分）

        self._load_config()
        self._build_ui()

    # UI
    def _build_ui(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        # 座標
        row = 0
        ttk.Label(frm, text="クリック座標 (x, y):").grid(column=0, row=row, sticky="w")
        ttk.Entry(frm, width=7, textvariable=self.click_x).grid(column=1, row=row)
        ttk.Entry(frm, width=7, textvariable=self.click_y).grid(column=2, row=row)
        ttk.Button(frm, text="位置を取得", command=self.pick_position).grid(column=3, row=row, padx=6)

        # パラメータ
        row += 1
        ttk.Label(frm, text="クリック回数:").grid(column=0, row=row, sticky="w")
        ttk.Entry(frm, width=7, textvariable=self.click_count).grid(column=1, row=row, sticky="w")
        ttk.Label(frm, text="連打間隔(秒):").grid(column=2, row=row, sticky="w")
        ttk.Entry(frm, width=7, textvariable=self.click_interval).grid(column=3, row=row, sticky="w")

        row += 1
        ttk.Label(frm, text="実行間隔(分):").grid(column=0, row=row, sticky="w")
        ttk.Entry(frm, width=7, textvariable=self.period_min).grid(column=1, row=row, sticky="w")

        # ボタン
        row += 1
        btns = ttk.Frame(frm)
        btns.grid(column=0, row=row, columnspan=4, pady=(10, 0))
        ttk.Button(btns, text="Start", command=self.start).pack(side="left", padx=6)
        ttk.Button(btns, text="Stop", command=self.stop).pack(side="left", padx=6)
        ttk.Button(btns, text="Exit", command=self.on_exit).pack(side="left", padx=6)

        # ログ表示
        row += 1
        self.log_text = tk.Text(frm, height=6, width=48, state="disabled")
        self.log_text.grid(column=0, row=row, columnspan=4, pady=(10, 0))
        self._log("準備完了。位置を取得して Start を押してください。")

    def _log(self, msg: str):
        logging.info(msg)
        self.log_text.configure(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    # 設定
    def _load_config(self):
        if CFG_PATH.exists():
            try:
                cfg = json.loads(CFG_PATH.read_text(encoding="utf-8"))
                self.click_x.set(cfg.get("x", 0))
                self.click_y.set(cfg.get("y", 0))
                self.click_count.set(cfg.get("count", 3))
                self.click_interval.set(cfg.get("interval", 0.2))
                self.period_min.set(cfg.get("period_min", 31))
            except Exception as e:
                logging.warning(f"設定の読み込みに失敗: {e}")

    def _save_config(self):
        cfg = dict(
            x=self.click_x.get(),
            y=self.click_y.get(),
            count=self.click_count.get(),
            interval=self.click_interval.get(),
            period_min=self.period_min.get(),
        )
        CFG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")

    # 機能
    def pick_position(self):
        self._log("5秒後に現在のマウス座標を取得します。")
        self.after(5000, self._capture_position)

    def _capture_position(self):
        x, y = pyautogui.position()
        self.click_x.set(x)
        self.click_y.set(y)
        self._save_config()
        self._log(f"座標を設定しました: ({x}, {y})")

    def start(self):
        if self.running:
            return
        if self.click_x.get() <= 0 and self.click_y.get() <= 0:
            messagebox.showwarning(APP_TITLE, "クリック座標が未設定です。")
            return
        self.running = True
        self._save_config()
        self._log("開始します。Stop で停止できます。")
        self.worker = threading.Thread(target=self._run_loop, daemon=True)
        self.worker.start()

    def stop(self):
        if not self.running:
            return
        self.running = False
        self._log("停止要求を受け付けました。次のタイミングで停止します。")

    def _run_loop(self):
        while self.running:
            try:
                # クリックバースト
                x, y = self.click_x.get(), self.click_y.get()
                for _ in range(int(self.click_count.get())):
                    pyautogui.click(x, y)
                    time.sleep(float(self.click_interval.get()))
                self._log(f"クリック実行: ({x}, {y})")

                # 所定の間隔だけ待つ（早めの停止に反応するため細切れにsleep）
                total = float(self.period_min.get()) * 60.0
                step = 0.5
                waited = 0.0
                while self.running and waited < total:
                    time.sleep(step)
                    waited += step
            except pyautogui.FailSafeException:
                self._log("FailSafe 発動（左上にマウス移動）。停止します。")
                self.running = False
            except Exception as e:
                self._log(f"エラー: {e}")
                self.running = False

    def on_exit(self):
        self.stop()
        self.after(200, self.destroy)

if __name__ == "__main__":
    app = BongoApp()
    app.mainloop()
