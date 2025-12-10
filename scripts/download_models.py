#!/usr/bin/env python3
import sys
from huggingface_hub import snapshot_download

def main():
    if len(sys.argv) != 3:
        print("Usage: python download_models.py <repo_id> <local_dir>")
        print("Example: python download_models.py prajjwal1/bert-mini models/prajjwal1_bert-mini")
        sys.exit(1)

    repo_id = sys.argv[1]
    local_dir = sys.argv[2]

    print(f"Downloading HuggingFace model:")
    print(f"  Repo ID:   {repo_id}")
    print(f"  Local dir: {local_dir}\n")

    snapshot_download(
        repo_id=repo_id,
        local_dir=local_dir,
        local_dir_use_symlinks=False  # ensures full copies, safest for HPC
    )

    print(f"\nDownload complete!")
    print(f"Model saved to: {local_dir}")
    print("You can now load it offline with AutoModel / AutoTokenizer.")

if __name__ == "__main__":
    main()
