import argparse
import time
import os

from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataCSVIO
from core_data_modules.util import SHAUtils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Applies ID to a collection of survey responses")
    parser.add_argument("user", help="User launching this program", nargs=1)
    parser.add_argument("input", help="Path to input file, containing a list of TracedData objects as JSON", nargs=1)
    parser.add_argument("json_output", metavar="json-output",
                        help="Path to write results of cleaning to, as a serialised TracedData JSON file", nargs=1)

    args = parser.parse_args()
    user = args.user[0]
    input_path = args.input[0]
    json_output_path = args.json_output[0]

    # Load data from JSON file
    with open(input_path, "r") as f:
        data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    for td in data:
        selected_empirical_expectations = td["EMPIRICAL EXPECTATIONS_R"]
        selected_nomrative_expectations = td["NORMATIVE EXPECTATIONS_R"]
        selected_parenthood = td["PARENTHOOD_R"]
        selected_reference_groups = td["REFERENCE GROUPS_R"]

        if "SANCTION_R" in td.keys():
            selected_sanctions = td["SANCTION_R"]
        else:
            selected_sanctions = td["SANCTIONS_R"]

        td.append_data(
            {
                "Selected_Empirical_Expectations" : selected_empirical_expectations,
                "Selected_Normative_Expectations" : selected_nomrative_expectations,
                "Selected_Parenthood" : selected_parenthood,
                "Selected_Sanctions" : selected_sanctions,
                "Selected_Reference_Groups" : selected_reference_groups,

                "Coda-Id-Empirical_Expectations" : SHAUtils.sha_string(selected_empirical_expectations),
                "Coda-Id-Normative_Expectations" : SHAUtils.sha_string(selected_nomrative_expectations),
                "Coda-Id-Parenthood" : SHAUtils.sha_string(selected_parenthood),
                "Coda-Id-Sanctions" : SHAUtils.sha_string(selected_sanctions),
                "Coda-Id-Reference_Groups" : SHAUtils.sha_string(selected_reference_groups)

                },
            Metadata(user, Metadata.get_call_location(), time.time()))

    # Write json output
    if os.path.dirname(json_output_path) is not "" and not os.path.exists(os.path.dirname(json_output_path)):
        os.makedirs(os.path.dirname(json_output_path))
    with open(json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(data, f, pretty_print=True)
