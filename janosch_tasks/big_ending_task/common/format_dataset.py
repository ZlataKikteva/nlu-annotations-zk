import json
import copy

INPUT_FILEPATH = "big_ending_task/resources/story_samples.json"
OUTPUT_FILEPATH = "big_ending_task/resources/annotation_samples.json"

NUMBER_OF_GROUPS = 65

with open("big_ambisentence_task/resources/all_word_senses.json", "r") as f:
    senses = json.load(f)

def get_example(word, gloss):
    for sense_dict in senses:
        if word == sense_dict["word"]:
            print(word, sense_dict)
            if sense_dict["gloss1"] == gloss:
                return sense_dict["example1"]
            if sense_dict["gloss2"] == gloss:
                return sense_dict["example2"]

    print("No example found for word ", word, gloss, "input example now")
    user_input = input("Example: ")
    senses.append({"word": word, "gloss1": gloss, "gloss2": gloss, "example1": user_input, "example2": user_input})
    return user_input

def main():
    with open(INPUT_FILEPATH, "r") as f:
        samples = json.load(f)

    new_samples = {}

    for i, sample in enumerate(samples):
        for meaning in sample["meaning1"], sample["meaning2"]:
            s = copy.deepcopy(sample)
            s_id = len(new_samples)
            s["displayed_meaning"] = meaning
            s["grouping"] = s_id % NUMBER_OF_GROUPS
            s["meaning1_example"] = get_example(s["word"], s["meaning1"])
            s["meaning2_example"] = get_example(s["word"], s["meaning2"])
            new_samples[s_id] = s

    with open(OUTPUT_FILEPATH, "w") as f:
        json.dump(new_samples, f, indent=4)



if __name__ == "__main__":
    main()