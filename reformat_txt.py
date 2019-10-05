import sys

from util.web_viewer_formatter import reformat_text

if __name__ == "__main__":
    input_file_name = sys.argv[1] if len(sys.argv) >= 2 else "input.txt"
    output_file_name = sys.argv[2] if len(sys.argv) >= 3 else "output.txt"
    reformat_text(input_file_name, output_file_name)
