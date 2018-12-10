import argparse
import time
from os import path
import json
from dateutil.parser import isoparse
from datetime import datetime
import pytz as pytz

from core_data_modules.cleaners import CharacterCleaner, Codes
from core_data_modules.cleaners.codes import SomaliaCodes
from core_data_modules.cleaners.location_tools import SomaliaLocations
from core_data_modules.data_models import Origin, Label
from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataCodaIO, TracedDataTheInterfaceIO
from core_data_modules.util import IOUtils


class CleaningUtils(object):
    @staticmethod
    def make_label(scheme, code, origin_id, origin_name="Pipeline Auto-Coder", date_time_utc=None):
        if date_time_utc is None:
            date_time_utc = datetime.now().astimezone(pytz.utc).isoformat()

        origin = Origin(origin_id, origin_name, "External")

        return Label(scheme, code, date_time_utc, origin, checked=False)

# TODO: remove once pull request for below merged with master in CoreDataModules
class TracedDataCoda2IO(object):
    @staticmethod
    def _dataset_lut_from_messages_file(f):
        """
        Creates a lookup table of MessageID -> SchemeID -> Labels from the given Coda 2 messages file.
        :param f: Coda 2 messages file.
        :type f: file-like
        :return: Lookup table.
        :rtype: dict of str -> (dict of str -> list of dict)
        """
        coda_dataset = dict()  # of MessageID -> (dict of SchemeID -> list of Label)

        for msg in json.load(f):
            schemes = dict()  # of SchemeID -> list of Label
            coda_dataset[msg["MessageID"]] = schemes
            msg["Labels"].reverse()
            for label in msg["Labels"]:
                scheme_id = label["SchemeID"]
                if scheme_id not in schemes:
                    schemes[scheme_id] = []
                schemes[scheme_id].append(label)

        return coda_dataset

    @staticmethod
    def _is_coded_as_missing(labels):
        """
        Returns whether all of the given labels are the same and either true missing, skipped, or not logical.
        :param labels: Labels to check
        :type labels: iterable of dict
        :return: Whether or not all of the given code_ids are the same and one of true missing, skipped, or not logical.
        :rtype: bool
        """
        # control_codes = [label.get("ControlCode") for label in labels if label is not None]
        # if len(set(control_codes)) == 1:
        #     control_code = control_codes.pop()
        #     if control_code in {Codes.TRUE_MISSING, Codes.SKIPPED, Codes.NOT_INTERNALLY_CONSISTENT}:
        #         return True
        # return False
        # TODO: Re-implement using control codes
        code_ids = [label["CodeID"] for label in labels if label is not None]
        if len(set(code_ids)) == 1:
            code_id = code_ids.pop()
            return code_id.startswith("code-NA") or code_id.startswith("code-NS")
        return False

    @classmethod
    def import_coda_2_to_traced_data_iterable(cls, user, data, message_id_key, scheme_keys, nr_label, f):
        """
        Codes keys in an iterable of TracedData objects by using the codes from a Coda 2 messages JSON file.

        Data which is has not been checked in the Coda file is coded using the provided nr_label
        (irrespective of whether there was an automatic code there before).
        Data which was previously coded as TRUE_MISSING, SKIPPED, or NOT_LOGICAL by any means is untouched.

        TODO: Data which has been assigned a code under one scheme but none of the others needs to coded as NC not NR
        TODO: Or, do this in Coda so as to remove ambiguity from the perspective of the RAs?

        :param user: Identifier of user running this program.
        :type user: str
        :param data: TracedData objects to be coded using the Coda file.
        :type data: iterable of TracedData
        :param message_id_key: Key in TracedData objects of the message ids.
        :type message_id_key: str
        :param scheme_keys: Dictionary of (key in TracedData objects to assign labels to) ->
                            (ids of the scheme in the Coda messages file to retrieve the labels from)
        :type scheme_keys: dict of str -> str
        :param nr_label: Label to apply to messages which haven't been reviewed yet.
        :type nr_label: core_data_modules.data_models.Label
        :param f: Coda data file to import codes from.
        :type f: file-like
        """
        # Build a lookup table of MessageID -> SchemeID -> Labels
        coda_dataset = cls._dataset_lut_from_messages_file(f)

        # Apply the labels from Coda to each TracedData item in data
        for td in data:
            if message_id_key not in td:
                continue

            for key_of_coded, scheme_id in scheme_keys.items():
                labels = coda_dataset.get(td[message_id_key], dict()).get(scheme_id)
                if labels is not None:
                    for label in labels:
                        # TODO: Check not duplicating previous history?
                        td.append_data(
                            {key_of_coded: label},
                            Metadata(user, Metadata.get_call_location(),
                                     (isoparse(label["DateTimeUTC"]) - datetime(1970, 1, 1,
                                                                                tzinfo=pytz.utc)).total_seconds())
                        )

                    if key_of_coded not in td or not td[key_of_coded]["Checked"] or \
                            td[key_of_coded]["CodeID"] == "SPECIAL-MANUALLY_UNCODED":
                        td.append_data(
                            {key_of_coded: nr_label.to_dict()},
                            Metadata(user, Metadata.get_call_location(), time.time())
                        )
                elif not cls._is_coded_as_missing([td.get(key_of_coded)]):
                    td.append_data(
                        {key_of_coded: nr_label.to_dict()},
                        Metadata(user, Metadata.get_call_location(), time.time())
    )

    @classmethod
    def import_coda_2_to_traced_data_iterable_multi_coded(cls, user, data, message_id_key, scheme_keys, nr_label,
                                                        f):
        """
        Codes keys in an iterable of TracedData objects by using the codes from a Coda 2 messages JSON file.
        Data which is has not been checked in the Coda file is coded using the provided nr_label
        (irrespective of whether there was an automatic code there before).
        Data which was previously coded as TRUE_MISSING, SKIPPED, or NOT_LOGICAL by any means is untouched.
        TODO: Data which has been assigned a code under one scheme but none of the others needs to coded as NC not NR
        TODO: Or, do this in Coda so as to remove ambiguity from the perspective of the RAs?
        :param user: Identifier of user running this program.
        :type user: str
        :param data: TracedData objects to be coded using the Coda file.
        :type data: iterable of TracedData
        :param message_id_key: Key in TracedData objects of the message ids.
        :type message_id_key: str
        :param scheme_keys: Dictionary of (key in TracedData objects to assign labels to) ->
                            (ids of schemes in the Coda messages file to retrieve the labels from)
        :type scheme_keys: dict of str -> (iterable of str)
        :param nr_label: Label to apply to messages which haven't been reviewed yet.
        :type nr_label: core_data_modules.data_models.Label
        :type scheme_keys: dict of str -> list of str
        :param f: Coda data file to import codes from.
        :type f: file-like
        """
        # Build a lookup table of MessageID -> SchemeID -> Labels
        coda_dataset = cls._dataset_lut_from_messages_file(f)

        # Apply the labels from Coda to each TracedData item in data
        for td in data:
            if message_id_key not in td:
                continue

            for coded_key in scheme_keys.keys():
                # Get all the labels assigned to this scheme across all the virtual schemes in Coda,
                # and sort oldest first.
                labels = []
                for scheme_id in scheme_keys[coded_key]:
                    #print(coda_dataset.get(td[message_id_key]))
                    labels.extend(coda_dataset.get(td[message_id_key], dict()).get(scheme_id, []))
                # print("labels: ", labels)
                labels.sort(key=lambda l: isoparse(l["DateTimeUTC"]))
                
                # Get the currently assigned list of codes for this multi-coded scheme
                td_codes = td.get(coded_key, [])
                td_codes_lut = {code["SchemeID"]: code for code in td_codes}

                for label in labels:
                    # Update the relevant label in this traced data's list of labels with the new label,
                    # and append the whole new list to the traced data.
                    td_codes_lut[label["SchemeID"]] = label
                    if len(td_codes_lut) > 1:
                        for key, code in td_codes_lut.items():
                            if code.get("ControlCode") == Codes.NOT_CODED:
                                del td_codes_lut[key]

                    td_codes = list(td_codes_lut.values())
                    td.append_data({coded_key: td_codes},
                                   Metadata(user, Metadata.get_call_location(),
                                            (isoparse(label["DateTimeUTC"]) - datetime(1970, 1, 1,
                                                                                       tzinfo=pytz.utc)).total_seconds()))

                for scheme_id, code in list(td_codes_lut.items()):
                    if code["CodeID"] == "SPECIAL-MANUALLY_UNCODED":
                        del td_codes_lut[scheme_id]
                        td_codes = list(td_codes_lut.values())
                    
                        td.append_data({coded_key: td_codes}, Metadata(user, Metadata.get_call_location(), time.time()))

                checked_codes_count = 0
                coded_as_missing = False
                labels = td.get(coded_key)
                #print(labels)
                if labels is not None:
                    for label in labels:
                        if label["Checked"]:
                            checked_codes_count += 1

                    coded_as_missing = cls._is_coded_as_missing(labels)

                if checked_codes_count == 0 and not coded_as_missing:
                    td.append_data(
                        {coded_key: [nr_label.to_dict()]},
                        Metadata(user, Metadata.get_call_location(), time.time())
                    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merges manually cleaned files back into a traced data file.")
    parser.add_argument("user", help="User launching this program, for use by TracedData Metadata")
    parser.add_argument("json_input_path", metavar="json-input-path",
                        help="Path to JSON input file, which contains a list of TracedData objects")
    parser.add_argument("coded_input_path", metavar="coded-input-path",
                        help="Directory to read manually-coded Coda files from")
    parser.add_argument("json_output_path", metavar="json-output-path",
                        help="Path to a JSON file to write merged results to")
    parser.add_argument("scheme_input_path", metavar="scheme-input-path",
                        help="Directory to read Coda scheme files from")
                        
    
    args = parser.parse_args()
    user = args.user
    json_input_path = args.json_input_path
    coded_input_path = args.coded_input_path
    json_output_path = args.json_output_path
    scheme_input_path = args.scheme_input_path

    class MergePlan:
        def __init__(self, raw_field, coda_name, coded_name, scheme_name):
            self.raw_field = raw_field
            self.coda_name = coda_name
            self.coded_name = coded_name
            self.scheme_name = scheme_name

    merge_plan = [
        MergePlan("Message - Aisha", "WUSC_KEEP_II_Aisha", "Message - Aisha_Coded", "Dadaab Themes"),
        MergePlan("Message - Amina", "WUSC_KEEP_II_Amina", "Message - Amina_Coded", "Dadaab Themes"),
        MergePlan("Message - Mohamed", "WUSC_KEEP_II_Mohamed", "Message - Mohamed_Coded", "Dadaab Themes"),
        MergePlan("Message - Zamzam", "WUSC_KEEP_II_Zamzam", "Message - Zamzam_Coded", "Dadaab Themes"),

        MergePlan("Selected_Gender - Demog_survey", "WUSC_KEEP_II_Demogs_Gender", "Gender - Demog_survey_Coded", "Gender"),
        MergePlan("Selected_Age - Demog_survey", "WUSC_KEEP_II_Demogs_Age", "Age - Demog_survey_Coded", "Age"),
        MergePlan("Selected_Location - Demog_survey", "WUSC_KEEP_II_Demogs_Locations", "Location - Demog_survey_Coded", "Location"),

        MergePlan("Selected_Empirical_Expectations - Aisha_survey", "WUSC_KEEP_II_Aisha_Empirical_Expectations", "Empirical_Expectations - Aisha_survey_Coded", "Empirical Expectations"),
        MergePlan("Selected_Empirical_Expectations - Amina_survey", "WUSC_KEEP_II_Amina_Empirical_Expectations", "Empirical_Expectations - Amina_survey_Coded", "Empirical Expectations"),
        MergePlan("Selected_Empirical_Expectations - Mohamed_survey", "WUSC_KEEP_II_Mohamed_Empirical_Expectations", "Empirical_Expectations - Mohamed_survey_Coded", "Empirical Expectations"),
        MergePlan("Selected_Empirical_Expectations - Zamzam_survey", "WUSC_KEEP_II_Zamzam_Empirical_Expectations", "Empirical_Expectations - Zamzam_survey_Coded", "Empirical Expectations"),

        MergePlan("Selected_Normative_Expectations - Aisha_survey", "WUSC_KEEP_II_Aisha_Normative_Expectations", "Normative_Expectations - Aisha_survey_Coded", "Normative Expectations"),
        MergePlan("Selected_Normative_Expectations - Amina_survey", "WUSC_KEEP_II_Amina_Normative_Expectations", "Normative_Expectations - Amina_survey_Coded", "Normative Expectations"),
        MergePlan("Selected_Normative_Expectations - Mohamed_survey", "WUSC_KEEP_II_Mohamed_Normative_Expectations", "Normative_Expectations - Mohamed_survey_Coded", "Normative Expectations"),
        MergePlan("Selected_Normative_Expectations - Zamzam_survey", "WUSC_KEEP_II_Zamzam_Normative_Expectations", "Normative_Expectations - Zamzam_survey_Coded", "Normative Expectations"),

        MergePlan("Selected_Parenthood - Aisha_survey", "WUSC_KEEP_II_Aisha_Parenthood", "Parenthood - Aisha_survey_Coded", "NoYes"),
        MergePlan("Selected_Parenthood - Amina_survey", "WUSC_KEEP_II_Amina_Parenthood", "Parenthood - Amina_survey_Coded", "NoYes"),
        MergePlan("Selected_Parenthood - Mohamed_survey", "WUSC_KEEP_II_Mohamed_Parenthood", "Parenthood - Mohamed_survey_Coded", "NoYes"),
        MergePlan("Selected_Parenthood - Zamzam_survey", "WUSC_KEEP_II_Zamzam_Parenthood", "Parenthood - Zamzam_survey_Coded", "NoYes"),
        
        MergePlan("Selected_Reference_Groups - Aisha_survey", "WUSC_KEEP_II_Aisha_Reference_Groups", "Reference_Groups - Aisha_survey_Coded", "Reference group and Reference Group Others"),
        MergePlan("Selected_Reference_Groups - Amina_survey", "WUSC_KEEP_II_Amina_Reference_Groups", "Reference_Groups - Amina_survey_Coded", "Reference group and Reference Group Others"),
        MergePlan("Selected_Reference_Groups - Mohamed_survey", "WUSC_KEEP_II_Mohamed_Reference_Groups", "Reference_Groups - Mohamed_survey_Coded", "Reference group and Reference Group Others"),
        MergePlan("Selected_Reference_Groups - Zamzam_survey", "WUSC_KEEP_II_Zamzam_Reference_Groups", "Reference_Groups - Zamzam_survey_Coded", "Reference group and Reference Group Others"),

        MergePlan("Selected_Reference_Groups_Others - Aisha_survey", "WUSC_KEEP_II_Aisha_Reference_Groups_Others", "Reference_Groups_Others - Aisha_survey_Coded", "Reference group and Reference Group Others"),
        MergePlan("Selected_Reference_Groups_Others - Amina_survey", "WUSC_KEEP_II_Amina_Reference_Groups_Others", "Reference_Groups_Others - Amina_survey_Coded", "Reference group and Reference Group Others"),
        MergePlan("Selected_Reference_Groups_Others - Mohamed_survey", "WUSC_KEEP_II_Mohamed_Reference_Groups_Others", "Reference_Groups_Others - Mohamed_survey_Coded", "Reference group and Reference Group Others"),
        MergePlan("Selected_Reference_Groups_Others - Zamzam_survey", "WUSC_KEEP_II_Zamzam_Reference_Groups_Others", "Reference_Groups_Others - Zamzam_survey_Coded", "Reference group and Reference Group Others"),

        MergePlan("Selected_Sanctions - Aisha_survey", "WUSC_KEEP_II_Aisha_Sanctions", "Sanctions - Aisha_survey_Coded", "Approval"),
        MergePlan("Selected_Sanctions - Amina_survey", "WUSC_KEEP_II_Amina_Sanctions", "Sanctions - Amina_survey_Coded", "Approval"),
        MergePlan("Selected_Sanctions - Mohamed_survey", "WUSC_KEEP_II_Mohamed_Sanctions", "Sanctions - Mohamed_survey_Coded", "Approval"),
        MergePlan("Selected_Sanctions - Zamzam_survey", "WUSC_KEEP_II_Zamzam_Sanctions", "Sanctions - Zamzam_survey_Coded", "Approval"),
    ]

    # Load data from JSON file
    with open(json_input_path, "r") as f:
        data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # Merge manually coded survey Coda files into the cleaned dataset
    for plan in merge_plan:
        coda_file_path = path.join(coded_input_path, "{}.json".format(plan.coda_name))

        if not path.exists(coda_file_path):
            print("Warning: No Coda file found for key '{}'".format(plan.coda_name))
            for td in data:
                td.append_data(
                    {plan.coded_name: None},
                    Metadata(user, Metadata.get_call_location(), time.time())
                )
            continue

        scheme_file_path = path.join(scheme_input_path, "{}.json").format(plan.scheme_name)
        with open(scheme_file_path, "r") as f:
            coding_scheme = json.load(f)

        nr_label = CleaningUtils.make_label(
                coding_scheme["SchemeID"], "code-NR-5e3eee23",
                Metadata.get_call_location()
        )

        if "Message" not in plan.raw_field:
            message_id_field = "Coda-Id-{}".format(plan.raw_field.split("Selected_")[1])
        else:
            message_id_field = "Coda-Id{}".format(plan.raw_field.split("Message")[1])

        if "Reference_Groups" in plan.raw_field:
            with open(coda_file_path, "r") as f:
                TracedDataCoda2IO.import_coda_2_to_traced_data_iterable_multi_coded(
                    user, data, message_id_field, {plan.coded_name: [coding_scheme["SchemeID"]]}, nr_label, f)

        else:    
            with open(coda_file_path, "r") as f:
                TracedDataCoda2IO.import_coda_2_to_traced_data_iterable(
                    user, data, message_id_field, {plan.coded_name: coding_scheme["SchemeID"]}, nr_label, f)

    # Write coded data back out to disk
    IOUtils.ensure_dirs_exist_for_file(json_output_path)
    with open(json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(data, f, pretty_print=True)

    