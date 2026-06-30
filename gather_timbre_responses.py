import csv
import json
from pathlib import Path


def parse_response_key(key):
    """Parse response keys like '1, Primed,Trumpet,Anachronistic, Powerful'."""
    parts = [part.strip() for part in key.split(",")]

    # Expected format: block_number, condition, instrument, timing, correct_word
    if len(parts) != 5:
        return None

    block_number, condition, instrument, style, correct = parts
    if block_number not in {"1", "2"}:
        return None
    if condition not in {"Primed", "Un", "Unprimed"}:
        return None

    return {
        "block_number": block_number,
        "condition": condition,
        "instrument": instrument,
        "style": style,
        "correct": correct,
    }


def determine_target_indices(trials):
    """
    Determine target trial indices dynamically from the response keys.
    This avoids relying on a brittle hard-coded range when the block order changes.
    """
    target_indices = set()
    first_block_info = None

    for trial in trials:
        trial_index = trial.get("trial_index")
        response = trial.get("response", {})

        if not isinstance(response, dict):
            continue

        for key, value in response.items():
            if not isinstance(value, list):
                continue

            parsed = parse_response_key(key)
            if parsed is None:
                continue

            target_indices.add(trial_index)
            if first_block_info is None:
                first_block_info = parsed
            break

    return target_indices, first_block_info


def gather_timbre_responses():
    folder_path = Path("data/timbre_descriptions")
    gathered_responses = []

    for participant_id, json_file in enumerate(sorted(folder_path.glob("*.json")), start=1):
        participant = participant_id
        print(f"Processing file: {json_file.name} as Participant {participant}")

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        target_indices, first_block_info = determine_target_indices(data.get("trials", []))
        if first_block_info:
            print(
                "Detected first block as "
                f"Block {first_block_info['block_number']} / "
                f"{first_block_info['condition']}"
            )

        participant_trial_number = 0
        for trial in data.get("trials", []):
            trial_index = trial.get("trial_index")
            if trial_index not in target_indices:
                continue

            participant_trial_number += 1
            response = trial.get("response", {})
            for key, value in response.items():
                if not isinstance(value, list):
                    continue

                parsed = parse_response_key(key)
                if parsed is None:
                    continue

                gathered_responses.append(
                    {
                        "participant": participant,
                        "trial_number": participant_trial_number,
                        "instrument": parsed["instrument"],
                        "style": parsed["style"],
                        "priming": parsed["condition"],
                        "correct": parsed["correct"],
                        "descriptions": value,
                    }
                )
                break

    return gathered_responses


def write_to_csv(responses, filename="timbre_responses.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(
            [
                "Participant",
                "Trial",
                "Priming",
                "Instrument",
                "Style",
                "Correct",
                "Description",
                "Score",
            ]
        )

        all_data = []
        for response in responses:
            for index, desc in enumerate(response["descriptions"]):
                score = len(response["descriptions"]) - index
                all_data.append(
                    (
                        response["participant"],
                        response["trial_number"],
                        response["priming"],
                        response["instrument"],
                        response["style"],
                        response["correct"],
                        desc,
                        score,
                    )
                )

        all_data.sort(
            key=lambda x: (
                x[0],
                x[1],
                x[2],
                x[3],
                x[4],
                x[5],
            )
        )

        for participant, trial_number, priming, instrument, style, correct, desc, score in all_data:
            writer.writerow(
                [participant, trial_number, priming, instrument, style, correct, desc, score]
            )


if __name__ == "__main__":
    responses = gather_timbre_responses()

    write_to_csv(responses)
    print("Results written to timbre_responses.csv")

    print("\nResults sorted by Participant:")
    all_data = []
    for response in responses:
        scored_list = [
            (desc, len(response["descriptions"]) - index)
            for index, desc in enumerate(response["descriptions"])
        ]
        all_data.append(
            (
                response["participant"],
                response["instrument"],
                response["style"],
                response["priming"],
                response["correct"],
                scored_list,
            )
        )

    all_data.sort(key=lambda x: (x[0], x[1], x[2], x[3], x[4]))

    current_participant = None
    for participant, instrument, style, priming, correct, scored_list in all_data:
        if participant != current_participant:
            if current_participant is not None:
                print()
            print(f"Participant {participant}:")
            current_participant = participant
        print(f"  {instrument},{style},{priming},{correct}: {scored_list}")