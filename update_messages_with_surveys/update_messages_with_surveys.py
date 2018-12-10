import argparse
import os

from core_data_modules.traced_data import TracedData
from core_data_modules.traced_data.io import TracedDataJsonIO
from core_data_modules.util import IOUtils

class CombineRawDatasets(object):
    @staticmethod
    def combine_raw_datasets(user, messages_datasets, surveys_datasets):
        data = []

        for messages_dataset in messages_datasets:
            data.extend(messages_dataset)

        for surveys_dataset in surveys_datasets:
            TracedData.update_iterable(user, "avf_phone_id", data, surveys_dataset, "survey_responses")
            
        return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Joins radio show answers with survey answers on respondents' "
                                                 "phone ids.")
    parser.add_argument("user", help="User launching this program")
    parser.add_argument("messages_input_path", metavar="messages-input-path",
                        help="Path to the input messages messages folder, containing files of list of serialized TracedData objects")
    parser.add_argument("survey_input_path", metavar="survey-input-path",
                        help="Path to the cleaned survey folder file, containing files of list of serialized TracedData objects")
    parser.add_argument("demog_input_path", metavar="demog-input-path",
                        help="Path to the cleaned survey JSON file, containing a list of serialized TracedData objects")
    parser.add_argument("json_output_path", metavar="json-output-path",
                        help="Path to a JSON file to write processed messages to")

    args = parser.parse_args()
    user = args.user
    messages_input_path = args.messages_input_path
    survey_input_path = args.survey_input_path
    demog_input_path = args.demog_input_path
    json_output_path = args.json_output_path

    # Load messages
    messages_datasets = []
    for filename in os.listdir(messages_input_path):
        with open(os.path.join(messages_input_path, filename)) as f:
            messages_datasets.append(TracedDataJsonIO.import_json_to_traced_data_iterable(f))

    # Load followup surveys
    survey_datasets = []
    for filename in os.listdir(survey_input_path):
        with open(os.path.join(survey_input_path, filename)) as f:
            messages_datasets.append(TracedDataJsonIO.import_json_to_traced_data_iterable(f))

    # Load demogs
    print("Loading Demographics...")
    with open(demog_input_path, "r") as f:
        demographics = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # Add survey data to the messages
    print("Combining Datasets...")
    data = CombineRawDatasets.combine_raw_datasets(user, messages_datasets, survey_datasets)
    data = CombineRawDatasets.combine_raw_datasets(user, [data], [demographics])

    # Write json output
    IOUtils.ensure_dirs_exist_for_file(json_output_path)
    with open(json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(data, f, pretty_print=True)