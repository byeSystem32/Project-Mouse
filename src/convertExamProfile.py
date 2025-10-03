from pathlib import Path
import json
import sys
from datetime import datetime

def setup_exam_structure(json_path, exam_folder_name):
    # Base directory = folder where this script lives
    base_dir = Path(__file__).parent.resolve()
    # Always build exams inside mouseV1/past_exams
    past_exams_dir = base_dir / "mouseV1" / "past_exams"

    # Root dir for this specific exam
    root_dir = past_exams_dir / exam_folder_name
    questions_dir = root_dir / "questions"
    questions_dir.mkdir(parents=True, exist_ok=True)

    # Load exam profile JSON
    json_path = Path(json_path).resolve()
    with open(json_path, "r") as f:
        exam_json = json.load(f)

    # Setup index.json skeleton
    index_data = {
        "exam_name": f"{datetime.now().strftime("%B")} {exam_json['exam_name']}",
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "questions": []
    }

    # Create section + question folders
    for section in exam_json["sections"]:
        section_name = section["section_name"]
        num_questions = int(section["number_of_questions"])

        for q in range(1, num_questions + 1):
            qid = f"Q{q}"
            folder_name = f"{section_name.replace(' ', '_')}_{qid}"
            q_folder = questions_dir / folder_name
            photos_folder = q_folder / "photos"
            photos_folder.mkdir(parents=True, exist_ok=True)

            # Write per-question metadata
            q_metadata = {
                "section": section_name,
                "id": qid,
                "photos": []
            }
            with open(q_folder / "question_metadata.json", "w") as f:
                json.dump(q_metadata, f, indent=2)

            # Add entry to index.json
            index_data["questions"].append({
                "section": section_name,
                "id": qid,
                "prompt": "",
                "folder_path": str(Path("questions") / folder_name),  # relative path
                "photo_count": 0,
                "on_question": False
            })

    # Write index.json at the root of this exam
    with open(root_dir / "index.json", "w") as f:
        json.dump(index_data, f, indent=2)

    print(f"✅ Exam folder created at: {root_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python setup_exam.py <path_to_exam_json> <exam_folder_name>")
        sys.exit(1)

    exam_file = sys.argv[1]
    exam_folder = sys.argv[2]
    setup_exam_structure(exam_file, exam_folder)