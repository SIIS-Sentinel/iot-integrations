# Config file for the Home Assistant MQTT integrations

# MQTT broker and base topics
broker_addr: str = "hub.local"
cafile: str = "/certs/CA.pem"
certfile: str = "/certs/node.crt"
keyfile: str = "/certs/node.key"
username: str = "adrien"
password: str = "mqttpassword"
base_topic: str = "home/"
scheduler_topic: str = "scheduler/"
port: int = 8883

# MQTT topic suffixes
set_suffix: str = "/set"
state_suffix: str = "/state"
available_suffix: str = "/available"

# Sensor update delay, in seconds
update_delay: float = 1

# Payloads
online_payload: str = "online"
offline_payload: str = "offline"

# Hardware connections
pin: int = 18
