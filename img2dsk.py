
import sys, os, struct

SINGLE_SIDED_DSK_SIZE = 360*1024
DOUBLE_SIDED_DSK_SIZE = SINGLE_SIDED_DSK_SIZE * 2

"""
 IMG and DSK differ only by IMG files having one byte header
 in the case of single sided IMG file the header is 01
 and double sided IMG has header 02.
""" 
SINGLE_SIDED_IMG_SIZE = SINGLE_SIDED_DSK_SIZE + 1
DOUBLE_SIDED_IMG_SIZE = DOUBLE_SIDED_DSK_SIZE + 1

class Img2Dsk(object):
    def __init__(self, input_filename, output_filename):
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.contents = None

    def check_size(self):
        try:
            self.input_file_size = os.path.getsize(self.input_filename)
        except os.error:
            sys.stderr.write("Could not get the size of {}".format(
                             self.input_filename))
            sys.exit(1)

        if self.input_file_size not in (SINGLE_SIDED_IMG_SIZE,
                                        DOUBLE_SIDED_IMG_SIZE):
            sys.stderr.write("{} size is not {:d}k nor {:d}k\n".format(
                             self.input_filename, SINGLE_SIDED_IMG_SIZE/1024,
                             DOUBLE_SIDED_IMG_SIZE/1024))
            sys.exit(2)

    def read_input_file(self):
        try:
            input_file = open(self.input_filename, "rb")
        except IOError:
            sys.stderr.write("Could not open input_file file {}".format(
                             self.input_filename))
            sys.exit(1)

        with input_file:
            self.raw_header = input_file.read(1)
            self.contents = input_file.read()

    def check_header(self):
        if not self.raw_header:
            sys.stderr.write("Could not read header\n")
            sys.exit(1)

        header, = struct.unpack("b", self.raw_header)
        if header * SINGLE_SIDED_DSK_SIZE + 1 != self.input_file_size:
            sys.stderr.write("Warning: IMG header does not match size\n")

    def write_dsk(self):
        try:
            output_file = open(self.output_filename, "wb")
        except IOError as e:
            sys.stderr.write("Failed to create file {}\n{}".format(
                             self.output_filename, str(e)))
            sys.exit(1)

        with output_file:
            try:
                output_file.write(self.contents)
            except IOError as e:
                sys.stderr.write("Failed to write to file {}\n{}".format(
                                 self.output_filename, str(e)))
                sys.exit(1)


    def convert(self):
        self.check_size()
        self.read_input_file()
        self.check_header()
        self.write_dsk()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: python img2dsk.py source_file target_file\n")
        sys.stderr.write("Convert IMG file to DSK file.\n")
        sys.exit(2)

    converter = Img2Dsk(sys.argv[1], sys.argv[2])
    converter.convert()
