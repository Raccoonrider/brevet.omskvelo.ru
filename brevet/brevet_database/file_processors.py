from datetime import datetime, timedelta

import xlrd
import openpyxl

def read_xls_protocol(file):
    """Reads *.xls file returned by ACP"""
    exception = None
    content = {}
    try:
        book = xlrd.open_workbook(file_contents=file.read(), ignore_workbook_corruption=True)
        sheet = book.sheet_by_index(0)
        rows = sheet.nrows

        date = sheet.cell_value(rowx=1, colx=5)
        distance = sheet.cell_value(rowx=1, colx=6)
        code = str(sheet.cell_value(rowx=1, colx=4))  

        content["date"] = datetime.strptime(date, "%d/%m/%Y").date()
        content["distance"] = int(distance[:-2].strip())
        content["code"] = int("".join(x for x in code.split(".")[0] if x.isdigit()))
        content["results"] = []

        row = 3
        col_homologation = 0
        col_surname = 1
        col_name = 2
        col_code = 5
        col_time = 6
        col_medal = 7
        col_female = 8

        while row < rows:

            # Read data
            homologation = sheet.cell_value(rowx=row, colx=col_homologation)
            surname = sheet.cell_value(rowx=row, colx=col_surname)
            name = sheet.cell_value(rowx=row, colx=col_name)
            code = str(sheet.cell_value(rowx=row, colx=col_code))
            time = sheet.cell_value(rowx=row, colx=col_time)
            medal = sheet.cell_value(rowx=row, colx=col_medal)
            female = sheet.cell_value(rowx=row, colx=col_female)
            
            # Format data
            homologation = str(int(homologation))
            surname = surname.title()
            name = name.title()
            code = int("".join(x for x in code if x.isdigit()))
            h,m = time.split(":")
            time = timedelta(hours=int(h), minutes=int(m))
            medal = medal != ""
            female = female != ""
            
            result = {
                'homologation' : homologation,
                'surname' : surname,
                'name' : name,
                'code' : code,
                'time' : time,
                'medal' : medal,
                'female' : female,
            }
            content["results"].append(result)

            row +=1 
            book.release_resources()

            
    except Exception as e:
        exception = str(e)

    return content, exception


def read_xlsx_protocol(file):
    """Reads *.xlsx file returned by ACP"""
    exception = None
    content = {}
    try:
        book = openpyxl.load_workbook(filename=file, read_only=True)
        sheet = book.worksheets[0]

        date = sheet['F2'].value
        distance = sheet['G2'].value
        code = sheet['E2'].value

        content["date"] = datetime.strptime(date, "%d/%m/%Y").date()
        content["distance"] = int(''.join(x for x in distance if x.isdigit()))
        content["code"] = int("".join(x for x in code.split(".")[0] if x.isdigit()))
        content["results"] = []

        for row in sheet.iter_rows(min_row=4, values_only=True):
            if row[1] is None:
                break

            # Read data
            homologation = str(row[0]).strip()
            surname = row[1].title()
            name = row[2].title()
            code = int("".join(x for x in row[5] if x.isdigit()))
            h,m = row[6].split(":")
            time = timedelta(hours=int(h), minutes=int(m))
            medal = row[7] is not None
            female = row[8] is not None            
            
            content["results"].append(
                {
                    'homologation' : homologation,
                    'surname' : surname,
                    'name' : name,
                    'code' : code,
                    'time' : time,
                    'medal' : medal,
                    'female' : female,
                }
            )

            
    except Exception as e:
        exception = str(e)

    return content, exception
