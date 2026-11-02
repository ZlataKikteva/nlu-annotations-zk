import json

INPUT_FILEPATH = "ambistory2_task/resources/story_samples.json"



def main():
    new_samples = {}

    with open(INPUT_FILEPATH, "r") as f:
        samples = json.load(f)

    for i in samples:
        sample = samples[i]
        odds_or_evens = int(i) % 2

        new_samples[str(1 + (int(i)-1) * 2)] = {"word": sample["word"], "meaning1": sample["meaning1"], "meaning2": sample["meaning2"], "meaning": sample["meaning1"], "precontext": sample["precontext"], "sentence": sample["sentence"], "grouping": odds_or_evens * 2}
        new_samples[str(1 + (int(i)-1) * 2 + 1)] = {"word": sample["word"], "meaning1": sample["meaning1"], "meaning2": sample["meaning2"], "meaning": sample["meaning2"], "precontext": sample["precontext"], "sentence": sample["sentence"], "grouping": odds_or_evens * 2 + 1}

    with open("ending_task/resources/story_samples.json", "w") as f:
        json.dump(new_samples, f, indent=4)

if __name__ == "__main__":
    main()