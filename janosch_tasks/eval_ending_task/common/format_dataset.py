import json
import copy

with open("testing/ending_database.json") as f:
    users = json.load(f)

with open("ending_task/resources/story_samples.json") as f:
    stories = json.load(f)

MODS_KILL_THIS_GUY = ["9V3BP7L4"]

samples = [{} for i in range(160)]
for user in users:
    if user["task"] != "ending_task":
        continue
    if "test" in user["data"]["prolific_id"].lower() or "burner" in user["data"]["prolific_id"].lower():
        continue
    if user["qualified"] != 1:
        continue 
    if user["User ID"] == MODS_KILL_THIS_GUY:
        continue

    for i, annotation in enumerate(user["annotations"]["annotation"]):
        if annotation:
            samples[i*2] = copy.deepcopy(annotation)
            samples[i*2]["grouping"] = (i*2) % 4
            samples[i*2]["displayed_meaning"] = stories[str(i+1)]["meaning1"]
            samples[i*2]["word"] = stories[str(i+1)]["word"]
            samples[i*2+1] = copy.deepcopy(annotation)
            samples[i*2+1]["grouping"] = (i*2+1) % 4
            samples[i*2+1]["displayed_meaning"] = stories[str(i+1)]["meaning2"]
            samples[i*2+1]["word"] = stories[str(i+1)]["word"]

    dict_samples = {}
    for i, sample in enumerate(samples):
        dict_samples[str(i+1)] = sample
    
with open("eval_ending_task/resources/story_samples.json", "w") as f:
    json.dump(dict_samples, f, indent=4)

    