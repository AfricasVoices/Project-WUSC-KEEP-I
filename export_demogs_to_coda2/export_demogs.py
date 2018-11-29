import argparse
import time
import os
import json
from dateutil.parser import isoparse
import pytz as pytz

from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataCSVIO
from core_data_modules.util import SHAUtils

# Temp until this is in core_data_modules
class Message(object):
    message_id = None
    text = None
    creation_date_time_utc = None
    labels = []
    
    def to_dict(self):
        return {
            "MessageID": self.message_id,
            "Text": self.text,
            "CreationDateTimeUTC": self.creation_date_time_utc,
            "Labels": self.labels
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exports a list of surveys to Coda for labelling")
    parser.add_argument("user", help="User launching this program", nargs=1)
    parser.add_argument("input", help="Path to input file, containing a list of TracedData objects as JSON", nargs=1)
    parser.add_argument("variable", help="Name of the variable to export", nargs=1)    
    parser.add_argument("json_output", metavar="json-output",
                        help="Path to write results to for loading into Coda", nargs=1)

    args = parser.parse_args()
    user = args.user[0]
    input_path = args.input[0]
    variable = args.variable[0]
    json_output_path = args.json_output[0]

    # Load data from JSON file
    with open(input_path, "r") as f:
        data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    ids_already_exported = set()
    messages = []

    for td in data:
        var_name = variable
        id_name = variable.replace('Selected_', 'Coda-Id-')

        id = td[id_name]
        if id in ids_already_exported:
            continue

        message_text = td[var_name]
        if message_text == "":
            continue

        if "Date" in td.keys():
            date = td["Date"]
        elif "start_date" in td.keys():
            date = td["start_date"]
        else:
            print ("No date found in td")
            print (json.dump(td))
            assert False


        message = Message()
        message.message_id = id
        message.text = message_text
        message.creation_date_time_utc = isoparse(date).astimezone(pytz.utc).isoformat()
        message.labels = []
        
        ids_already_exported.add(id)
        messages.append(message)

    # Write json output
    if os.path.dirname(json_output_path) is not "" and not os.path.exists(os.path.dirname(json_output_path)):
        os.makedirs(os.path.dirname(json_output_path))
    with open(json_output_path, "w") as f:
        json.dump([m.to_dict() for m in messages], f, sort_keys=True, indent=2, separators=(", ", ": "))
