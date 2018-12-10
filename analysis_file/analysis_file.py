import sys
import time
import argparse
import os
import json
import sys

from core_data_modules.cleaners import Codes
from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.io import TracedDataCSVIO, TracedDataJsonIO
from core_data_modules.traced_data.util import FoldTracedData
from analysis_keys import AnalysisKeys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("user")
    parser.add_argument("coding_schemes_path", metavar="coding-schemes-path", help="Directory containing coding schemes")
    parser.add_argument("data_path")
    parser.add_argument("csv_by_message_output_path")
    parser.add_argument("csv_by_individual_output_path")

    args = parser.parse_args()
    user = args.user
    coding_schemes_path = args.coding_schemes_path
    data_path = args.data_path
    csv_by_message_output_path = args.csv_by_message_output_path
    csv_by_individual_output_path = args.csv_by_individual_output_path

    with open(data_path) as f:
        data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    coding_schemes = {}

    for filename in os.listdir(coding_schemes_path):
        with open(os.path.join(coding_schemes_path, filename)) as f:
            # TODO: Switch to use Scheme.from_firebase_map()
            coding_schemes[filename.split(".json")[0]] = json.load(f)
    
    code_ids = dict()
    for scheme in coding_schemes:
        scheme_dict = coding_schemes[scheme]
        codes = scheme_dict["Codes"]
        code_ids[scheme_dict["Name"]] = {}
        for code in codes:
            if "ControlCode" in code:
                code_text = code["ControlCode"]
            else:
                code_text = code["DisplayText"]
            code_ids[scheme_dict["Name"]][code["CodeID"]] = code_text

    class CodingPlan(object):
        def __init__(self, raw_field, coded_field, coda_filename=None, cleaner=None, code_scheme=None, time_field=None,
                    run_id_field=None, icr_filename=None, analysis_file_key=None):
            self.raw_field = raw_field
            self.coded_field = coded_field
            self.coda_filename = coda_filename
            self.icr_filename = icr_filename
            self.cleaner = cleaner
            self.code_scheme = code_scheme
            self.time_field = time_field
            self.run_id_field = run_id_field
            self.analysis_file_key = analysis_file_key

    SURVEY_CODING_PLANS = [
    CodingPlan(raw_field="Selected_Gender - Demog_survey",
                coded_field="Gender - Demog_survey_Coded",
                analysis_file_key="gender",
                code_scheme=coding_schemes["Gender"]),

    CodingPlan(raw_field="Selected_Age - Demog_survey",
                coded_field="Age - Demog_survey_Coded",
                coda_filename="age",
                analysis_file_key="age",
                code_scheme=coding_schemes["Age"]),

    CodingPlan(raw_field="Selected_Location - Demog_survey",
                coded_field="Location - Demog_survey_Coded",
                analysis_file_key="location",
                code_scheme=coding_schemes["Location"]),

    CodingPlan(raw_field="Selected_Empirical_Expectations - Amina_survey",
                coded_field="Empirical_Expectations - Amina_survey_Coded",
                analysis_file_key="w1_emp_expect_dadaab",
                code_scheme=coding_schemes["Empirical Expectations"]),

    CodingPlan(raw_field="Selected_Empirical_Expectations - Aisha_survey",
                coded_field="Empirical_Expectations - Aisha_survey_Coded",
                analysis_file_key="w2_emp_expect_dadaab",
                code_scheme=coding_schemes["Empirical Expectations"]),
    
    CodingPlan(raw_field="Selected_Empirical_Expectations - Mohamed_survey",
                coded_field="Empirical_Expectations - Mohamed_survey_Coded",
                analysis_file_key="w3_emp_expect_dadaab",
                code_scheme=coding_schemes["Empirical Expectations"]),

    CodingPlan(raw_field="Selected_Empirical_Expectations - Zamzam_survey",
                coded_field="Empirical_Expectations - Zamzam_survey_Coded",
                analysis_file_key="w4_emp_expect_dadaab",
                code_scheme=coding_schemes["Empirical Expectations"]),

    CodingPlan(raw_field="Selected_Normative_Expectations - Amina_survey",
                coded_field="Normative_Expectations - Amina_survey_Coded",
                analysis_file_key="w1_norma_expect_dadaab",
                code_scheme=coding_schemes["Normative Expectations"]),

    CodingPlan(raw_field="Selected_Normative_Expectations - Aisha_survey",
                coded_field="Normative_Expectations - Aisha_survey_Coded",
                analysis_file_key="w2_norma_expect_dadaab",
                code_scheme=coding_schemes["Normative Expectations"]),
    
    CodingPlan(raw_field="Selected_Normative_Expectations - Mohamed_survey",
                coded_field="Normative_Expectations - Mohamed_survey_Coded",
                analysis_file_key="w3_norma_expect_dadaab",
                code_scheme=coding_schemes["Normative Expectations"]),
    
    CodingPlan(raw_field="Selected_Normative_Expectations - Zamzam_survey",
                coded_field="Normative_Expectations - Zamzam_survey_Coded",
                analysis_file_key="w4_norma_expect_dadaab",
                code_scheme=coding_schemes["Normative Expectations"]),

    CodingPlan(raw_field="Selected_Parenthood - Amina_survey",
                coded_field="Parenthood - Amina_survey_Coded",
                analysis_file_key="w1_parenthood_dadaab",
                code_scheme=coding_schemes["NoYes"]),

    CodingPlan(raw_field="Selected_Parenthood - Aisha_survey",
                coded_field="Parenthood - Aisha_survey_Coded",
                analysis_file_key="w2_parenthood_dadaab",
                code_scheme=coding_schemes["NoYes"]),

    CodingPlan(raw_field="Selected_Parenthood - Mohamed_survey",
                coded_field="Parenthood - Mohamed_survey_Coded",
                analysis_file_key="w3_parenthood_dadaab",
                code_scheme=coding_schemes["NoYes"]),

    CodingPlan(raw_field="Selected_Parenthood - Zamzam_survey",
                coded_field="Parenthood - Zamzam_survey_Coded",
                analysis_file_key="w4_parenthood_dadaab",
                code_scheme=coding_schemes["NoYes"]),

    CodingPlan(raw_field="Selected_Sanctions - Amina_survey",
                coded_field="Sanctions - Amina_survey_Coded",
                analysis_file_key="w1_sanctions_dadaab",
                code_scheme=coding_schemes["Approval"]),

    CodingPlan(raw_field="Selected_Sanctions - Aisha_survey",
                coded_field="Sanctions - Aisha_survey_Coded",
                analysis_file_key="w2_sanctions_dadaab",
                code_scheme=coding_schemes["Approval"]),

    CodingPlan(raw_field="Selected_Sanctions - Mohamed_survey",
                coded_field="Sanctions - Mohamed_survey_Coded",
                analysis_file_key="w3_sanctions_dadaab",
                code_scheme=coding_schemes["Approval"]),

    CodingPlan(raw_field="Selected_Sanctions - Zamzam_survey",
                coded_field="Sanctions - Zamzam_survey_Coded",
                analysis_file_key="w4_sanctions_dadaab",
                code_scheme=coding_schemes["Approval"])
    ]

    MATRIX_CODING_PLANS = [

    CodingPlan(raw_field="Selected_Reference_Groups - Amina_survey",
                coded_field="Reference_Groups - Amina_survey_Coded",
                analysis_file_key="w1_ref_groups_dadaab_",
                code_scheme=coding_schemes["Reference group and Reference Group Others"]),

    CodingPlan(raw_field="Selected_Reference_Groups - Aisha_survey",
                coded_field="Reference_Groups - Aisha_survey_Coded",
                analysis_file_key="w2_ref_groups_dadaab_",
                code_scheme=coding_schemes["Reference group and Reference Group Others"]),

    CodingPlan(raw_field="Selected_Reference_Groups - Mohamed_survey",
                coded_field="Reference_Groups - Mohamed_survey_Coded",
                analysis_file_key="w3_ref_groups_dadaab_",
                code_scheme=coding_schemes["Reference group and Reference Group Others"]),

    CodingPlan(raw_field="Selected_Reference_Groups - Zamzam_survey",
                coded_field="Reference_Groups - Zamzam_survey_Coded",
                analysis_file_key="w4_ref_groups_dadaab_",
                code_scheme=coding_schemes["Reference group and Reference Group Others"]),

    CodingPlan(raw_field="Selected_Reference_Groups_Others - Amina_survey",
                coded_field="Reference_Groups_Others - Amina_survey_Coded",
                analysis_file_key="w1_ref_groups_dadaab_",
                code_scheme=coding_schemes["Reference group and Reference Group Others"]),

    CodingPlan(raw_field="Selected_Reference_Groups_Others - Aisha_survey",
                coded_field="Reference_Groups_Others - Aisha_survey_Coded",
                analysis_file_key="w2_ref_groups_dadaab_",
                code_scheme=coding_schemes["Reference group and Reference Group Others"]),

    CodingPlan(raw_field="Selected_Reference_Groups_Others - Mohamed_survey",
                coded_field="Reference_Groups_Others - Mohamed_survey_Coded",
                analysis_file_key="w3_ref_groups_dadaab_",
                code_scheme=coding_schemes["Reference group and Reference Group Others"]),

    CodingPlan(raw_field="Selected_Reference_Groups_Others - Zamzam_survey",
                coded_field="Reference_Groups_Others - Zamzam_survey_Coded",
                analysis_file_key="w4_ref_groups_dadaab_",
                code_scheme=coding_schemes["Reference group and Reference Group Others"])
    ]
    
    # Serializer is currently overflowing
    # TODO: Investigate/address the cause of this.
    sys.setrecursionlimit(10000)

    # Set the list of raw/coded keys which
    survey_keys = []
    for plan in SURVEY_CODING_PLANS:
        if plan.analysis_file_key not in survey_keys:
            survey_keys.append(plan.analysis_file_key)
        if plan.raw_field not in survey_keys:
            survey_keys.append(plan.raw_field)

    survey_keys.sort()

    for td in data:
        for key in td:
            if "Group - " in key:
                td.append_data({"Group": td[key]}, Metadata(user, Metadata.get_call_location(), time.time()))

    print("Creating survey analysis keys/coded values")
    for td in data:
        for plan in SURVEY_CODING_PLANS:
            if plan.coded_field in td:
                td.append_data(
                    {plan.analysis_file_key: code_ids[plan.code_scheme["Name"]][td[plan.coded_field]["CodeID"]]},
                    Metadata(user, Metadata.get_call_location(), time.time())
                    )
            else:
                td.append_data({plan.analysis_file_key: Codes.TRUE_MISSING},
                    Metadata(user, Metadata.get_call_location(), time.time())
                    )
                td.append_data({plan.coded_field: Codes.TRUE_MISSING},
                    Metadata(user, Metadata.get_call_location(), time.time())
              )     
            
            # DEBUG: above returns correct keys with corresponding codes eg. "w3_sanctions_dadaab disapprove"
            # print(plan.analysis_file_key, td[plan.analysis_file_key])
               
    column_keys = {
    "Message - Aisha",
    "Message - Aisha_Coded",
    "Message - Amina",
    "Message - Amina_Coded",
    "Message - Mohamed",
    "Message - Mohamed_Coded",
    "Message - Zamzam",
    "Message - Zamzam_Coded"
    }

    coded_column_keys = ["Message - Aisha_Coded", "Message - Amina_Coded", "Message - Mohamed_Coded", "Message - Zamzam_Coded"]

    # Drop data without a key Group  TODO: Understand why some data doesn't have a group
    # print(f"Before dropping groups: {len(data)}")
    # data = [td for td in data if "Group" in td]
    # print(f"After dropping groups: {len(data)}")

    # TODO: Remove this temporary group workaround.
    for td in data:
        if "Group" not in td:
            import secrets
            td.append_data({"Group": secrets.token_hex(8)}, Metadata(user, Metadata.get_call_location(), time.time()))

    data = [td for td in data if td.get("Message - Aisha") != "Kazi"]
    print(f"After filtering kazi: {len(data)}")

    print("Creating message column analysis keys/coded values")
    for td in data:
        for key in coded_column_keys:
            if key in td:
                td.append_data({key: code_ids["Dadaab Themes"][td[key]["CodeID"]]}, 
                Metadata(user, Metadata.get_call_location(), time.time()))  

    # TODO: For each td in data, if Message - x is in that td object, assert Message - x_Coded is too, and vice versa

    # Translate keys to final values for analysis
    matrix_keys = []

    print("Creating matrix analysis keys/coded values")
    for plan in MATRIX_CODING_PLANS:
        show_matrix_keys = set()
        for code in code_ids[plan.code_scheme["Name"]]:
            show_matrix_keys.add(f"{plan.analysis_file_key}{code_ids[plan.code_scheme['Name']][code]}")

        AnalysisKeys.set_matrix_keys(
            user, data, show_matrix_keys, plan, code_ids, plan.coded_field, plan.analysis_file_key)

        matrix_keys.extend(show_matrix_keys)

    matrix_keys.sort()

    equal_keys = ["avf_phone_id", "Group"]
    equal_keys.extend(survey_keys)

    print("Folding")
    folded = FoldTracedData.fold_iterable_of_traced_data(
    user, data, lambda td: (td["avf_phone_id"], td["Group"]), equal_keys=equal_keys, column_keys=column_keys, matrix_keys=matrix_keys
    )

    print("Post fold fix-up")

    # Determine which column keys were set by FoldTracedData.fold_iterable_of_traced_data
    folded_column_keys = set()
    for key in column_keys:
        for td in folded:
            i = 1
            while "{} {}".format(key, i) in td:
                folded_column_keys.add("{} {}".format(key, i))
                i += 1

    # For column keys set on one td but not others, set the others to NA
    for td in folded:
        d = dict()
        for key in folded_column_keys:
            if key not in td:
                d[key] = Codes.TRUE_MISSING
        td.append_data(d, Metadata(user, Metadata.get_call_location(), time.time()))

    # Export to CSV
    export_keys = ["avf_phone_id", "Group"]
    export_keys.extend(list(folded_column_keys))
    export_keys.extend(survey_keys)
    export_keys.extend(matrix_keys)
    export_keys.sort()

    print("Writing 1/2")
    with open(csv_by_individual_output_path, "w") as f:
        TracedDataCSVIO.export_traced_data_iterable_to_csv(folded, f, headers=export_keys)

    print("Writing 2/2")
    # Hack an unused output field to write traced data to (for debug)
    # FIXME
    with open(csv_by_message_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(data, f, pretty_print=True)
        # TracedDataCSVIO.export_traced_data_iterable_to_csv(data, f, headers=export_keys)

