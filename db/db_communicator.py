from decimal import Decimal
from typing import Optional

import psycopg2
from psycopg2 import Error


class Bill:
    def __init__(self, stay_id: int, tariff: Decimal, stay_duration: int):
        super().__init__()
        self.stay_id = stay_id
        self.tariff = tariff
        self.stay_duration = stay_duration


class DatabaseCommunicator:
    def __init__(self):
        super().__init__()

    def new_stay(self, vehicle_type: str, license_plate: str) -> bool:
        raise NotImplementedError()

    def get_bill(self, license_plate: str):
        raise NotImplementedError()

    def insert_stay_end_info(self, stay_id: int, stay_duration: int,
                             payment_amount: Decimal) -> bool:
        raise NotImplementedError()


class PostrgesDatabaseCommunicator(DatabaseCommunicator):
    def __init__(self, user: str, password: str,
                 host: str, port: int, database: str):
        super().__init__()

        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def __enter__(self):
        try:
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            # return self.cursor
            return self
        except (Exception, psycopg2.Error) as error:
            print("Nie udało się połączyć z bazą danych.\nBłąd: ", error, "\n")

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def new_stay(self, vehicle_type: str, license_plate: str) -> bool:
        self.cursor.callproc('new_stay', [vehicle_type, license_plate])
        result = self.cursor.fetchone()[0]

        return result

    def get_bill(self, license_plate: str) -> Bill:
        self.cursor.callproc('get_bill', [license_plate])

        bill: Optional[Bill] = None

        buf = self.cursor.fetchone()[0]
        if buf is not None:
            bill = Bill(*buf)

        return bill

    def insert_stay_end_info(self, stay_id: int, stay_duration: int,
                             payment_amount: Decimal) -> bool:
        self.cursor.callproc('insert_stay_end_info',
                             [stay_id, stay_duration, payment_amount])

        result = self.cursor.fetchone()[0]

        return result
