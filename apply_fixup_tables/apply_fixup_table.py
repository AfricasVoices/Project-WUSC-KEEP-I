import os
import json
import argparse
import time

from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataCSVIO
from core_data_modules.util import SHAUtils


WS_key = "code-WS-adb25603b7af"
WS_Scheme = "Scheme-fff774bb5099"

EMPTY_STRING_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

demog_maps = [
    {"MessageId" : "Coda-Id-Age",       "Coda-Dataset" : "WUSC_KEEP_II_Demogs_Age"},
    {"MessageId" : "Coda-Id-Gender",    "Coda-Dataset" : "WUSC_KEEP_II_Demogs_Gender"},
    {"MessageId" : "Coda-Id-Location",  "Coda-Dataset" : "WUSC_KEEP_II_Demogs_Locations"}
]

message_maps = [
    {"MessageId" : "Coda-Id", "Coda-Dataset" : "WUSC_KEEP_II_Aisha", "FileName" : "Aisha_with_id.json"},
    {"MessageId" : "Coda-Id", "Coda-Dataset" : "WUSC_KEEP_II_Amina", "FileName" : "Amina_with_id.json"},
    {"MessageId" : "Coda-Id", "Coda-Dataset" : "WUSC_KEEP_II_Mohamed", "FileName" : "Mohamed_with_id.json"},
    {"MessageId" : "Coda-Id", "Coda-Dataset" : "WUSC_KEEP_II_Zamzam", "FileName" : "Zamzam_with_id.json"}
]

survey_file_names = [
    "Aisha_survey_with_id.json",
    "Amina_survey_with_id.json",
    "Mohamed_survey_with_id.json",
    "Zamzam_survey_with_id.json"
]

survey_maps = [
    {"MessageId" : "Coda-Id-Empirical_Expectations",    "Coda-Dataset" : "Empirical_Expectations"},
    {"MessageId" : "Coda-Id-Normative_Expectations",    "Coda-Dataset" : "Normative_Expectations"},
    {"MessageId" : "Coda-Id-Parenthood",                "Coda-Dataset" : "Parenthood"},
    {"MessageId" : "Coda-Id-Reference_Groups",          "Coda-Dataset" : "Reference_Groups"},
    {"MessageId" : "Coda-Id-Reference_Groups_Others",   "Coda-Dataset" : "Reference_Groups_Others"},
    {"MessageId" : "Coda-Id-Sanctions",                 "Coda-Dataset" : "Sanctions"}
]

user = "luke"

def remap(id, dataset_in_principle, fixup_table, code_schemes):
    for fix in fixup_table:
        if fix["MessageID"] == id and fix["SourceDataset"] == dataset_in_principle:            
            avf_phone_id = msg["avf_phone_id"]
            destination = fix["DestinationDataset"]

            new_code_id = fix["Remapped_CodeID"] 
            new_code_scheme = fix["Remapped_SchemeID"]

            codes = code_schemes[new_code_scheme]["Codes"]
            match_codes = [c for c in codes if c["CodeID"] == new_code_id]
            assert (len(match_codes) == 1)
            code = match_codes[0]

            new_code_string_value = code["DisplayText"]

            print ("{}, {}, {}, {}, {}, {}, {}".format(avf_phone_id, fix["Text"].replace(",", " "), dataset_in_principle, destination, new_code_scheme, new_code_id, new_code_string_value))



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Prepares the table for repackaging")
    
    parser.add_argument("fixup_table_path", help="Path to mapping table", nargs=1)
    parser.add_argument("messages_in_folder", help="Path to messages folder", nargs=1)
    parser.add_argument("surveys_in_folder", help="Path to surveys folder", nargs=1)
    parser.add_argument("demogs_in_folder", help="Path to demogs folder", nargs=1)

    parser.add_argument("code_schemes_in_folder", help="Path to code_schemes folder", nargs=1)


    args = parser.parse_args()

    fixup_table_path = args.fixup_table_path[0]

    messages_in_folder = args.messages_in_folder[0]
    surveys_in_folder = args.surveys_in_folder[0]
    demogs_in_folder = args.demogs_in_folder[0]

    code_schemes_in_folder = args.code_schemes_in_folder[0]

    print ("{}, {}, {}, {}, {}, {}, {}".format("avf_phone_id", "Text", "Origin dataset", "Destination dataset", "new_code_scheme", "new_code_id", "new value"))

    # print ("Loading coda fixup table")
    fixup_table = json.load(open(fixup_table_path, 'r'))

    # print ("Loading code schemes")
    code_scheme_paths_list = [os.path.join(code_schemes_in_folder, f) for f in os.listdir(code_schemes_in_folder) if os.path.isfile(os.path.join(code_schemes_in_folder, f))]

    code_schemes = {}
    for code_scheme_path in code_scheme_paths_list:
        scheme = json.load(open(code_scheme_path, 'r'))
        code_schemes[scheme["SchemeID"]] = scheme

    # print ("Loading demog data")
    demog_td = TracedDataJsonIO.import_json_to_traced_data_iterable(open(os.path.join(demogs_in_folder, "Demog_survey_with_id.json"), 'r'))

    # print ("Remapping demogs")    
    for msg in demog_td:
        for demog_map in demog_maps:
            id = msg[demog_map["MessageId"]]
            dataset_in_principle = demog_map["Coda-Dataset"]
            remap(id, dataset_in_principle, fixup_table, code_schemes)

    # print ("Remapping messages")    
    for message_map in message_maps:
        # print ("Loading message_map: {}".format(message_map["FileName"]))
        messages_td = TracedDataJsonIO.import_json_to_traced_data_iterable(open(os.path.join(messages_in_folder, message_map["FileName"]), 'r'))

        # print ("Remapping messages")    
        for msg in messages_td:
            # for demog_map in demog_maps:
            id = msg[message_map["MessageId"]]
            dataset_in_principle = message_map["Coda-Dataset"]
            remap(id, dataset_in_principle, fixup_table, code_schemes)

    # print ("Remapping surveys")
    for survey_file_name in survey_file_names:
        characterName = survey_file_name.split('_')[0]
        
        # print ("Loading survey: {}".format(survey_file_name))
        survey_td = TracedDataJsonIO.import_json_to_traced_data_iterable(open(os.path.join(surveys_in_folder, survey_file_name), 'r'))

        for survey_map in survey_maps:
            coda_dataset = "WUSC_KEEP_II_{}_{}".format(characterName, survey_map["Coda-Dataset"])
            # print (coda_dataset)
            
            # print ("Remapping messages")    
            for msg in survey_td:
                # for demog_map in demog_maps:
                id = msg[survey_map["MessageId"]]
                dataset_in_principle = coda_dataset
                remap(id, dataset_in_principle, fixup_table, code_schemes)
