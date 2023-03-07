# Setup Steps

If you're downloading the project for the first time...

On Windows using Powershell (PS>):
```
PS> git clone https://github.com/redwavetech/redwave-device-api-test-app.git
PS> cd redwave-device-api-test-app
```
If you've already cloned the project...
```
PS> cd redwave-device-api-test-app
PS> git pull origin master
```
Now create your virtual environment with...
```
PS> python -m venv venv
PS> .\venv\Scripts\activate
PS> python -m pip install -r requirements.txt
```
> If you run into an error like `Active.psql cannot be loaded because running scripts is disabled on this system` when trying to load your venv, you can try running your PowerShell as administrator and then run `Set-ExecutionPolicy AllSigned`.

<br />

At this point, the python app is ready to run.  Before you make a request from the python app to the device, please follow these steps:

- Turn on your Redwave device
- Connect your device to your PC via USB
- run `python ports.py` at your command prompt to determine which port your device is connected to
- change the port_name variable in this line `port_name = '/dev/ttys016'` in the request-response.py script
- run `python request-response.py` 

`request-response.py` is initially setup to send the `get_commands` command. To test other endpoints/commands, replace the command in this line, `msg = contsruct_payload_from_json('{"command":"get_commands"}')` in the `request-response.py` with your desired command. All the available commands are listed below.

When you're done, you can exit from your virtual environment with the following command:
```
PS> deactivate
```

<br />

# API Description

_NOTE: The API will be part of Redwave's XplorIR and ProtectIR devices. Additional information on when the API will feature real data and more endpoints will be posted on this page._

_NOTE 2: This API is not in a stable state and is subject to change._

The following commands are available in a request/response fashion. Our Team Leader app or your own proprietary app will send a JSON command to Redwave's device and the device's API will return a JSON response. 

## List of Commands

<table>
    <tr>
        <th>Command</th>
        <th>Availability</th>
    </tr>
    <tr>
        <td><a href="#disconnect">disconnect</a></td>
        <td>As a fixture only</td>
    </tr>
    <tr>
        <td><a href="#get_commands">get_commands</a></td>
        <td>As a fixture only</td>
    </tr>
    <tr>
        <td><a href="#get_sample">get_sample</a></td>
        <td>As a fixture only</td>
    </tr>
    <tr>
        <td><a href="#get_sessions">get_sessions</a></td>
        <td>As a fixture only</td>
    </tr>
    <tr>
        <td><a href="#get_session">get_session</a></td>
        <td>As a fixture only</td>
    </tr>
    <tr>
        <td><a href="#get_wifi_info">get_wifi_info</a></td>
        <td>As a fixture only</td>
    </tr>      
    <tr>
        <td><a href="#set_wifi">set_wifi</a></td>
        <td>As a fixture only</td>
    </tr> 
    <tr>
        <td><a href="#start_single_point">start_single_point</a></td>
        <td>As a fixture only</td>
    </tr> 
    <tr>
        <td><a href="#start_continuous">start_continuous</a></td>
        <td>As a fixture only</td>
    </tr>    
    <tr>
        <td><a href="#stop_continuous">stop_continuous</a></td>
        <td>As a fixture only</td>
    </tr>                     
    <tr>
        <td><a href="#get_device_info">get_device_info</a></td>
        <td>As a fixture only</td>
    </tr>                     
    <tr>
        <td><a href="#get_configuration">get_configuration</a></td>
        <td>As a fixture only</td>
    </tr>                     
    <tr>
        <td><a href="#set_configuration">set_configuration</a></td>
        <td>As a fixture only</td>
    </tr>                     
    <tr>
        <td><a href="#start_diagnostics">start_diagnostics</a></td>
        <td>As a fixture only</td>
    </tr>                              
    <tr>
        <td><a href="#get_diagnostics">get_diagnostics</a></td>
        <td>As a fixture only</td>
    </tr> 
    <tr>
        <td><a href="#shutdown">shutdown</a></td>
        <td>As a fixture only</td>
    </tr>                                                    
</table>

## Command Details

### <span id="disconnect">disconnect</span>

Disconnects the client from the host.

```json
{ 
    "command": "disconnect" 
}
```

The response from this command will be:

