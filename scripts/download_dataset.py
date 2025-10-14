import sys
from datasets import load_dataset

def main():
    if len(sys.argv) != 3:
        print("Usage: python download_and_save_dataset.py <dataset_name> <output_path>")
        print("Example: python download_and_save_dataset.py dbarbedillo/SMS_Spam_Multilingual_Collection_Dataset /tmp/spam")
        sys.exit(1)

    dataset_name = sys.argv[1]
    output_path = sys.argv[2]

    print(f"Loading dataset: {dataset_name}")
    ds = load_dataset(dataset_name)

    print(f"Saving dataset to: {output_path}")
    ds.save_to_disk(output_path)

    print("Done.")

if __name__ == "__main__":
    main()
