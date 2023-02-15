# Setup Steps

- Turn on your Redwave FTIR device
- Connect your device to your PC via USB
- Query your PC for the port that the device is connected to 
- In `response.py`, change the port value
- In `request.py`, change the port value below to for a list of available commands.
- Open two terminals
- In terminal 1: run `python3 response.py`
- In terminal 2, run `python3 request.py`
- In `request.py`, change the command `{"command":"disconect"}` as desired; see documentation for a list of available commands

<br />
<br />

# API Description

_The API software will be available starting in XplorIR release v0.40 and later._

The following commands are available in a request/response fashion. Our Team Leader app or your own proprietary app will send a JSON command to Redwave's XplorIR device and the device's API return a JSON response. 

## disconnect

`{"command":"disconect"}`

Disconnects client from host

## get_wifi_info

`{"command":"get_wifi_info"}`

Gets Wifi information including: a list of available networks, the network that the device is connected, and whether the device has wifi enabled.

## set_wifi

`{"command":"set_wifi"}`

## get_commands

`{"command":"get_commands"}`

## get_sessions

Each time you run the device in single point mode or in continuous monitoring mode, we store the results as a session.  A single point session will have a single value while a continous monitoring session will have one or many values. To get a list of sessions from the device, send the following _get_sessions_ command:

`{"command":"get_sessions"}`

The response from this command is as follows:

```
{
		"errors": null,
		"description": "A list of sessions",
		"results": [
			{				
    			"date": "2023-01-31T20:47:37.224256",                
				"name": "2023-01-31/20-47-37"
                "type": "singlePoint",
                "uuid": "3eca380e-54c6-4a2f-9d9f-cd86fbd05c96",
			},
			{
                "date": "2023-02-02T10:37:17.114257",
				"name": "2023-02-02/10-37-17",
                "type": "continousMonitoring",
                "uuid": "7yty380e-54c6-4a2f-9d9f-cd86fbd05c96",    							
			}
		]
	}
```

## get_session

`{"command":"get_session"}`

## get_sample

`{"command":"get_sample"}`