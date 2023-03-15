import sys

from multirec.web.main_page import main_page


if __name__ == '__main__':
    input_csv = sys.argv[1]
    main_page(input_csv)
