from decimal import Decimal
from typing import Optional
from collections import namedtuple

import psycopg2
from psycopg2 import Error


class Bill:
    def __init__(self, stay_id: int, tariff: Decimal, stay_duration: int):
        super().__init__()
        self.stay_id = stay_id
        self.tariff = tariff
        self.stay_duration = stay_duration


Sector = namedtuple('Sector', [
    'id', 'name', 'vehicle_type_name', 'row', 'col', 'row_span', 'col_span'
])


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

    def get_sectors_data(self):
        raise NotImplementedError


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

    def get_sectors_data(self):
        with self._return_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc('get_sectors_data', [])
                results = cursor.fetchall()
                for i in range(len(results)):
                    results[i] = Sector(*results[i])

                return results
