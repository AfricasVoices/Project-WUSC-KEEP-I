import argparse
import os
import json
import jsonpickle

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("coded_input_path", metavar="coded-input-path")
    parser.add_argument("coded_filtered_output_path", metavar="coded-filtered-output-path")

    args = parser.parse_args()
    coded_input_path = args.coded_input_path
    coded_filtered_output_path = args.coded_filtered_output_path

    for filename in os.listdir(coded_input_path):
        output_path = os.path.join(coded_filtered_output_path, filename)
        with open(os.path.join(coded_input_path, filename), "r") as f, open(output_path, "w") as outf:
            coded_file = json.load(f)

            coded_file = [message for message in coded_file if "_moved_from" not in message.keys()]

            jsonpickle.set_encoder_options("json", sort_keys=True)
            outf.write(jsonpickle.dumps(coded_file))
            outf.write("\n")