```json
{
    "message": "Connection successfully terminated.",
    "command": "disconnect"
    "succeeded": true,
}
```

### <span id="get_wifi_info">_get_wifi_info_</span>

Gets Wifi information including: a list of available networks, the network that the device is connected to, and whether the device has wifi enabled.

```json
{
    "command":"get_wifi_info"
}
```
The response from this command will be:
```json
{
    "command": "get_wifi_info",
    "message": "Successfully obtained list of nearby networks",
    "results": {
        "networks":[
            {
                "name": "Network A",
                "signalStrength": 96,
                "requiresPassword": true
            },
            {
                "name": "Network B",
                "signalStrength": 78,
                "requiresPassword": false
            }
        ],
        "connectedTo": "Network A",
        "isEnabled": false
    },
    "succeeded": true,
}
```

### <span id="set_wifi">_set_wifi_</span>

Sets Wifi settings including whether Wifi is on/off and which network it should be connected to.

```json
{
    "command":"set_wifi"
}
```
Response from this command will be:
```json
{
    "command":"set_wifi",
    "message": "Successfully set wifi configuration",
    "succeeded": true
}
```

### <span id="get_commands">_get_commands_</span>

This command will list the available commands on the device.  

```json
{
    "command":"get_commands"
}
```

The response for this command is as follows:

```json
{
    "description": "A list of commands",
    "message":"Successfully retrieved a list of commands",				
    "results": [
        {
            "command": "disconnect",
            "description": "Diconnects client from the host."
        },
        {
            "command": "get_sessions",
            "description": "Returns a list of sessions."
        },
        {
            "command": "get_wifi_info",
            "description": "Returns a list of available wifi networks, the currently connected network, and whether wifi is enabled."
        }
    ],
    "succeeded": true
}
```

### <span id="get_sessions">_get_sessions_</span>

Each time you run the device in single point mode or in continuous monitoring mode, we store the results as a session.  A single point session will have a single value while a continous monitoring session will have one or many values. To get a list of sessions from the device, send the following _get_sessions_ command:

```json
{
    "command":"get_sessions"
}
```

The response from this command is as follows:

```json
{
    "message": "Successfully retrieved a list of sessions",    
    "results": [
        {				
            "date": "2023-01-31T20:47:37.224256",                
            "name": "2023-01-31/20-47-37",
            "type": "singlePoint",
            "uuid": "3eca380e-54c6-4a2f-9d9f-cd86fbd05c96",
        },
        {
            "date": "2023-02-02T10:37:17.114257",
            "name": "2023-02-02/10-37-17",
            "type": "continousMonitoring",
            "uuid": "7yty380e-54c6-4a2f-9d9f-cd86fbd05c96",    							
        }
    ],
    "succeeded": true,
}
```

### <span id="get_session">_get_session_</span>

This endpoint gets details of a current sessions

```json
{
    "command":"get_session", 
    "args": { 
        "uuid": "7yty380e-54c6-4a2f-9d9f-cd86fbd05c96" 
    }
}
```

The response from this command is as follows:

```json
{
    "message": "Successfully retrieved session data",
    "results": {
        "date": "2023-01-31T20:47:37.224256",
        "name": "2023-01-31/20-47-37",
        "uuid": "7yty380e-54c6-4a2f-9d9f-cd86fbd05c96",						
        "data": [
            {            
                "uuid": "3eca380e-54c6-4a2f-9d9f-cd86fbd05c96",
                "name": "2023-01-31/20-45-37",   
                "date": "2023-01-31T20:45:37.224256",
                "coords": {
                    "lat": 12345,
                    "lon": 12321
                },            
                "compounds": []
            }, 
            {      
                "uuid": "3eca380e-54c6-4a2f-9d9f-cd86fbd05c96",
                "name": "2023-01-31/20-46-37",
                "date": "2023-01-31T20:46:37.224256",
                "coords": null,            
                "compounds": []
            },         
            {         
                "uuid": "eb8f268e-8007-45e9-9438-aadec17ac09f",
                "name": "2023-01-31/20-47-37",            
                "date": "2023-01-31T20:47:37.224256",
                "coords": {
                    "lat": 12345,
                    "lon": 12321
                },            					
                "compounds": [
                    {
                        "cas_number": "67-63-0",
                        "name": "2-Propanol",
                        "score": 0.982,
                        "is_top_hit": true
                    }
                ]
            }
        ]
    },
    "succeeded": true
}
```

