## Steps

1. Open two terminals
2. In `response.py`, change the port value
3. In terminal 1: run `python3 response.py`
4. In `request.py`, change the port value
5. In `request.py`, change the command `{"command":"disconect"}` as desired
6. In terminal 2, run `python3 request.py`
7. Repeat steps 5-6 as needed

## Commands

**disconnect**

`{"command":"disconect"}`

Disconnects client from host

**get_wifi_info**

`{"command":"get_wifi_info"}`

Gets Wifi information including: a list of available networks, the network that the device is connected, and whether the device has wifi enabled.

**set_wifi**

`{"command":"set_wifi"}`



**get_commands**

`{"command":"get_commands"}`

**get_sessions**

`{"command":"get_sessions"}`

**get_session**

`{"command":"get_session"}`

**get_sample**

`{"command":"get_sample"}`