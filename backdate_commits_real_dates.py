import os
import subprocess
from datetime import datetime, timedelta

# === CONFIGURATION ===
REPO_DIR = "."  # Change to "." to use current folder
COMMIT_FILE = "commit_messages.txt"
NUM_COMMITS = 1000

def load_commit_messages(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if len(lines) < NUM_COMMITS:
        raise ValueError(f"Expected at least {NUM_COMMITS} unique commit messages.")
    return lines[:NUM_COMMITS]

def generate_real_dates(n):
    today = datetime.now()
    return [(today - timedelta(days=i)).strftime("%Y-%m-%dT12:00:00") for i in range(n)]

def setup_repo(path):
    if not os.path.exists(path):
        os.makedirs(path)
        subprocess.run(["git", "init"], cwd=path)
    elif not os.path.exists(os.path.join(path, ".git")):
        subprocess.run(["git", "init"], cwd=path)

def make_commit(repo_path, message, date_iso):
    dummy_file = os.path.join(repo_path, "log.txt")
    with open(dummy_file, "a", encoding="utf-8") as f:  # UTF-8 write
        f.write(f"{message}\n")

    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_iso
    env["GIT_COMMITTER_DATE"] = date_iso

    subprocess.run(["git", "add", "."], cwd=repo_path, env=env)
    subprocess.run(["git", "commit", "-m", message], cwd=repo_path, env=env)

def main():
    print("📄 Loading commit messages...")
    messages = load_commit_messages(COMMIT_FILE)
    dates = generate_real_dates(NUM_COMMITS)

    print(f"📁 Setting up Git repo at: {REPO_DIR}")
    setup_repo(REPO_DIR)

    print("⏳ Creating commits with real dates (one per day)...")
    for i in range(NUM_COMMITS):
        print(f"📦 Commit {i+1}/{NUM_COMMITS} → {dates[i]} | {messages[i]}")
        make_commit(REPO_DIR, messages[i], dates[i])

    print("\n✅ Done! All commits backdated using real dates.")

if __name__ == "__main__":
    main()
