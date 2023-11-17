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

    def new_stay(self, vehicle_type: str, license_plate: str) -> str:
        raise NotImplementedError()

    def get_bill(self, license_plate: str):
        raise NotImplementedError()

    def finish_stay(self, stay_id: int, stay_duration: int,
                    payment_amount: Decimal) -> bool:
        raise NotImplementedError()


class PostgresDatabaseCommunicator(DatabaseCommunicator):
    def __init__(self, user: str, password: str,
                 host: str, port: int, database: str):
        super().__init__()

        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def _return_connection(self):
        connection = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database
        )
        return connection

    # def __enter__(self):
    #     try:
    #         self.connection = psycopg2.connect(
    #             user=self.user,
    #             password=self.password,
    #             host=self.host,
    #             port=self.port,
    #             database=self.database
    #         )
    #         self.cursor = self.connection.cursor()
    #         # return self.cursor
    #         return self
    #     except (Exception, psycopg2.Error) as error:
    #         print("Nie udało się połączyć z bazą danych.\nBłąd: ", error, "\n")
    #
    # def __exit__(self, exc_type, exc_value, traceback):
    #     if self.cursor:
    #         self.cursor.close()
    #     if self.connection:
    #         self.connection.close()

    def new_stay(self, vehicle_type: str, license_plate: str) -> str:
        with self._return_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc('new_stay', [vehicle_type, license_plate])
                sector_name: str = cursor.fetchone()[0]

                connection.commit()

                return sector_name

    def get_bill(self, license_plate: str) -> Bill:
        with self._return_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc('get_bill', [license_plate])

                bill: Optional[Bill] = None

                buf = cursor.fetchone()
                if buf is not None and len(buf) == 3 \
                        and not any([x is None for x in buf]):
                    bill = Bill(*buf)

                return bill

    def finish_stay(self, stay_id: int, stay_duration: int,
                    payment_amount: Decimal) -> bool:
        with self._return_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc('finish_stay',
                                [stay_id, stay_duration, payment_amount])
                result = cursor.fetchone()[0]
                connection.commit()

                return result
