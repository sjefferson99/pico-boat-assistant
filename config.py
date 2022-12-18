# Registered modules - Name and module ID
registered_modules = {
"hub" : 1,
"lights" : 2,
"relays" : 3
}

# I2C
## List modules to enable for this node from registered modules:
local_modules = ["hub", "relays"]
## GPIO PIN numbers
sda1 = 2
scl1 = 3
## Default 100000
i2c1_freq = 100000

# Network
WIFI_SSID = "your SSID here!"
WIFI_PASS = "Your PSK here!"

## (seconds between connectivity tests), enter 0 to disable
heartbeat_interval = 300
## URL for heartbeat test - pick a high uptime site that returns http 200
heartbeat_url = "https://api.ipify.org"

# Relays
## {relayid: value,...}
initial_values = {1: 1, 2: 1, 3: 0, 4: 0}
## ID of relay will reset on heartbeat failure, enter 0 for no relay
network_relay = 1
## Duration in ms for network relay to remain off on failed test reset
reset_duration = 4000