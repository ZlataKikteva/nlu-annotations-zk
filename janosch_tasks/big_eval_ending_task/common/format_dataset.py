import json
import copy

with open("big_eval_ending_task/resources/big_ending_revision_dataset.json") as f:
    samples = json.load(f)


NUMBER_OF_GROUPS = 130


def create_new_sample(i, meaning, grouping, ending_sample):
    new_sample = {}
    new_sample["story_id"] = i 
    new_sample["word"] = ending_sample["sample"]["word"]
    new_sample["judged_meaning"] = meaning
    new_sample["precontext"] = ending_sample["precontext"]
    new_sample["sentence"] = ending_sample["sample"]["revision"]
    new_sample["ending"] = ending_sample["revised_ending"]
    new_sample["sentence_info"] = {
        "author": ending_sample["sample"]["user_id"],
        "ID": ending_sample["sample"]["ID"],
        "meaning1": ending_sample["sample"]["meaning1"],
        "meaning2": ending_sample["sample"]["meaning2"],
        "meaning1_example": ending_sample["sample"]["meaning1_example"],
        "meaning2_example": ending_sample["sample"]["meaning2_example"],
        "original_sentence": ending_sample["sample"]["sentence"]
    }
    new_sample["ending_info"] = {
        "original_ending": ending_sample["ending"],
        "comment": ending_sample["comment"],
        "intended_meaning": ending_sample["meaning"]
    }
    new_sample["grouping"] = grouping

    return new_sample


def insert_attention_check(new_samples, i):
    new_samples[len(new_samples)+1] = {
        "story_id": "ATT",
        "word": "hard",
        "judged_meaning": "solid; not soft",
        "precontext": "The puzzle pieces were scattered across the table. We spent hours on the puzzle, but each piece seemed to fit nowhere.",
        "sentence": "It was a hard puzzle.",
        "ending": "",
        "sentence_info": {
            "author": "admin",
            "ID": -1,
            "meaning1": "solid; not soft.",
            "meaning2": "solid; not soft.",
            "meaning1_example": "The stone floor is hard.",
            "meaning2_example": "The stone floor is hard.",
            "original_sentence": "It was a hard puzzle."
        },
        "ending_info": {
            "original_ending": "",
            "comment": "",
            "intended_meaning": "solid; not soft."
        }
    }
    return new_samples

def main():
    new_samples = {}


    for i in samples:

        if i == "590":
            new_samples = insert_attention_check(new_samples, i)

        for ending_sample in samples[i]:
            
            sample = copy.deepcopy(ending_sample)

            for meaning in [sample["sample"]["meaning1"], sample["sample"]["meaning2"]]:
                new_sample = create_new_sample(i, meaning, len(new_samples) % NUMBER_OF_GROUPS, sample)
                new_samples[len(new_samples)+1] = new_sample
        # get endingless sample
        for meaning in [sample["sample"]["meaning1"], sample["sample"]["meaning2"]]:
            sample = copy.deepcopy(sample)
            sample["ending"] = ""
            sample["revised_ending"] = ""
            sample["ending_rating"] = -1
            new_sample = create_new_sample(i, meaning, len(new_samples) % NUMBER_OF_GROUPS, sample)
            new_samples[len(new_samples)+1] = new_sample

    with open("big_eval_ending_task/resources/annotation_samples.json", "w") as f:
        json.dump(new_samples, f, indent=4)


if __name__ == "__main__":
    main()