### <span id="get_sample">_get_sample_</span>

The following endpoint will get detailed information on a specific sample.

```json
{
    "command":"get_sample"
}
```

The response from this command is as follows:

```json
{         
    "uuid": "eb8f268e-8007-45e9-9438-aadec17ac09f",  
    "name": "2023-01-31/20-47-37",          
    "date": "2023-01-31T20:47:37.224256",
    "coords": {
        "lat": 12345,
        "lon": 12321
    },            					
    "compounds": [
        {
            "cas_number": "67-63-0",
            "name": "2-Propanol",
            "score": 0.982,
            "is_top_hit": true
        }
    ],
    "succeeded": true,
}
```

### <span id="stop_continuous">_stop_continuous_</span>

The following endpoint will stop a continuous monitoring session.
```json
{
    "command":"stop_continuous"
}
```
The response from this command is as follows:

```json
{
    "command": "stop_continuous",
    "message": "Successfully stopped continuous monitoring session",
    "succeeded": true,
}
```

### <span id="get_device_info">_get_device_info_</span>

The following endpoint will retrieve information about the device.
```json
{
    "command":"get_device_info"
}
```
The response from this command is as follows:

```json
{		
    "command": "get_device_info",
    "data": {
        "serialNumber": "A1001024B",
        "instrumentId": "123456789",
        "softwareVersion": "0.41"
    },
    "message": "Successfully retrieved device info",
    "succeeded": true,
}
```

### <span id="start_continuous">_start_continuous_</span>

The following endpoint will start a continuous monitoring session.
```json
{
    "command":"start_continuous"
}
```
The response from this command is as follows:

```json
{
    "command": "start_continuous",
    "message": "Successfully started continuous monitoring session",
    "succeeded": true,
}
```

### <span id="start_single_point">_start_single_point_</span>

The following endpoint will start a single point detection.
```json
{
    "command":"start_single_point"
}
```
The response from this command is as follows:

```json
{
    "command": "start_single_point",
    "message": "Successfully started single point detection",
    "succeeded": true,
}
```

### <span id="get_configuration">_get_configuration_</span>

The following endpoint will get the device's configuration.
```json
{
    "command":"get_configuration"
}
```
The response from this command is as follows:

```json
{
    "command": "get_configuration",
    "data": {
        "ledAlarmsOn": false,
        "audioAlarmsOn": false,
        "bluetoothOn": false,
        "wifiOn": false			
    },
    "message": "Successfully retrieved configuration",
    "succeeded": true,
}
```

### <span id="set_configuration">_set_configuration_</span>

The following endpoint will set the device's configuration:
```json
{
    "command": "set_configuration",
    "args": {
        "ledAlarmsOn": false,
        "audioAlarmsOn": false,
        "bluetoothOn": false,
        "wifiOn": false			
    }
}

```
The response from this command is as follows:
```json
{
    "command": "set_configuration",
    "message": "Successfully set configuration",
    "succeeded": true,
}
```

### <span id="start_diagnostics">start_diagnostics</span>

The following endpoint will start a diagnostic test:
```json
{
    "command": "start_diagnostics",
}

```
The response from this command is as follows:
```json
{
    "command": "start_diagnostics",
    "message": "Successfully started a diagnostic test",
    "succeeded": true,
}
```

### <span id="get_diagnostics">_get_diagnostics</span>

The following endpoint will get a list of diagnostic tests:
```json
{
    "command": "get_diagnostics",
}

```
The response from this command is as follows:
```json
{
    "command": "get_diagnostics",
    "data": {
        "diagnostics": [
            {
                "date": "2023-01-31T20:47:37.224256",
                "results": "passed"
            }
        ]
	},
    "message": "Successfully retrieved diagnostic tests",
    "succeeded": true,
}
```

### <span id="shutdown">_shutdown_</span>

The following endpoint will shutdown the device.
```json
{
    "command":"shutdown"
}
```
The response from this command is as follows:

```json
{
    "command": "shutdown",
    "message": "Device is shutting down",
    "succeeded": true,
}
```



