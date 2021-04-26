# json_str = "{

# }"


# """ { section abc }, {section efg }, { section hij """
# """ 
# This is 
# {the text 
#     [
#         under test 
#     ]
# }

# {the text 
#     [
#         under test 
#     ]
# }

# {the text 
#     [
#         under test 
#     ]
# }

# """

# # Equivalence partitioning: Test Coverage: input_files
# # green: valid inputs: work reliably

# # orange: invalid inputs: fail gracefully
# invalid_a = """ [{asbc(efg)] """  # "[{asbc", "efg)"] 
# invalid_b = "123[]#0)"   # 123[]#0)
# invalid_c = ""
# # red: overwhelming inputs: recover/reset



# def parse_json_file_content(input_file_path):
#     # read text from file
#     with open(input_file_path, 'r') as json_file:
#         text = json_file.read()

#     # parse by section
#     # assert if missing delimiter
#     delimiters = [('{', '}'), ('[', ']'), ('(', ')')]
#     for tup_delim_pair in delimiters:
#         for section in text.split(tup_delim_pair[0]):
#             assert len(text.split(tup_delim_pair[0])) > 1, "no starting delim: {}".format(tup_delim_pair[0])
#             assert section, "empty section: invalid format"
#             err_msg = "missing closing delimiter: {}".format(tup_delim_pair[-1])
#             assert tup_delim_pair[-1] in section, err_msg




# def main():
#     parse_json_file_content('./new_json_file.txt')

