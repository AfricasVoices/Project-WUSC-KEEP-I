import time
import argparse
import os

from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataCSVIO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merges data from show inboxes and survery responses")
    parser.add_argument("user", help="User launching this program, for audit logging", nargs=1)
    parser.add_argument("input_messages", help="Path to input messages file, containing a list of TracedData objects as JSON", nargs=1)
    parser.add_argument("input_adverts", help="Path to input adverts file, containing a list of TracedData objects as JSON", nargs=1)
    parser.add_argument("json_output", metavar="json-output",
                        help="Path to write results of merging to, as a serialised TracedData JSON file", nargs=1)

    args = parser.parse_args()
    user = args.user[0]
    input_path_messages = args.input_messages[0]
    input_path_adverts = args.input_adverts[0]
    json_output_path = args.json_output[0]

    # Load data from JSON file
    with open(input_path_messages, "r") as f:
        messages_data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # Load data from JSON file
    with open(input_path_adverts, "r") as f:
        adverts_data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # Map "QUESTION_R" => "Message"
    for td in adverts_data:
        assert "QUESTION_R" in td.keys()
        td.append_data(
            { "Message" : td["QUESTION_R"]}, 
            Metadata(user, Metadata.get_call_location(), time.time()))

    merged_data = list(messages_data)
    merged_data.extend(adverts_data)

    # Write json output
    if os.path.dirname(json_output_path) is not "" and not os.path.exists(os.path.dirname(json_output_path)):
        os.makedirs(os.path.dirname(json_output_path))
    with open(json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(merged_data, f, pretty_print=True)