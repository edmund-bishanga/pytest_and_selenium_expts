#!/usr/bin/python
""" IDSR Project: SW: SysTest: Re-usable|Shared Utils. """

# pylint: disable=missing-function-docstring  # descriptive function names OK

import copy
import json
import logging
import os

# Config: Logging
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
LOGFILE = os.path.join(RESULTS_DIR, "utils.log")
log_fmt = "%(asctime)s: %(levelname)s: %(message)s"
date_fmt = "%a/%d.%b.%Y %H:%M:%S"
logging.basicConfig(format=log_fmt, datefmt=date_fmt, level=logging.DEBUG)
log = logging.getLogger("utils")

log_file_h = logging.FileHandler(LOGFILE, encoding="utf-8", mode="w")
log_file_h.setLevel(logging.DEBUG)
log_file_h.setFormatter(logging.Formatter(fmt=log_fmt, datefmt=date_fmt))
log.addHandler(log_file_h)
log.propagate = False

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def read_from_json_file(json_filename):
    json_file = os.path.join(DATA_DIR, json_filename)
    with open(json_file, "r", encoding="utf-8") as jsfile:
        json_obj = json.load(jsfile)
    return json_obj

def flatten_keyvals_update_inv(nested_dict):
    """ Takes in a nested dict, flattens it, outputs a flat dict. """
    flat_dict = {}
    for key, inner_dict in nested_dict.items():
        for inner_key, inner_vals in inner_dict.items():
            non_alphanums = ";'#;:<>[]"
            if isinstance(inner_vals, dict):
                for key, vals in inner_vals.items():
                    if isinstance(vals, str):  # singleton: str, int, float
                        new_key = f"{key}_{vals}"
                        flat_dict.update({new_key: vals})
                    else:
                        for val in vals:
                            nval = str(val)
                            if any(char in str(val) for char in non_alphanums):
                                nval = "nonAlphaNumChars"
                            nval = "empty" if not nval else nval
                            new_key = f"{key}_{nval}"
                            flat_dict.update({new_key: val})
            elif isinstance(inner_vals, str):  # singleton: str, int, float
                log.debug("%s: treated as a singleton", inner_vals)
                new_key = f"{key}_{inner_key}"
                flat_dict.update({new_key: inner_vals})
            elif isinstance(inner_vals, list):
                log.debug("%s: treated as a list", inner_vals)
                for val in inner_vals:
                    nval = str(val)
                    if any(char in str(val) for char in non_alphanums):
                        nval = "nonAlphaNumChars"
                    nval = "empty" if not nval else nval
                    new_key = f"{key}_{nval}"
                    flat_dict.update({new_key: val})
            else:
                pass
    log.debug("Flat dict: \n%s", flat_dict)
    return flat_dict

def flatten_keyvals_new_inv(nested_dict):
    """ Takes in a nested dict, flattens it, outputs a flat dict. """
    flat_dict = {}
    for key, inner_dict in nested_dict.items():
        for inner_key, inner_vals in inner_dict.items():
            non_alphanums = ";'#;:<>[]"
            if isinstance(inner_vals, dict):
                for key, vals in inner_vals.items():
                    if isinstance(vals, (str, int)):  # singleton: str, num
                        new_key = f"{key}_{vals}"
                        flat_dict.update({new_key: vals})
                    else:
                        for val in vals:
                            nval = str(val)
                            if any(char in str(val) for char in non_alphanums):
                                nval = "nonAlphaNumChars"
                            nval = "empty" if not nval else nval
                            new_key = f"{key}_{nval}"
                            flat_dict.update({new_key: val})
            elif isinstance(inner_vals, str):  # singleton: str, int, float
                log.debug("%s: treated as a singleton", inner_vals)
                new_key = f"{key}_{inner_key}"
                flat_dict.update({new_key: inner_vals})
            elif isinstance(inner_vals, list):
                log.debug("%s: treated as a list", inner_vals)
                for val in inner_vals:
                    nval = str(val)
                    if any(char in str(val) for char in non_alphanums):
                        nval = "nonAlphaNumChars"
                    nval = "empty" if not nval else nval
                    new_key = f"{key}_{nval}"
                    flat_dict.update({new_key: val})
            else:
                pass
    log.debug("Flat dict: \n%s", flat_dict)
    return flat_dict

def expand_single_listed_dict(klisted_dict, key, delim="_", prefix=""):
    list_of_kdicts = []
    if delim not in key:
        klist = klisted_dict.get(key)
        log.debug("klist: %s", klist)
        if isinstance(klist, list) and not isinstance(klist, str):
            for scenario_val in klist:
                log.debug("adding scenario: %s", scenario_val)
                kdict = klisted_dict.copy()
                kdict[key] = scenario_val
                list_of_kdicts.append(kdict)
    else:
        nested_keys = key.strip().split(delim)
        assert len(nested_keys) == 2, "nested_keys: only 2 supported"
        klist = klisted_dict[nested_keys[0]][nested_keys[-1]]
        if isinstance(klist, list) and not isinstance(klist, str):
            for scenario_val in klist:
                log.debug("adding scenario: %s", scenario_val)
                kdict = copy.deepcopy(klisted_dict)
                kdict[nested_keys[0]][nested_keys[-1]] = scenario_val
                list_of_kdicts.append(kdict)
    expanded_collection = {}
    for count, item in enumerate(list_of_kdicts, start=1):
        prefixstr = key if not prefix else prefix
        expanded_collection.update({f"{prefixstr}_{count}": item})
    return expanded_collection

def find_listed_keys(ldict):
    listed_keys = []
    for key, val in ldict.items():
        if isinstance(val, list) and not isinstance(val, str):
            listed_keys.append(key)
        elif isinstance(val, dict):
            for inner_key, i_val in val.items():
                if isinstance(i_val, list) and not isinstance(i_val, str):
                    listed_keys.append(f"{key}_{inner_key}")
    return listed_keys

def expand_klisted_dicts(scenarios_dict):
    new_scenarios_dict = copy.deepcopy(scenarios_dict)
    for key in scenarios_dict:
        scenario = scenarios_dict[key]
        listed_keys = find_listed_keys(scenario)
        for lkey in listed_keys:
            exp_collection = expand_single_listed_dict(scenario, lkey, prefix=key)
            if exp_collection:
                new_scenarios_dict.pop(key)
                new_scenarios_dict.update(exp_collection)
    return new_scenarios_dict
