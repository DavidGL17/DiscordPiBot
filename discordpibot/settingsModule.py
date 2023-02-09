import yaml

# Settings

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

cron_string = config["cron_string"]
control_file = config["control_file"]
feed_url = config["feed_url"]
user_agent = config["user_agent"]
channel_id = config["channel_id"]
token = config["token"]
