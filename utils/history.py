import json
from datetime import datetime
from config import DATA_FILE_PATH


def write_history(score, death_cause):
    with open(DATA_FILE_PATH) as obj:
        data = json.load(obj)
        data["history"].append(
            {
                "created": int(datetime.now().timestamp()),
                "score": score,
                "death_cause": death_cause,
            }
        )

        if data["highest_score"] < score:
            data["highest_score"] = score

        with open(DATA_FILE_PATH, "w") as file:
            file.write(json.dumps(data))


def get_highest_score():
    with open(DATA_FILE_PATH) as file:
        score = json.load(file)["highest_score"]
        return score
