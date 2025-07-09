# cleanup_unused.py
import shutil
from pathlib import Path

REMOVE_PATHS = [
    "articles",
    "scripts/articles",
    "logs",
    "icons",
    "docs",
]

print("🧹 不要なディレクトリ・ファイルを削除します...\n")

for path in REMOVE_PATHS:
    p = Path(path)
    if p.exists():
        if p.is_dir():
            shutil.rmtree(p)
            print(f"🗑️ 削除: {path}/")
        else:
            p.unlink()
            print(f"🗑️ 削除: {path}")
    else:
        print(f"✅ スキップ（既に存在しない）: {path}")

print("\n🎉 クリーンアップ完了！")
