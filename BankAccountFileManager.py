import os
import re
import shutil

from PyPDF2 import PdfReader
from dotenv import dotenv_values


class BankAccountFileManager:
    def __init__(self):
        self.__env = {}
        self.__input_filepath = ""
        self.__input_files = []
        self.__pdf_details = []
        self.__output_name = ""
        self.__validate_details = [
            "Girokonto Nummer",
            "Extra-Konto Nummer",
            "Datum",
            "Auszugsnummer"
        ]

    def __enter__(self):
        if os.path.isfile(".env"):
            self.__env = dotenv_values(".env")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_file_list(self):
        input_filepath = self.__env["input_filepath"]
        if input_filepath == "":
            return False

        for filename in os.listdir(input_filepath):
            f = os.path.join(input_filepath, filename)
            if os.path.isfile(f):
                self.__input_files.append(f)

    def build_filename_by_details(self):
        pdf_details = self.__pdf_details
        if len(pdf_details) < 3:
            print("somethings wrong with the details")
            print(pdf_details)
            return False
        # get all detail values
        details = [i[1].strip() for i in pdf_details]

        # build outputname by details
        output_name = ""
        output_name += details[0] + "." + details[1][-4:]
        output_name += "," + [details[2], "0" + str(details[2])][int(details[2]) < 10]
        output_name += "_" + details[1] + "_Kontoauszug.pdf"
        return output_name

    def validate_details(self, list_of_details):
        details = [i[0] for i in list_of_details]
        return all(item in self.__validate_details for item in details)

    def get_filename_details(self, file):
        reader = PdfReader(file)
        text = reader.pages[0].extract_text()
        match_details = re.findall(r"^.*\b(Girokonto Nummer|Extra-Konto Nummer|Datum|Auszugsnummer)(.*)$", text, re.MULTILINE)
        if self.validate_details(match_details):
            self.__pdf_details = match_details
            self.__output_name = self.build_filename_by_details()
        else:
            print('validation failed')
            return False

    def rename_files(self):
        self.get_file_list()
        file_list = self.__input_files
        if len(file_list) == 0:
            print('no files given')
            return False


        """ generate output filename based on PDF details
        then rename the file and move it to a output path
        """
        # return output name with path
        input_filepath = self.__env["input_filepath"]
        output_filepath = self.__env["output_filepath"]

        for file in file_list:
            self.get_filename_details(file)
            if not self.__output_name:
                return False
            new_name = input_filepath + "\\" + self.__output_name
            new_path = output_filepath + "\\" + self.__output_name

            if file != new_name:
                if not os.path.exists(new_name):
                    os.rename(file, new_name)
                if not os.path.exists(new_path):
                    shutil.move(new_name, new_path)
            if file == new_name:
                if not os.path.exists(new_path):
                    shutil.move(file, new_path)
            else:
                print(self.__output_name)
                print(file)
                print('---')
