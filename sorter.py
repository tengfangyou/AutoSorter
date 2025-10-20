import argparse
import json
import os
import shutil
import time
from typing import Dict, List

# ========== 預設設定 ==========
DEFAULT_DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
DEFAULT_CONFIG_FILE = "config.json"
DEFAULT_LOG_FILE = "autosorter.log"
# ==============================


def load_rules(config_path: str) -> Dict[str, List[str]]:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 將所有副檔名轉小寫，去除可能的點號
    norm = {}
    for folder, exts in data.items():
        norm[folder] = [e.lower().lstrip(".") for e in exts]
    return norm


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def safe_move(src: str, dst: str) -> str:
    """
    若目標已存在同名檔案，於檔名後面加上 (1)、(2)...
    回傳實際移動到的目標路徑。
    """
    base, ext = os.path.splitext(dst)
    candidate = dst
    counter = 1
    while os.path.exists(candidate):
        candidate = f"{base} ({counter}){ext}"
        counter += 1
    shutil.move(src, candidate)
    return candidate


def log(message: str, log_file: str, quiet: bool = False) -> None:
    if not quiet:
        print(message)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")


def detect_category(filename: str, rules: Dict[str, List[str]]) -> str:
    # 沒有副檔名 → Others
    if "." not in filename or filename.startswith("."):
        return "Others"
    ext = filename.rsplit(".", 1)[-1].lower()
    for folder, exts in rules.items():
        if ext in exts:
            return folder
    return "Others"


def sort_once(
    target_dir: str, rules: Dict[str, List[str]], log_file: str, dry_run: bool, quiet: bool
) -> None:
    if not os.path.isdir(target_dir):
        raise NotADirectoryError(f"Not a directory: {target_dir}")

    entries = os.listdir(target_dir)
    if not entries and not quiet:
        print("No files found. Directory is empty.")

    for name in entries:
        src_path = os.path.join(target_dir, name)

        # 只處理檔案，跳過資料夾與連結
        if not os.path.isfile(src_path):
            continue

        # 決定分類
        category = detect_category(name, rules)
        dest_dir = os.path.join(target_dir, category)
        dest_path = os.path.join(dest_dir, name)

        # 執行
        if dry_run:
            log(f"[DRY RUN] {name} → {category}/", log_file, quiet=quiet)
        else:
            try:
                ensure_dir(dest_dir)
                final_path = safe_move(src_path, dest_path)
                log(f"Moved: {name} → {os.path.relpath(final_path, target_dir)}", log_file, quiet=quiet)
            except Exception as e:
                log(f"Error moving {name}: {e}", log_file, quiet=quiet)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Auto-sort files in a directory by extension according to config.json"
    )
    p.add_argument(
        "--path",
        default=DEFAULT_DOWNLOAD_DIR,
        help=f"要整理的資料夾（預設為目前使用者的 Downloads） e.g. {DEFAULT_DOWNLOAD_DIR}",
    )
    p.add_argument(
        "--config",
        default=DEFAULT_CONFIG_FILE,
        help="分類規則檔（預設 config.json）",
    )
    p.add_argument(
        "--log",
        default=DEFAULT_LOG_FILE,
        help="記錄檔路徑（預設 autosorter.log）",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="試跑模式：只顯示將要移動的結果，不實際移動檔案",
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="靜音模式：不印出終端訊息，只寫入 log",
    )
    return p.parse_args()


def main():
    args = parse_args()
    rules = load_rules(args.config)

    print("=== AutoSorter ===")
    print(f"Target directory: {args.path}")
    if args.dry_run:
        print("Mode: DRY RUN (不會實際移動檔案)")
    print("==================")

    sort_once(
        target_dir=args.path,
        rules=rules,
        log_file=args.log,
        dry_run=args.dry_run,
        quiet=args.quiet,
    )

    if not args.quiet:
        print("Done.")


if __name__ == "__main__":
    main()
