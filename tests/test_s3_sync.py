from src.s3_sync import is_weekday
import datetime as dt


def test_is_weekday_monday():
    monday = dt.datetime(2024, 2, 5)
    assert is_weekday(monday) == True


def test_is_weekday_tuesday():
    tuesday = dt.datetime(2024, 2, 6)
    assert is_weekday(tuesday) == True


def test_is_weekday_wednesday():
    wednesday = dt.datetime(2024, 2, 7)
    assert is_weekday(wednesday) == True


def test_is_weekday_thursday():
    thursday = dt.datetime(2024, 2, 8)
    assert is_weekday(thursday) == True


def test_is_weekday_friday():
    friday = dt.datetime(2024, 2, 9)
    assert is_weekday(friday) == True


def test_is_weekday_saturday():
    saturday = dt.datetime(2024, 2, 10)
    assert is_weekday(saturday) == False


def test_is_weekday_sunday():
    sunday = dt.datetime(2024, 2, 11)
    assert is_weekday(sunday) == False
