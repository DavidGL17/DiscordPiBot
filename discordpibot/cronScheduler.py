import re
import datetime


def compute_next_run(cron_expression: str, current_time: datetime.datetime = None):
    if current_time is None:
        current_time = datetime.datetime.now()

    cron_expression = re.split("\s+", cron_expression.strip())
    if len(cron_expression) != 5:
        raise ValueError("Invalid cron expression")

    (minute, hour, day, month, day_of_week) = cron_expression
    next_time = current_time.replace(microsecond=0, second=0, minute=0, hour=0)

    next_time += datetime.timedelta(days=1)
    while not evaluate_expression(next_time, minute, hour, day, month, day_of_week):
        next_time += datetime.timedelta(minutes=1)

    return next_time


def evaluate_expression(time, minute, hour, day, month, day_of_week):
    (minute, hour, day, month, day_of_week) = [
        x if x != "*" else "0-59" for x in [minute, hour, day, month, day_of_week]
    ]

    if not check_expression(time.minute, minute):
        return False
    if not check_expression(time.hour, hour):
        return False
    if not check_expression(time.day, day):
        return False
    if not check_expression(time.month, month):
        return False
    if not check_expression((time.weekday() + 1) % 7, day_of_week):
        return False

    return True


def check_expression(value, expression):
    tokens = expression.split(",")
    for token in tokens:
        if "-" in token:
            (start, end) = token.split("-")
            if int(start) <= value <= int(end):
                return True
        elif "/" in token:
            (start, step) = token.split("/")
            if (value - int(start)) % int(step) == 0:
                return True
        elif str(value) == token:
            return True

    return False
