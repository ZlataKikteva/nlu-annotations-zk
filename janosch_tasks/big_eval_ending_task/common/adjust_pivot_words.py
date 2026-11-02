import json
import string


INPUT_FILEPATH = "big_eval_ending_task/resources/annotation_samples_130.json"
OUTPUT_FILEPATH = "big_eval_ending_task/resources/ready_samples.json"


with open(INPUT_FILEPATH, "r") as f:
    samples = json.load(f)

sentences_to_word = {}


def check_for_discrepancy(sample):
    word = sample["word"]
    sentence = sample["sentence"]

    if sentence in sentences_to_word:
        return sentences_to_word[sentence]

    no_punc_sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    split_sentence = no_punc_sentence.split()
    if word in split_sentence:
        print("OK", word, split_sentence)
        sentences_to_word[sentence] = word
        return word
    else:
        print(word, " NOT IN ", split_sentence)
        print("write the word that is actually used")
        new_word = input("write: ")
        sentences_to_word[sentence] = new_word
        return new_word


def main():

    new_samples = {}
    for i in samples:
        print(i)
        sample = samples[i]
        new_word = check_for_discrepancy(sample)
        sample["og_word"] = sample["word"]
        sample["word"] = new_word
        new_samples[i] = sample

        with open(OUTPUT_FILEPATH, "w") as f:
            json.dump(new_samples, f, indent=4)
    


if __name__ == "__main__":
    main()