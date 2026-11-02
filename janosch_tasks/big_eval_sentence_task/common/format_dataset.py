import json


sets = ["testing/big_eval_ending/ambistory_ex/train.json", "testing/big_eval_ending/ambistory_ex/dev.json", "testing/big_eval_ending/ambistory_ex/test.json"]


NUMBER_OF_ANNOTATOR_GROUPS = 30


def insert_attention_check(new_samples, i):
    new_samples[len(new_samples)+1] = {
        "story_id": "ATT",
        "homonym": "hard",
        "judged_meaning": "solid; not soft",
        "precontext": "The puzzle pieces were scattered across the table. We spent hours on the puzzle, but each piece seemed to fit nowhere.",
        "sentence": "It was a hard puzzle.",
        "ending": "",
        "example_sentence": "The stone floor is hard.",
        "sample_id": "ATT"
    }
    return new_samples



def main():
    sentences = []
    sentence_samples = []
    for s in sets:
        with open(s, "r") as f:
            samples = json.load(f)
        for i in samples:
            sample = samples[i]
            if sample["sentence"] + sample["judged_meaning"] not in sentences:
                sentences.append(sample["sentence"] + sample["judged_meaning"])
                sample["precontext"] = ""
                sample["ending"] = ""
                sentence_samples.append(sample)

    annotation_samples = {}
    for i, sample in enumerate(sentence_samples):
        del sample["choices"]
        del sample["average"]
        del sample["stdev"]
        del sample["nonsensical"]
        sample["grouping"] = (i+1)% NUMBER_OF_ANNOTATOR_GROUPS
        annotation_samples[str(i+1)] = sample

    annotation_samples = insert_attention_check(annotation_samples, i+1)

    with open("big_eval_sentence_task/resources/annotation_samples.json", "w") as f:
        json.dump(annotation_samples, f, indent=4)



if __name__ == "__main__":
    main()