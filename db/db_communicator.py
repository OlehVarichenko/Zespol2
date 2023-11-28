from decimal import Decimal
from typing import Optional, List
from collections import namedtuple

import psycopg2
from psycopg2 import Error


class Bill:
    """
    Klasa reprezentująca rachunek wystawiany kierowcom na wyjeździe z parkingu.
    """
    def __init__(self, stay_id: int, tariff: Decimal, stay_duration: int):
        """
        Args:
            stay_id(int): ID postoju do opłaty ściągnięte z bazy danych
            tariff(Decimal): Taryfa postojowa dla danego typu samochodu za godzinę
            stay_duration(int): Czas postoju w sekundach
        """
        super().__init__()
        self.stay_id = stay_id
        self.tariff = tariff
        self.stay_duration = stay_duration


class Sector:
    """
    Klasa przechowuje informację o sektorach w celu naniesienia ich na schemat i nie tylko.
    """
    def __init__(self, db_id: int, name: str, vehicle_type_name: str,
                 row: int, col: int, row_span: int, col_span: int):
        """
        Funkcja
        Args:
            db_id(int): ID sektora
            name(str): Nazwa sektora (A, B, C, itp)
            vehicle_type_name(str): Typ pojazdu
            row(int): Początkowy wiersz schematu będącego QGridLayout'em
            col(int): Początkowa kolumna schematu będącego QGridLayout'em
            row_span(int): Rozpiętość do dołu (pod względem wierszów)
            col_span(int): Rozpiętość do prawej strony (pod względem kolumn)
        """
        super().__init__()
        self.db_id = db_id
        self.name = name
        self.vehicle_type_name = vehicle_type_name
        self.row = row
        self.col = col
        self.row_span = row_span
        self.col_span = col_span


class DatabaseCommunicator:
    """
    Generyczny interfejs (klasa abstrakcyjna) do komunikowania się z bazą danych.
    Do każdego systemu zarządzania relacyjnymi bazami danych należy tworzyć klasę implementującą ten interfejs.
    """
    def __init__(self):
        super().__init__()

    def new_stay(self, vehicle_type: str, license_plate: str) -> Optional[str]:
        """
        Funkcja wywoływana w razie braku czynnych postojów danego samochodu w bazie.

        Powinna wywoływać odpowiednią funkcję osadzoną SQL o takiej samej nazwie na odpowiednim serwerze bazodanowym.

        Zwraca nazwę sektoru do parkowania pojazdu lub None w razie braku miejsc dla danego typu pojazdu. W razie braku
        miejsc należy zaimplementować wyświetlanie odpowiedniego komunikatu o braku miejsc.

        Może wyrzucać wyjątki.

        Args:
            vehicle_type(str): Wykryty typ samochodu dostarczony przez YOLOv7
            license_plate(str): Wykryty numer rejestracyjny dostarczony przez YOLOv7

        Returns:
            Optional[str]: Nazwa sektoru do parkowania pojazdu, taka jak A, B, C, itp

        """
        raise NotImplementedError()

    def get_bill(self, license_plate: str) -> Optional[Bill]:
        """
        Funkcja zwraca rachunek w razie obecności w bazie danych wpisu czynnego postoju.
        W razie nieobecności takowego wpisu zrwaca None.

        Powinna wywoływać odpowiednią funkcję osadzoną SQL o takiej samej nazwie na odpowiednim serwerze bazodanowym.

        Może wyrzucać wyjątki.

        Args:
            license_plate(str): Numer rejestracyjny

        Returns:
            Optional[Bill]: Obiekt klasy Bill lub None

        """
        raise NotImplementedError()

    def finish_stay(self, stay_id: int, stay_duration: int,
                    payment_amount: Decimal) -> None:
        """
        Funkcja uruchamia odpowiednią procedurę osadzoną SQL, kończącą postój samochodu.

        W ciele funkcji powinno się wywoływać odpowiednią funkcję osadzoną SQL
        o takiej samej nazwie na odpowiednim serwerze bazodanowym.

        Może wyrzucać wyjątki.

        Args:
            stay_id(int): ID postoju do zamknięcia ściągnięte z bazy danych
            stay_duration(int): Czas postoju w sekundach
            payment_amount(Decimal): Zapłacona kwota notowana w bazie danych
        """
        raise NotImplementedError()

    def get_sectors_data(self) -> List[Sector]:
        """
        Funkcja zwraca dane o sektorach w celu uzupełnienia schematu w aplikacji.

        W ciele funkcji powinno się wywoływać odpowiednią funkcję osadzoną SQL
        o takiej samej nazwie na odpowiednim serwerze bazodanowym.

        Może wyrzucać wyjątki.

        Returns:
            List[Sector]: Dane o istniejących sektorach

        """
        raise NotImplementedError


class PostgresDatabaseCommunicator(DatabaseCommunicator):
    """
    Klasa implementująca bazowy interfejs DatabaseCommunicator.
    Patrz dokumentację zaimplementowanych funkcji w dokumentacji interfejsu.
    """
    def __init__(self, user: str, password: str,
                 host: str, port: int, database: str):
        """
        Funkcja przyjmuje dane do późniejszego nawiązywania połączeń z BD.

        Args:
            user(str):
            password(str):
            host(str):
            port(str):
            database(str):
        """
        super().__init__()

        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def _return_connection(self):
        """
        Funkcja zwraca połączenie z BD Postgres w celu użycia wewnątrz pythonowej klauzuli "with".

        Returns:
            postgres_connection

        """
        connection = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database
        )
        return connection

    def new_stay(self, vehicle_type: str, license_plate: str) -> Optional[str]:
        """
        Implementacja funkcji z interfejsu bazowego. Patrz ogólną dokumentację w tym miejscu.

        Wykonuje operacje wewnątrz klauzul "with", a więc zarządza połączeniem samodzielnie.

        Args:
            vehicle_type:
            license_plate:

        Returns:
            Optional[str]

        """
        with self._return_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc('new_stay', [vehicle_type, license_plate])
                sector_name: str = cursor.fetchone()[0]

                connection.commit()

                return sector_name

    def get_bill(self, license_plate: str) -> Optional[Bill]:
        """
        Implementacja funkcji z interfejsu bazowego. Patrz ogólną dokumentację w tym miejscu.

        Wykonuje operacje wewnątrz klauzul "with", a więc zarządza połączeniem samodzielnie.

        Args:
            license_plate:

        Returns:
            Optional[Bill]
        """
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
                    payment_amount: Decimal):
        """
        Implementacja funkcji z interfejsu bazowego. Patrz ogólną dokumentację w tym miejscu.

        Wykonuje operacje wewnątrz klauzul "with", a więc zarządza połączeniem samodzielnie.

        Args:
            stay_id:
            stay_duration:
            payment_amount:

        """
        with self._return_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc('finish_stay',
                                [stay_id, stay_duration, payment_amount])
                connection.commit()

    def get_sectors_data(self) -> List[Sector]:
        """
        Implementacja funkcji z interfejsu bazowego. Patrz ogólną dokumentację w tym miejscu.

        Wykonuje operacje wewnątrz klauzul "with", a więc zarządza połączeniem samodzielnie.

        Returns:
            List[Sector]

        """
        with self._return_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc('get_sectors_data', [])
                results = cursor.fetchall()
                for i in range(len(results)):
                    results[i] = Sector(*results[i])

                return results
