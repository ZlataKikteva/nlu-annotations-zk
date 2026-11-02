import json

NUMBER_OF_WANTED_GROUPS = 30


def main():
    with open("big_eval_ending_task/resources/ready_samples.json", "r") as f:
        samples = json.load(f)

    new_samples = {}
    for i in samples:
        sample = samples[i]
        if ("grouping" not in sample) or (sample["grouping"] < NUMBER_OF_WANTED_GROUPS):
            sample["og_index"] = i
            new_samples[len(new_samples)+1] = sample

    with open("big_eval_ending_task/resources/annotation_samples_30.json", "w") as f:
        json.dump(new_samples, f, indent=4)


if __name__ == "__main__":
    main()