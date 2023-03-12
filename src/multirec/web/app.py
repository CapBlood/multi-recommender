from multirec.web.main_page import main_page
import sys


if __name__ == '__main__':
    input_csv = sys.argv[1]

    if len(sys.argv) == 3:
        mapping = sys.argv[2]
        dict_mapping = dict()
        for m in mapping.split(','):
            original_name, map_name = m.split(":")
            dict_mapping[original_name] = map_name

        main_page(input_csv, dict_mapping)
    else:
        main_page(input_csv)
