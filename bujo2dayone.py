import argparse
import re
from dayonewriter import Entry, dayonewriter
from datetime import datetime
from PyInquirer import prompt


def add_bullet(s: str) -> str:
    if s.startswith(" "):
        return f"  - {s.lstrip()}"
    else:
        return f"- {s}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add image of bujo with transcription to DayOne"
    )
    parser.add_argument(
        "--journal",
        help="Name of the Journal the entry should be created in",
    )

    parser.add_argument("--image", help="Path to the image")

    args = parser.parse_args()

    # ask for the lines
    lines = []
    while True:
        questions = [
            {
                "type": "input",
                "name": "input",
                "message": "Input",
            }
        ]

        answers = prompt(questions)
        if (answer := answers.get("input")) == "":
            break
        else:
            lines.append(answer)

    # make bullet points out of the lines
    bullet_points = list(map(add_bullet, lines))
    # add the photo to the beginning of the entry
    bullet_points.insert(0, "[{photo}]")

    date_str = re.search(r"\d{4}-\d{2}-\d{2}", args.image).group(0)

    entry = Entry()
    entry.date = datetime.strptime(f"{date_str}-12-00", "%Y-%m-%d-%H-%M")
    entry.text = "\n".join(bullet_points)
    # entry.tags = ["bujo"]
    entry.photos = [args.image]
    entry.journal = args.journal

    entry_id = dayonewriter(entry)
