from pathlib import Path

def find_project_root(filename=".git") -> Path:
    current_path = Path.cwd()

    for parent in current_path.parents:
        if (parent / filename).exists():
            return parent
    raise FileNotFoundError(f"Could not find {filename} in any parent directories.")

def preprocess_data(file_path: Path) -> None:
    print(f"Processing data...")
    import json
    with open(str(file_path), mode="r", encoding="utf-8") as f:
        raw_data = json.load(f)

    raw_data = raw_data["messages"]
    data = []
    for raw_message in raw_data:
        if (not "content" in raw_message) or ("share" in raw_message):
            continue
        message = {}
        if raw_message["sender_name"] == "Viven Iyer":
            message["label"] = 0
        elif raw_message["sender_name"] == "Sangeetha":
            message["label"] = 1
        message["text"] = raw_message["content"]
        data.append(message)
    with open("data/dataset.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)