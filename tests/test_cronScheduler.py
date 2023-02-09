from discordpibot.cronScheduler import compute_next_run
from datetime import datetime


def test_compute_next_run():
    # check that it works for the next minute
    now = datetime(2023, 2, 9, 20, 00)
    assert compute_next_run("* * * * *", now) == datetime(2023, 2, 9, 20, 1)
    assert compute_next_run("0 * * * *", now) == datetime(2023, 2, 9, 21, 0)
    assert compute_next_run("0 0 * * *", now) == datetime(2023, 2, 10, 0, 0)
    assert compute_next_run("0 0 1 * *", now) == datetime(2023, 3, 1, 0, 0)
    assert compute_next_run("0 0 * * 1", now) == datetime(2023, 2, 13, 0, 0)
    assert compute_next_run("0 0 1 1 *", now) == datetime(2024, 1, 1, 0, 0)
    assert compute_next_run("0 0 1 1 1", now) == datetime(2024, 1, 1, 0, 0)
    assert compute_next_run("2 0 * * 2", now) == datetime(2023, 2, 14, 0, 2)
    now = datetime(2023, 2, 9, 21, 19)
    assert compute_next_run("21 21 * * *", now) == datetime(2023, 2, 9, 21, 21)

    # now = datetime(2023, 2, 9, 20, 00)
    # assert compute_next_run("0 0 * * *", now) == datetime(2023, 2, 10, 0, 0)
    # assert compute_next_run("0 0 1 * *", now) == datetime(2023, 3, 1, 0, 0)
    # assert compute_next_run("0 0 * * 1", now) == datetime(2023, 2, 13, 0, 0)
    # assert compute_next_run("0 0 1 1 *", now) == datetime(2024, 1, 1, 0, 0)
    # assert compute_next_run("0 0 1 1 1", now) == datetime(2024, 1, 1, 0, 0)
    # assert compute_next_run("2 0 * * 2", now) == datetime(2023, 2, 14, 0, 2)
    # now = datetime(2023, 2, 9, 21, 19)
    # assert compute_next_run("21 21 * * *", now) == datetime(2023, 2, 9, 21, 21)

    # now = datetime(2023, 2, 9, 21, 00)
    # assert compute_next_run("0 22 * * 1-5", now) == datetime(2023, 2, 9, 22, 0)
    # assert compute_next_run("23 0-20/2 * * *", now) == datetime(2023, 2, 10, 0, 23)
