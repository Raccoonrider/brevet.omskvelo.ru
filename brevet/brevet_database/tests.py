from io import BytesIO
import datetime

from django.test import TestCase
from django.conf import settings

from brevet_database.file_processors import read_xls_protocol, read_xlsx_protocol

class FileProcessorsTest(TestCase):
    reference_data = (
        {
            'date': datetime.date(2023, 7, 8), 
            'distance': 300, 
            'code': 511042, 
            'results': [
                {'homologation': '315150', 'surname': 'Ermakov', 'name': 'Artem', 'code': 511042, 'time': datetime.timedelta(seconds=50040), 'medal': False, 'female': False}, 
                {'homologation': '315151', 'surname': 'Eskov', 'name': 'Vitaliy', 'code': 511042, 'time': datetime.timedelta(seconds=53820), 'medal': False, 'female': False}, 
                {'homologation': '315152', 'surname': 'Klapotovskiy', 'name': 'Denis', 'code': 511042, 'time': datetime.timedelta(seconds=46020), 'medal': False, 'female': False}, 
                {'homologation': '315153', 'surname': "Kon'Kov", 'name': 'Maksim', 'code': 511042, 'time': datetime.timedelta(seconds=45360), 'medal': False, 'female': False}, 
                {'homologation': '315154', 'surname': 'Krupkin', 'name': 'Andrey', 'code': 511042, 'time': datetime.timedelta(seconds=49620), 'medal': False, 'female': False}, 
                {'homologation': '315155', 'surname': 'Osipov', 'name': 'Aleksey', 'code': 511042, 'time': datetime.timedelta(seconds=53820), 'medal': False, 'female': False}, 
                {'homologation': '315156', 'surname': 'Skidanov', 'name': 'Yaroslav', 'code': 511042, 'time': datetime.timedelta(seconds=56220), 'medal': False, 'female': False}, 
                {'homologation': '315157', 'surname': 'Sokolov', 'name': 'Maxim', 'code': 511042, 'time': datetime.timedelta(seconds=49800), 'medal': False, 'female': False}, 
                {'homologation': '315158', 'surname': 'Sustavov', 'name': 'Aleksey', 'code': 511042, 'time': datetime.timedelta(seconds=54000), 'medal': False, 'female': False}, 
                {'homologation': '315159', 'surname': 'Ukolova', 'name': 'Alena', 'code': 511042, 'time': datetime.timedelta(seconds=53820), 'medal': False, 'female': True}
            ]
        }, 
        None)
    
    def test_load_xlsx(self):
        path = settings.BASE_DIR / 'brevet_database' / 'fixtures' / 'homologation.xlsx'

        data = BytesIO()
        data.write(path.read_bytes())
        data.seek(0)


        self.assertEqual(read_xlsx_protocol(data), self.reference_data)

    def test_load_xls(self):
        path = settings.BASE_DIR / 'brevet_database' / 'fixtures' / 'homologation.xls'

        data = BytesIO()
        data.write(path.read_bytes())
        data.seek(0)

        self.assertEqual(read_xls_protocol(data), self.reference_data)
