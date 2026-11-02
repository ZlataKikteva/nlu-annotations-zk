import json
import random

with open("adv_eval_ending_task2/resources/stage2_samples.json", "r") as f:
    samples = json.load(f)

# Since there is an even number of annotator groups with same domain, the same people will end up always getting meaning1 or meaning2.
# So we swap that around a bit

new_samples = {}

for i in samples:
    if int(i) <= 628:

        if int(i) % 2 != 1:
            continue
        sample = samples[i]

        next_sample = samples[str(int(i)+1)]

        if sample["sentence"] != next_sample["sentence"]:
            print("Warning!!!", sample["sentence"], next_sample["sentence"])

        annotators = [sample["grouping"], next_sample["grouping"]]
        random.shuffle(annotators)
        sample["grouping"] = annotators[0]
        next_sample["grouping"] = annotators[1]

        new_samples[i] = sample
        new_samples[str(int(i)+1)] = next_sample 

    else: 
        new_samples[i] = samples[i]

with open("adv_eval_ending_task2/resources/better_stage2_samples.json", "w") as f:
    json.dump(new_samples, f, indent=4)