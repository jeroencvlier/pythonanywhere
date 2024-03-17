from pythonanywhere_scripts import telegram_bot


def test_send_mess_blank():
    try:
        telegram_bot.send_mess()
        raise AssertionError("Exception not raised")
    except TypeError:
        pass
    except NameError:
        pass


def test_send_mess():
    try:
        telegram_bot.send_mess("Test Message!")
    except Exception as error:
        raise AssertionError("Exception") from error
