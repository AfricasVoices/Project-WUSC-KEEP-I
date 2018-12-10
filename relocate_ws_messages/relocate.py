import os
import json
import argparse

WS_key = "code-WS-adb25603b7af"

code_to_dataset = {
  "code-6e49c8f2bba3" : "WUSC_KEEP_II_Aisha",
  "code-e3b32d7a4ffb" : "WUSC_KEEP_II_Amina",
  "code-b4007d8c0fa5" : "WUSC_KEEP_II_Mohamed",
  "code-075ee91c6ddb" : "WUSC_KEEP_II_Zamzam",
  "code-c2cf9e4e3016" : "WUSC_KEEP_II_Demogs_Age",
  "code-daa3c33b9e5b" : "WUSC_KEEP_II_Demogs_Gender", 
  "code-35b2c5c55a5f" : "WUSC_KEEP_II_Demogs_Locations",
  "code-5816d8cc5ae4" : "WUSC_KEEP_II_Aisha_Empirical_Expectations", 
  "code-1056beb8e95a" : "WUSC_KEEP_II_Aisha_Normative_Expectations", 
  "code-680a279def74" : "WUSC_KEEP_II_Aisha_Parenthood", 
  "code-bda79ce52f54" : "WUSC_KEEP_II_Aisha_Reference_Groups", 
  "code-d23abbf2ce3d" : "WUSC_KEEP_II_Aisha_Reference_Groups_Others", 
  "code-572e99d49e15" : "WUSC_KEEP_II_Aisha_Sanctions", 
  "code-3db4d24996f3" : "WUSC_KEEP_II_Amina_Empirical_Expectations", 
  "code-1a3c617cae67" : "WUSC_KEEP_II_Amina_Normative_Expectations", 
  "code-bf29a7b6cb82" : "WUSC_KEEP_II_Amina_Parenthood", 
  "code-6df5ef0a3e09" : "WUSC_KEEP_II_Amina_Reference_Groups", 
  "code-990e9335223e" : "WUSC_KEEP_II_Amina_Reference_Groups_Others", 
  "code-67be51f81647" : "WUSC_KEEP_II_Amina_Sanctions", 
  "code-6c138acf6693" : "WUSC_KEEP_II_Mohamed_Empirical_Expectations", 
  "code-88021e17e7b0" : "WUSC_KEEP_II_Mohamed_Normative_Expectations", 
  "code-918ef3c147af" : "WUSC_KEEP_II_Mohamed_Parenthood", 
  "code-0f21e066ec59" : "WUSC_KEEP_II_Mohamed_Reference_Groups", 
  "code-9125085a480b" : "WUSC_KEEP_II_Mohamed_Reference_Groups_Others", 
  "code-0fe16d2b510a" : "WUSC_KEEP_II_Mohamed_Sanctions", 
  "code-d500a7c07cd7" : "WUSC_KEEP_II_Zamzam_Empirical_Expectations", 
  "code-a191c42b91c2" : "WUSC_KEEP_II_Zamzam_Normative_Expectations", 
  "code-a8c977b7686e" : "WUSC_KEEP_II_Zamzam_Parenthood", 
  "code-59959767b909" : "WUSC_KEEP_II_Zamzam_Reference_Groups", 
  "code-fcc3969d1ff4" : "WUSC_KEEP_II_Zamzam_Reference_Groups_Others", 
  "code-6162b81ea647" : "WUSC_KEEP_II_Zamzam_Sanctions"
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Repackages data to the right scheme")
    
    parser.add_argument("input_data", help="Path to input messages file, containing a list of Coda messages as JSON", nargs=1)
    parser.add_argument("output_folder", help="Path to create new messages to push to Coda", nargs=1)

    args = parser.parse_args()
    input_data = args.input_data[0]
    json_output_folder = args.output_folder[0]

    dataset_to_new_messages = {

    }

    # Load data from JSON file
    with open(input_data, "r") as f:
        data = json.load(f)

    for msg_map in data:
        del msg_map['SequenceNumber']
        msg_map["_moved_from"] = input_data.split('.')[0].split("/")[-1]

        relocate = False
        relocate_target = None

        labels = msg_map['Labels']
        for label in labels:
            if label["CodeID"] == WS_key:
                relocate = True
                continue

            if label["SchemeID"] != "Scheme-fff774bb5099":
                continue

            if label["CodeID"] == "SPECIAL-MANUALLY_UNCODED":
                relocate = False
                break
            
            relocate = True
            relocate_target = code_to_dataset[label["CodeID"]]
            print (relocate_target)
            break
            
        if relocate and relocate_target != None:
            if relocate_target not in dataset_to_new_messages:
                dataset_to_new_messages[relocate_target] = []
            
            msg_map["Labels"] = []
            dataset_to_new_messages[relocate_target].append(msg_map)

            print ("{}: {}".format(relocate_target, len(dataset_to_new_messages[relocate_target])))
    
    print (dataset_to_new_messages)

    for dataset_name in dataset_to_new_messages.keys():
        out_path = os.path.join(json_output_folder, dataset_name + ".json")

        print (out_path)

        if os.path.exists(out_path):
            with open(out_path, "r") as f:
                existing_messages = json.load(f)
        else:
            existing_messages = []
        
        existing_messages.extend(dataset_to_new_messages[dataset_name])
        with open(out_path, "w") as f:
            json.dump(existing_messages, f, indent=2)
