import yaml
import pytz

# Settings

with open("settings.yaml", "r") as f:
    config = yaml.safe_load(f)

cron_string = config["cron_string"]
timezone = pytz.timezone(config["timezone"])
control_file = config["control_file"]
feed_url = config["feed_url"]
user_agent = config["user_agent"]
channel_id = config["channel_id"]
token = config["token"]
log_file = config["log_file"]
