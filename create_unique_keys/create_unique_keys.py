import argparse
import csv
import time
import os

from core_data_modules.traced_data import TracedData, Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO

def create_unique_keys(traced_data_iterable, keys_to_update, group_name):
    """
    Acts on the TracedData Object itself(traced_data_iterable)
    :param traced_data_iterable: Data to update the keys of
    :type traced_data_iterable: iterable of TracedData
    :param key_to_update: Key to search for and update
    :type key_to_update: list
    :param group_name: String create new key from 
    :type group_name: str
    """
    for record in traced_data_iterable:
        data_to_append = {}
        for key in record.keys():
            for key_to_update in keys_to_update:
                if key_to_update in key:
                    new_key = key_to_update + " - " + group_name
                    data_to_append[new_key] = record[key]
                    data_to_append[key] = "NO_DATA (FIELD RENAMED)"
        md =  Metadata(user, Metadata.get_call_location(), time.time())
        record.append_data(data_to_append, md)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Loads the activation surveys and concatenates them")
    parser.add_argument("user", help="Identifier of user launching this program, for use in TracedData Metadata")
    parser.add_argument("messages_input_path", help="Path to folder containing the messages")
    parser.add_argument("surveys_input_path", help="Path to the folder containing the surveys")
    parser.add_argument("demogs_input_path", help="Path to the radio activation survey")
    parser.add_argument("messages_traced_json_output_path", help="Path to updated messages TraceData JSON")
    parser.add_argument("surveys_traced_json_output_path", help="Path to updted survey TraceData JSON")
    parser.add_argument("demogs_traced_json_output_path", help="Path to updted survey TraceData JSON")

 
    args = parser.parse_args()
    user = args.user
    messages_input_path = args.messages_input_path
    surveys_input_path = args.surveys_input_path
    demogs_input_path = args.demogs_input_path
    messages_traced_json_output_path = args.messages_traced_json_output_path
    surveys_traced_json_output_path = args.surveys_traced_json_output_path
    demogs_traced_json_output_path = args.demogs_traced_json_output_path


    # Load messages
    for filename in os.listdir(messages_input_path):
        with open(os.path.join(messages_input_path, filename)) as f:
            messages = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

            # Create a set of all the keys appearing in the data 
            keys = {key for message in messages for key in message.keys()}
            keys = list(keys)
            keys.remove("avf_phone_id")

            # Add group name to each key
            group_name = filename.split("_with_id.json")[0] 
            create_unique_keys(messages, keys, group_name)

        # Output updated td-s    
        message_output_path = os.path.join(messages_traced_json_output_path, "{}_updated_keys.json".format(group_name))
        with open(message_output_path, "w") as f:
             TracedDataJsonIO.export_traced_data_iterable_to_json(messages, f, pretty_print=True)

    # Load surveys
    for filename in os.listdir(surveys_input_path):
        with open(os.path.join(surveys_input_path, filename)) as f:
            surveys = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

            # Create a set of all the keys appearing in the data
            keys = {key for survey in surveys for key in survey.keys()}
            keys = list(keys)
            keys.remove("avf_phone_id")

            # Add group name to each key
            group_name = filename.split("_with_id.json")[0]
            create_unique_keys(surveys, keys, group_name)

        # Output updated td-s    
        message_output_path = os.path.join(surveys_traced_json_output_path, "{}_updated_keys.json".format(group_name))
        with open(message_output_path, "w") as f:
             TracedDataJsonIO.export_traced_data_iterable_to_json(surveys, f, pretty_print=True)


    # Load demogs
    for filename in os.listdir(demogs_input_path):
        with open(os.path.join(demogs_input_path, filename)) as f:
            demogs = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

            # Create a set of all the keys appearing in the data 
            keys = {key for message in demogs for key in message.keys()}
            keys = list(keys)
            keys.remove("avf_phone_id")

            # Add group name to each key
            group_name = filename.split("_with_id.json")[0] 
            create_unique_keys(demogs, keys, group_name)

        # Output updated td-s    
        demogs_output_path = os.path.join(demogs_traced_json_output_path, "{}_updated_keys.json".format(group_name))
        with open(demogs_output_path, "w") as f:
             TracedDataJsonIO.export_traced_data_iterable_to_json(demogs, f, pretty_print=True)

