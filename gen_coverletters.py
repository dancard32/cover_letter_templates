import json
import os
from datetime import date

def get_tex(fid):
    with open(fid) as f:
        str_out = ""
        for lines in f:
            str_out += lines
    return str_out

def get_json():
    with open("letters.json") as f:
        letters_json = json.load(f)
    return letters_json

def main():
    str_main = get_tex('main.tex')
    letters_json = get_json()

    for position in letters_json:

        tmp_position = get_tex(f"rep/{position.lower()}.tex")

        for json_data in letters_json[position]["Companies"]:
            tmp_out = str_main.replace("\import{rep/}{template}", tmp_position)
            company_name = json_data["company"]
            company_name_underscored = company_name.replace(" ", "_")
            company_name_nospaces = company_name.replace(" ", "")

            tmp_out = tmp_out.replace("<COMPANY>", company_name)
            tmp_out = tmp_out.replace("<COMPANY-PHOTO>", f"{company_name_underscored.lower()}")
            tmp_out = tmp_out.replace("<RECIPIENT>", json_data['recipient'])
            if json_data['recipient-prefix'] != "na":
                tmp_out = tmp_out.replace("<RECIPIENT-PREFIX>", json_data['recipient-prefix'])
            else:
                tmp_out = tmp_out.replace("<RECIPIENT-PREFIX>", '')
            tmp_out = tmp_out.replace("<ADDRESS-LINE1>", json_data['address-1'])
            tmp_out = tmp_out.replace("<ADDRESS-LINE2>", json_data['address-2'])
            tmp_out = tmp_out.replace("<CITY-STATE-ZIP>", json_data['city-state-zip'])
            tmp_out = tmp_out.replace("<FULL-POSITION>", letters_json[position]["full-position"])

            if json_data['recipient'] != "Hiring Manager":
                tmp_name = json_data['recipient'].replace(" ", "-")
                file_name = f"{company_name_nospaces}-{tmp_name.lower()}_{str(date.today())}"
            else:
                file_name = f"{company_name_nospaces}_{str(date.today())}"

            text_file = open(f"{file_name}.tex", "w")
            text_file.write(tmp_out)
            text_file.close()

            os.system(f"pdflatex {file_name}.tex")

            pdfs = os.listdir(f"Jobs_2023/{position.lower()}")
            for pdf in pdfs:
                if file_name.split('_')[0] in pdf.split('_'):
                    os.system(f"rm Jobs_2023/{position.lower()}/{pdf}")

            os.system(f"mv {file_name}.pdf Jobs_2023/{position.lower()}/")
            os.system(f"rm {file_name}.tex {file_name}.aux {file_name}.log {file_name}.out ")

if __name__ == "__main__":
    main()
