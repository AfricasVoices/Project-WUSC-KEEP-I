import os
import json
import argparse

WS_key = "code-WS-adb25603b7af"
WS_Scheme = "Scheme-fff774bb5099"

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
    parser = argparse.ArgumentParser(description="Prepares the table for repackaging")
    
    parser.add_argument("input_data_folder", help="Path to input messages file, containing a list of Coda messages as JSON", nargs=1)
    parser.add_argument("output_path", help="Path to create the mapping table", nargs=1)

    args = parser.parse_args()
    input_data_folder = args.input_data_folder[0]
    json_output_path = args.output_path[0]

    dataset_names = [f for f in os.listdir(input_data_folder) if os.path.isfile(os.path.join(input_data_folder, f))]

    remappings = []

    datasets_messages = {}
    for dataset_name in dataset_names:
        dataset_path = os.path.join(input_data_folder, dataset_name)
        src_dataset = dataset_name.split('.')[0]

        messages = json.load(open(dataset_path, 'r'))
        datasets_messages[src_dataset] = messages


    for dataset_name in dataset_names:
        dataset_path = os.path.join(input_data_folder, dataset_name)
        src_dataset = dataset_name.split('.')[0]

        messages = datasets_messages[src_dataset]
        for message in messages:
            msg_id = message["MessageID"]
            msg_text = message["Text"]
            for label in message["Labels"]:
                if label["SchemeID"] == WS_Scheme:
                    if label["CodeID"] == 'SPECIAL-MANUALLY_UNCODED':
                        break
                    renamp_target = code_to_dataset[label["CodeID"]]

                    # Now look up what it got remapped to
                    remapped_in_dataset_messages = datasets_messages[renamp_target]
                    messages = [m for m in remapped_in_dataset_messages if m["MessageID"] == msg_id]
                    
                    # print (message)
                    # print (len(messages))
                    assert (len(messages) == 1)
                    new_message = messages[0]
                    assert (new_message["Text"] == msg_text)
                    new_label_code_id = None
                    new_label_scheme_id = None

                    for new_label in new_message["Labels"]:
                        if new_label["SchemeID"] == WS_Scheme:
                            continue
                        if new_label["CodeID"] == 'SPECIAL-MANUALLY_UNCODED':
                            continue
                        
                        new_label_code_id = new_label["CodeID"]
                        new_label_scheme_id = new_label["SchemeID"]
                        break

                    remappings.append(
                        {
                            "MessageID" : msg_id,
                            "Text" : msg_text, # Non canonical, used for debugging
                            "SourceDataset" : src_dataset,
                            "DestinationDataset" : renamp_target,
                            "Remapped_CodeID": new_label_code_id,
                            "Remapped_SchemeID": new_label_scheme_id,
                        }
                    )
                    break

    print ("Writing {} remappings".format(len(remappings)))
    
    # Write json output
    if os.path.dirname(json_output_path) is not "" and not os.path.exists(os.path.dirname(json_output_path)):
        os.makedirs(os.path.dirname(json_output_path))
    with open(json_output_path, "w") as f:
        json.dump(remappings, f, indent=2)

    
