# Description

This python app exists to help our integrators understand how Redwave's API works. You may not be developing your integration in python but, since python is fairly common, this app can help you become familiar with how to establish a connection and send/receive commands from our device. Currently, the API exists on our InterceptIR and XplorIR devices.

## On Windows using Powershell

If you're downloading the project for the first time...

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

- Connect the USB cable to your PC but not to the device (yet)
- run `python ports.py` at the command prompt to determine which port your device is connected to
- Turn on Redwave's InterceptIR device and wait for the green light to come on
- Connect the other end of the USB cable to the InterceptIR (this must be done within a couple seconds of when the green light comes on)
- When the port name appears, press `ctrl c` to exit
- Turn off the device


Now that you know the port, change the the PORT_NAME variable in the python script with the following steps:

- open `request-response.py`, find this line `PORT_NAME = 'COMxx'` near the top of the file, and change the `PORT_NAME` value to the port your device is connected to

Now that the `PORT_NAME` is updated, it's time to connect to the API with the following steps:

- Connect the USB cable to your PC but not to the device (yet)
- run `python request-response.py` at the command line
- Turn on Redwave's InterceptIR device and wait for the green light to come on
- Connect the other end of the USB cable to the InterceptIR (this must be done within a couple seconds of when the green light comes on)
- You should be ready to send commands to the device within 60 seconds

## On Mac

```
$ git clone https://github.com/redwavetech/redwave-device-api-test-app.git
$ cd redwave-device-api-test-app
```
If you've already cloned the project...
```
$ cd redwave-device-api-test-app
$ git pull origin master
```
Now create your virtual environment with...
```
$ python -m venv venv
$ source venv/bin/activate
$ python -m pip install -r requirements-mac.txt
```

If you're on a Mac, you have the ability to send command requests in one terminal while listening to responses in the other. To do this...

- Connect the USB cable to your Mac but not to the device (yet)
- Open a terminal window and run `python response.py`
- Turn on Redwave's InterceptIR device and wait for the green light to come on
- Connect the other end of the USB cable to the InterceptIR (this must be done within a couple seconds of when the green light comes on)
- Within ~60 seconds, the device should be ready to receive commands with the following steps:
- Open another terminal
- Run `python -m venv venv`
- Run `source venv/bin/activate`
- Run `python request.py --command='{"command": "get_device_info"}'`. The response should appear in the other terminal

To test other commands, replace the `--command=` argument with your desired command. All the available commands are listed below.

When you're done, you can exit from your virtual environment with the following command: `deactivate`

<br />

# Message Format

The format of the message following the following format: 

```
  * In-Memory View
  * +-----+-----+----------+-----------------------+-----+-----+-----+
  * | SOH | STX |   pLen   |        Payload        | CRC | ETX | EOT |
  * +-----+-----+----------+-----------------------+-----+-----+-----+
  * 0     1     2          6                      N-3   N-2   N-1    N	(Bytes)
```

Here is detailed information on each packet:

```
 *    ___________________________________________________________
 *    - SOH                                                      \
 *        Start of Heading ASCII control character 0x01.          \
 *                                                                 \____ Header
 *    - STX                                                        /     2 Bytes
 *        Start of Text ASCII control character 0x02.             /
 *    ___________________________________________________________/
 *    - pLen                                                     \
 *        Unsigned integer (little endian) representing the       \
 *        length of Payload. This should always end up being       \____ Payload length
 *        n-9 bytes with respect to this structure. Doubles        /     4 Bytes
 *        as an additional packet validity check.                 /
 *    ___________________________________________________________/
 *    - Payload                                                  \
 *        Serialized JSON data. This is the user data to be       \
 *        extracted if and only if:                                \
 *            1. Header exists at the beginning of the packet       \___ Payload (user data)
 *            2. pLen matches the length of the payload             /    N-9 Bytes
 *            3. CRC matches the receiving ends crc calculation    /
 *            4. Footer exists at the end of the packet           /
 *    ___________________________________________________________/
 *    - CRC                                                      \
 *        8-bit cyclic redundancy check on Payload. This greatly  \_____ Cyclic Redundancy Check
 *        mitigates the chances of processing invalid user data   /      1 Bytes
 *    ___________________________________________________________/
 *    - ETX                                                      \
 *        End of Text ASCII control character 0x03.               \
 *                                                                 \____ Footer
 *    - EOT                                                        /     2 Bytes
 *        End of Transmission ASCII control character 0x04.       /
 *    ___________________________________________________________/
```

Failure to correctly format your message in the above format will results in an `Invalid packet format` error being returned.  Here is a visual representation of the message format:

![message format](message-format.png "Message Format")

<br />

# API Description

_NOTE: The API will be part of Redwave's XplorIR and InterceptIR devices._

The following commands are available in a request/response fashion. Our Team Leader app or your own proprietary app will send a JSON command to Redwave's device and the device's API will return a JSON response. 

## List of Commands

<table>
    <tr>
        <th>Command</th>
        <th>Availability</th>
    </tr>
    <tr>
        <td><a href="#get_device_info">get_device_info</a></td>
        <td>Available</td>
    </tr>
    <tr>
        <td><a href="#start_cm">start_cm</a></td>
        <td>Available</td>
    </tr>    
    <tr>
        <td><a href="#cancel_cm">cancel_cm</a></td>
        <td>Available</td>
    </tr>     
    <tr>
        <td><a href="#disconnect">disconnect</a></td>
        <td>Available</td>
    </tr>                     
    <!-- <tr>
        <td><a href="#start_background_collection">start_background_collection</a></td>
        <td>Next release</td>
    </tr> 
    <tr>
        <td><a href="#start_sample_collection">start_sample_collection</a></td>
        <td>Next release</td>
    </tr>   -->
    <!-- <tr>
        <td><a href="#cancel_spd">cancel_spd</a></td>
        <td>Next release</td>
    </tr> -->
    <tr>
        <td><a href="#get_sessions">get_sessions</a></td>
        <td>Available</td>
    </tr>
    <tr>
        <td><a href="#get_session">get_session</a></td>
        <td>Available</td>
    </tr>  
    <tr>
        <td><a href="#get_sample">get_sample</a></td>
        <td>Available</td>    
    </tr>       
    <tr>
        <td><a href="#run_validation_background">run_validation_background</a></td>
        <td>Not yet released</td>
    </tr>                              
    <tr>
        <td><a href="#run_validation_sample">run_validation_sample</a></td>
        <td>Not yet released</td>
    </tr> 
    <tr>
        <td><a href="#run_advanced_validation">run_advanced_validation</a></td>
        <td>Not yet released</td>
    </tr>                                      
    <tr>
        <td><a href="#get_diagnostics">get_diagnostics</a></td>
        <td>Available</td>
    </tr>                              
    <tr>
        <td><a href="#get_validations">get_validations</a></td>
        <td>Available</td>
    </tr> 
    <tr>
        <td><a href="#get_validation">get_validation</a></td>
        <td>Not yet released</td>
    </tr>                                                    
</table>

## Command Details

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
  "data": {
    "instrumentId": "011339ef1d0000c1",
    "lastIgramDir": 1,
    "locationLat": 41.4129093,
    "locationLon": -73.4220129,
    "macAddress": "00:04:f3:3d:b0:12",
    "softwareVersion": "13.09",
    "state": "idle"
  },
  "date": "2024-05-13T08:53:55.00000Z",
  "message": "Successfully retrieved device info",
  "responseTo": "get_device_info",
  "serialNumber": "X01530523D",
}
```

Note: locationLat and locationLon can and probably will be null.

### <span id="start_cm">_start_cm_</span>
<br />

> ### About Continuous Monitoring states
>
> When the device is in continuous monitoring mode, the device can be in any of the following states:
>
> - busy
> - monitoring
> - detection
> - identification
> - saturation
>
> Each state is explained more below. 

<br />

The following command will start a continuous monitoring session. Once a continuous monitoring session has been started, the device will send messages approximately every 5 seconds.  The type of response depends on the state the device is in. Here is the request command:

Request:

```json
{
    "command":"start_cm"
}
```

Response:

After sending the initial request, the device will be busy for up to 10 minutes while it builds it's models. During this time, the device will send the following response every 4 seconds:

```json
{  
  "date": "2023-01-31T20:47:43.224256",
  "message": "The device is busy",
  "responseTo": "start_cm",
  "status": "busy"
}
```

Once the device is done building it's models, it will go into a monitoring state. It will stay in this state until it detects a gas. The response from the device during this state will be:

```json
{  
  "date": "2023-01-31T20:47:43.224256",
  "message": "The device is monitoring. ",
  "responseTo": "start_cm",
  "status": "monitoring"
}
```

When the device detects a gas, it will be in the detection state while it runs our algorithms to find a match. During this state the device will respond with the following:

```json
{  
  "date": "2023-01-31T20:47:43.224256",
  "message": "A detection event occurred.",
  "responseTo": "start_cm",
  "status": "detection"
}
```

Shortly after that and if the detection state is able to identify a chemical, it goes into an identification state. During this state, the device will send seven messages while it runs it's algorithm to improve it's results. If you plan on storing results in your application, this would be the time to do so. The last "identification" message is the one you want to store. The response during this state is as follows:

```json
{
  "data": {
    "mixtureAnalysis": [
      {
        "casNumber": "67-64-1",
        "concentration": 648.0,
        "confidence": 4,
        "ghs": [],
        "idlh": "2",
        "ipcf": "",
        "isTopHit": true,
        "lel": "4",
        "name": "Isopropyl Alchohol",
        "score": 0.987
      }
    ],
    "currentCoAddCount": 1,
    "date": "",
    "instrumentId": "016ebaee1d000019",
    "locationLat": 41.4155093,
    "locationLon": -73.4240129,
    "maxCoAddCount": 15,
    "compounds": [],
    "name": "",
    "serialNumber": "X00030423A",
    "type": "gas"
  },
  "responseTo": "start_cm",
  "date": "2023-01-31T20:48:05.224256",
  "message": "A chemical has been identified",
  "status": "identification"
}
```

After the device has identified a chemical and the device is still in the gas plume, it goes back into the monitoring state but will continue to include the "data" node in the payload. Once the device exits the plume, it will go back to a monitoring state with no "data" node.  These responses will be as follows:

While still in the plume....

```json
{
  "data": {
    "compounds": [],
    "date": "",
    "instrumentId": "016ebaee1d000019",
    "locationLat": null,
    "locationLon": null,
    "mixtureAnalysis": [
      {
        "casNumber": "67-64-1",
        "concentration": 648.0,
        "confidence": 3,
        "ghs": [],
        "idlh": "2",
        "ipcf": "",
        "isTopHit": true,
        "lel": "4",
        "name": "Isopropyl Alchohol",
        "score": 0.987
      }
    ],
    "name": "",
    "serialNumber": "X00030423A",
    "type": "gas"
  },
  "responseTo": "start_cm",
  "date": "2023-01-31T20:47:43.224256",
  "message": "A chemical has been identified",
  "status": "monitoring"
}
```

After exiting the plume...

```json
{  
  "date": "2023-01-31T20:47:43.224256",
  "message": "The device is monitoring. ",
  "responseTo": "start_cm",
  "status": "monitoring"
}
```

Lastly, if the device pumps in too much gas it could go into a saturation state. This state can happen directly after the ready or detection states. The response for this state is as follows:

```json
{  
  "date": "2023-01-31T20:47:43.224256",
  "message": "The device is monitoring. ",
  "responseTo": "start_cm",
  "status": "saturation"
}
```

### <span id="cancel_cm">_cancel_cm_</span>

This command will stop (cancel) a continuous monitoring session.

Request:

```json
{
    "command":"cancel_cm"
}
```

Response:

```json
{
  "responseTo": "cancel_cm",
  "date": "2023-01-31T20:47:43.224256",
  "message": "Cancelled continuous monitoring.",
  "status": "done"
}
```

### <span id="disconnect">disconnect</span>

This command will disconnect the API.

Request:

```json
{
    "command":"disconnect"
}
```

Response:

```json
{
  "response": "Connection successfully terminated."
}
```

<!-- ### <span id="start_background_collection">_start_background_collection_</span>

A single point detection session is a two step process. The `start_background_collection` command is the first command you need to run and will take several minutes to complete. 

```json
{
    "command":"start_background_collection"
}
```

The initial response from this command is as follows:

```json
{
  "responseTo": "start_background_collection",
  "date": "2023-01-31T20:47:43.224256",
  "message": "Successfully started background collection",
  "status": "busy"
}
``` -->

<!-- As the background collection continues, the device will continue to send updates such as the following:

```json
{
  "responseTo": "start_background_collection",
  "date": "2023-01-31T20:47:43.224256",
  "message": "Background collection is 35% complete",
  "status": "busy"
}
```

At the end of this step, the device will respond with the following:

```json
{
  "responseTo": "start_background_collection",
  "date": "2023-01-31T20:47:43.224256",
  "message": "Successfully completed background collection",
  "status": "done"
}
``` -->

<!-- Once you receive this response, you can send the `start_sample_collection` command. -->

<!-- ### <span id="start_sample_collection">_start_sample_collection_</span>

The following command will start a single point sample collection. This command can only be called after the `start_background_collection` command has been run in its entirety.

```json
{
    "command":"start_sample_collection"
}
``` -->

<!-- As the sample collection continues, the device will continually to send messages like the following:

```json
{
  "responseTo": "start_sample_collection",
  "date": "2023-01-31T20:47:43.224256",
  "message": "Sample collection is 20% complete",
  "status": "busy"
}
```

Once complete, you'll receive the following response:

```json
{
  "responseTo": "start_sample_collection",
  "date": "2023-01-31T20:47:43.224256",
  "message": "Successfully completed sample collection",
  "status": "done"
}
``` -->

<!-- ### <span id="cancel_spd">_cancel_spd_</span>

The following command will cancel a single point detection session.

```json
{
    "command":"cancel_spd"
}
```

The response from this command is as follows:

```json
{
  "responseTo": "cancel_spd",
  "date": "2023-01-31T20:47:43.224256",
  "message": "Cancelled background collection",
  "status": "done"
}
``` -->

### <span id="get_sessions">_get_sessions_</span>

The following command will return a list of sessions on the device.

```json
{
  "command": "get_sessions",
  "args": {"limit": 10, "offset": 0}
}
```

The response from this command is as follows:

```json
{
  "data": {
    "sessions": [
      {
        "date": "2024-05-03T11:38:47.00000Z",
        "name": "2024-05-03/C-11-38-47",
        "sampleCount": 1,
        "samples": [
          {
            "date": "2024-05-03T15:43:32.00000Z",
            "hitCount": 1,
            "hits": [
              {
                "casNumber": "75-09-2",
                "name": "Dichloromethane",
                "score": 0.998602
              }
            ],
            "locationLat": null,
            "locationLon": null,
            "name": "2024-05-03/C-11-38-47/11-43-32"
          }
        ],
        "type": "cm"
      },
      {
        "date": "2024-05-01T09:49:43.00000Z",
        "name": "2024-05-01/C-09-49-43",
        "sampleCount": 0,
        "samples": [],
        "type": "cm"
      }
    ]
  },
  "date": "2024-05-13T11:38:59.00000Z",
  "message": "Successfully retrieved sessions",
  "responseTo": "get_sessions",
  "serialNumber": "X01530523D",
  "status": "done"
}
```
### <span id="get_session">_get_session_</span>

The following command will return a list of sessions on the device.  The "name" argument is the name of the sessions which you can get by running the _get_sessions_ command (see example above)

```json
{
    "command": "get_session",
    "args": {
      "name": "2023-11-09/C-19-02-02"
    }
}
```

The response from this command is as follows:

```json
{
  "data": {
    "samples": [
      {
        "date": "2024-04-15T14:56:51.00000Z",
        "hitCount": 4,
        "hits": [
          {"casNumber": "108-88-3", "name": "Toluene", "score": 0.994152},
          {"casNumber": "67-63-0", "name": "2-propanol", "score": 0.985039},
          {"casNumber": "67-64-1", "name": "Acetone", "score": 0.982767},
          {"casNumber": "67-56-1", "name": "Methanol", "score": 0.86013}
        ],
        "locationLat": null,
        "locationLon": null,
        "name": "2024-04-15/C-10-36-32/10-56-51"
      }
    ],
    "type": "cm"
  },
  "date": "2024-05-13T09:12:01.00000Z",
  "message": "Successfully retrieved session",
  "responseTo": "get_session",
  "serialNumber": "X01530523D",
  "status": "done"
}
```

### <span id="get_sample">_get_sample_</span>

The following command will return a specific sample:

```json
{
  "command": "get_sample",
  "args": {
    "name": "2024-04-15/C-10-36-32/10-56-51",
    "spectral_data": "raw",
}
```

The response from this command is as follows:

```json
{
  "data": {
    "compounds": [],
    "date": "",
    "instrumentId": "01bd5b411b000071",
    "locationLat": null,
    "locationLon": null,
    "mixtureAnalysis": [
      {
        "casNumber": "64-17-5",
        "confidence": 5,
        "ghs": [
          {"code": "GHS02", "isHazard": true, "name": "Flammable"},
          {"code": "GHS07", "isHazard": true, "name": "Harmful"},
          {"code": "GHS08", "isHazard": true, "name": "Health Hazard"}
        ],
        "idlh": "3300 ppm",
        "ipcf": "10.47 eV, 9.6x",
        "isTopHit": true,
        "lel": "3.3%",
        "name": "Ethanol",
        "score": 99.3
      }
    ],
    "name": "2023-07-28/C-17-43-00/17-51-49",
    "spectra": {
      "end": 4000,
      "points": 1676,
      "start": 650,
      "values": [
        0.134184,
        0.0,
        0.138669,
        0.385678,
        0.458317,
        0.530608,
        0.401532,
        0.446773,
        0.601015,
        0.693834,
        0.580019,
        0.513711,
        0.469705,
        0.393857,
        0.342327,
        0.460241,
        0.485476,
        0.403392,
        0.452047,
        0.414825,
        0.330107,
        0.359497,
        0.299904,
        0.325256,
        0.397646,
        0.471238,
        0.502461,
        0.505682,
        0.5021,
        0.482856,
        0.457614,
        0.47217,
        0.526782,
        0.489077,
        0.463152,
        0.471346,
        0.424265,
        0.450343,
        0.44962,
        0.432663,
        0.403286,
        0.416528,
        0.400003,
        0.42275,
        0.460819,
        0.42171,
        0.402313,
        0.461526,
        0.469975,
        0.390246,
        0.427508,
        0.466459,
        0.432857,
        0.413127,
        0.427568,
        0.458364,
        0.429905,
        0.412834,
        0.438207,
        0.43139,
        0.442662,
        0.46193,
        0.444695,
        0.443337,
        0.448059,
        0.43928,
        0.434315,
        0.438454,
        0.42657,
        0.401664,
        0.374505,
        0.39281,
        0.46449,
        0.473179,
        0.459085,
        0.461446,
        0.452798,
        0.44629,
        0.443802,
        0.449839,
        0.424068,
        0.407097,
        0.412171,
        0.43172,
        0.441939,
        0.436762,
        0.450969,
        0.427564,
        0.411398,
        0.429604,
        0.424179,
        0.435422,
        0.427221,
        0.394063,
        0.410832,
        0.450723,
        0.468615,
        0.436858,
        0.424243,
        0.469583,
        0.469527,
        0.420798,
        0.446745,
        0.462083,
        0.448156,
        0.450049,
        0.455425,
        0.47361,
        0.500874,
        0.490254,
        0.499849,
        0.515476,
        0.498426,
        0.491675,
        0.508736,
        0.510044,
        0.502151,
        0.512739,
        0.520603,
        0.534795,
        0.541921,
        0.517813,
        0.487238,
        0.496112,
        0.513367,
        0.496934,
        0.489313,
        0.503047,
        0.501169,
        0.468575,
        0.449426,
        0.452759,
        0.460393,
        0.437247,
        0.439403,
        0.458072,
        0.449304,
        0.445729,
        0.444714,
        0.448588,
        0.445755,
        0.432934,
        0.431234,
        0.430025,
        0.425778,
        0.430391,
        0.439827,
        0.455588,
        0.448079,
        0.440066,
        0.450562,
        0.450616,
        0.441483,
        0.437637,
        0.436143,
        0.434569,
        0.431252,
        0.423241,
        0.428899,
        0.439257,
        0.442263,
        0.443773,
        0.444624,
        0.451818,
        0.446883,
        0.437642,
        0.452491,
        0.45982,
        0.43567,
        0.439416,
        0.461243,
        0.448406,
        0.458257,
        0.481673,
        0.499465,
        0.511655,
        0.513863,
        0.528278,
        0.545428,
        0.544891,
        0.547908,
        0.567307,
        0.583053,
        0.589887,
        0.602822,
        0.614339,
        0.622567,
        0.620056,
        0.6631,
        0.712055,
        0.681152,
        0.680929,
        0.718301,
        0.763857,
        0.815146,
        0.839475,
        0.866544,
        0.896168,
        0.911256,
        0.931258,
        0.940352,
        0.946963,
        0.953316,
        0.960674,
        0.964877,
        0.921429,
        0.88301,
        0.929934,
        1.0,
        0.96159,
        0.914517,
        0.923677,
        0.926889,
        0.933614,
        0.921251,
        0.898401,
        0.862637,
        0.830346,
        0.801815,
        0.764138,
        0.724887,
        0.681798,
        0.656593,
        0.639454,
        0.625647,
        0.617276,
        0.618245,
        0.602944,
        0.580734,
        0.560606,
        0.550311,
        0.532877,
        0.509437,
        0.499845,
        0.50244,
        0.507142,
        0.501024,
        0.486315,
        0.477589,
        0.474197,
        0.475926,
        0.47339,
        0.463671,
        0.456407,
        0.458526,
        0.457859,
        0.453336,
        0.441718,
        0.444062,
        0.447559,
        0.442247,
        0.44988,
        0.456744,
        0.451746,
        0.442253,
        0.448727,
        0.457458,
        0.436243,
        0.432751,
        0.448791,
        0.455206,
        0.452865,
        0.454771,
        0.460765,
        0.449804,
        0.444322,
        0.456371,
        0.45475,
        0.450677,
        0.45682,
        0.464071,
        0.454539,
        0.451092,
        0.461474,
        0.467149,
        0.466218,
        0.468741,
        0.472068,
        0.479058,
        0.484219,
        0.488409,
        0.503623,
        0.503205,
        0.506312,
        0.52307,
        0.534131,
        0.539278,
        0.548529,
        0.555096,
        0.571014,
        0.581355,
        0.569441,
        0.544111,
        0.543998,
        0.546237,
        0.557813,
        0.577646,
        0.552173,
        0.552958,
        0.576977,
        0.575772,
        0.560599,
        0.556325,
        0.549569,
        0.548448,
        0.545964,
        0.544767,
        0.538062,
        0.520077,
        0.511261,
        0.51108,
        0.498557,
        0.493134,
        0.49759,
        0.495474,
        0.481898,
        0.465473,
        0.467248,
        0.459981,
        0.452121,
        0.457068,
        0.464562,
        0.476899,
        0.475292,
        0.452237,
        0.445143,
        0.455909,
        0.462107,
        0.464064,
        0.452907,
        0.454675,
        0.471552,
        0.462406,
        0.458751,
        0.464648,
        0.472992,
        0.478745,
        0.476265,
        0.46387,
        0.453114,
        0.446422,
        0.435815,
        0.440704,
        0.462213,
        0.485093,
        0.47987,
        0.449326,
        0.448125,
        0.453823,
        0.477241,
        0.482453,
        0.489997,
        0.49433,
        0.485931,
        0.502906,
        0.50064,
        0.495369,
        0.508321,
        0.515997,
        0.527968,
        0.535221,
        0.540134,
        0.545993,
        0.557189,
        0.582565,
        0.599762,
        0.595707,
        0.600053,
        0.61021,
        0.60437,
        0.587134,
        0.623969,
        0.688349,
        0.6238,
        0.582538,
        0.597608,
        0.598099,
        0.61787,
        0.627153,
        0.632034,
        0.629156,
        0.625667,
        0.604771,
        0.57993,
        0.590261,
        0.575745,
        0.528511,
        0.509145,
        0.506216,
        0.497072,
        0.504594,
        0.50338,
        0.495611,
        0.514661,
        0.496596,
        0.4967,
        0.49124,
        0.469162,
        0.481592,
        0.490031,
        0.494868,
        0.49755,
        0.506599,
        0.522846,
        0.531721,
        0.518471,
        0.481271,
        0.47248,
        0.501485,
        0.483033,
        0.479564,
        0.511662,
        0.502975,
        0.456444,
        0.450206,
        0.48333,
        0.472398,
        0.465842,
        0.491945,
        0.525672,
        0.532073,
        0.477221,
        0.478505,
        0.490781,
        0.467965,
        0.442854,
        0.452386,
        0.468792,
        0.456871,
        0.456089,
        0.477975,
        0.474721,
        0.480078,
        0.508299,
        0.501738,
        0.486022,
        0.471426,
        0.478415,
        0.489652,
        0.486287,
        0.456013,
        0.454128,
        0.473118,
        0.462799,
        0.484044,
        0.492022,
        0.477037,
        0.514702,
        0.481123,
        0.473392,
        0.46231,
        0.450853,
        0.462732,
        0.490127,
        0.576402,
        0.544451,
        0.467794,
        0.467566,
        0.447407,
        0.444677,
        0.429325,
        0.419085,
        0.445499,
        0.458043,
        0.449999,
        0.447237,
        0.442162,
        0.426429,
        0.413715,
        0.417644,
        0.423516,
        0.433303,
        0.455949,
        0.446643,
        0.418316,
        0.413244,
        0.430441,
        0.438758,
        0.417456,
        0.435848,
        0.454691,
        0.435351,
        0.440508,
        0.45435,
        0.440651,
        0.438346,
        0.429975,
        0.412846,
        0.434475,
        0.429771,
        0.417555,
        0.427444,
        0.444951,
        0.452473,
        0.440459,
        0.448991,
        0.458109,
        0.452624,
        0.455539,
        0.486793,
        0.453274,
        0.439155,
        0.454123,
        0.491617,
        0.462371,
        0.434482,
        0.46483,
        0.465592,
        0.447997,
        0.444811,
        0.45298,
        0.449834,
        0.448841,
        0.470503,
        0.482654,
        0.463338,
        0.478193,
        0.583327,
        0.50942,
        0.450781,
        0.435403,
        0.441124,
        0.468296,
        0.471126,
        0.493564,
        0.536453,
        0.500318,
        0.477564,
        0.458109,
        0.45032,
        0.42882,
        0.447147,
        0.473552,
        0.481387,
        0.472046,
        0.453524,
        0.442326,
        0.430296,
        0.430191,
        0.433671,
        0.460863,
        0.501949,
        0.498579,
        0.463367,
        0.463628,
        0.460757,
        0.468325,
        0.464742,
        0.456033,
        0.444639,
        0.445358,
        0.424242,
        0.425022,
        0.442067,
        0.44338,
        0.460128,
        0.455007,
        0.450991,
        0.451477,
        0.436166,
        0.450525,
        0.457905,
        0.439207,
        0.444368,
        0.445901,
        0.456779,
        0.437774,
        0.430768,
        0.426908,
        0.420811,
        0.440675,
        0.463608,
        0.454088,
        0.434072,
        0.419324,
        0.437985,
        0.433858,
        0.429444,
        0.433302,
        0.437051,
        0.447088,
        0.439572,
        0.438238,
        0.434915,
        0.434329,
        0.430041,
        0.421886,
        0.432298,
        0.428372,
        0.434879,
        0.451649,
        0.447874,
        0.434941,
        0.418398,
        0.431123,
        0.443036,
        0.456859,
        0.461727,
        0.45096,
        0.44081,
        0.426658,
        0.432365,
        0.428031,
        0.430455,
        0.428561,
        0.441359,
        0.441474,
        0.429736,
        0.437899,
        0.450064,
        0.433373,
        0.421709,
        0.426413,
        0.420007,
        0.410934,
        0.417513,
        0.432429,
        0.453496,
        0.441797,
        0.428655,
        0.431385,
        0.422118,
        0.427459,
        0.433993,
        0.439857,
        0.435774,
        0.435186,
        0.430426,
        0.429565,
        0.425903,
        0.415835,
        0.421601,
        0.425976,
        0.429259,
        0.437939,
        0.440473,
        0.439092,
        0.445267,
        0.453298,
        0.425919,
        0.427715,
        0.447475,
        0.437586,
        0.425977,
        0.430765,
        0.439508,
        0.42833,
        0.42557,
        0.452652,
        0.443325,
        0.430519,
        0.436433,
        0.424374,
        0.418642,
        0.415575,
        0.409159,
        0.413833,
        0.422185,
        0.432603,
        0.44597,
        0.448791,
        0.426395,
        0.422386,
        0.427873,
        0.425991,
        0.436689,
        0.435286,
        0.424448,
        0.432723,
        0.439373,
        0.436261,
        0.435439,
        0.428891,
        0.432077,
        0.430931,
        0.429059,
        0.431727,
        0.441816,
        0.433943,
        0.426686,
        0.449762,
        0.454298,
        0.435703,
        0.427776,
        0.434359,
        0.445084,
        0.44411,
        0.442222,
        0.436513,
        0.44048,
        0.448529,
        0.440765,
        0.431762,
        0.426348,
        0.414636,
        0.417382,
        0.426735,
        0.417587,
        0.416464,
        0.423392,
        0.442893,
        0.434597,
        0.420874,
        0.420548,
        0.416453,
        0.403904,
        0.416698,
        0.443549,
        0.433429,
        0.425896,
        0.433266,
        0.428914,
        0.421095,
        0.421838,
        0.430655,
        0.429684,
        0.429629,
        0.439112,
        0.444716,
        0.439643,
        0.432321,
        0.431966,
        0.430685,
        0.422227,
        0.414896,
        0.415994,
        0.422382,
        0.421729,
        0.4158,
        0.416416,
        0.427166,
        0.424984,
        0.42142,
        0.426964,
        0.414563,
        0.412466,
        0.423391,
        0.441479,
        0.446574,
        0.429482,
        0.426621,
        0.418317,
        0.421856,
        0.443389,
        0.447703,
        0.423533,
        0.42351,
        0.44195,
        0.424381,
        0.415366,
        0.420753,
        0.42347,
        0.429255,
        0.416041,
        0.419084,
        0.428941,
        0.432509,
        0.433464,
        0.43185,
        0.432698,
        0.428691,
        0.432736,
        0.433741,
        0.406055,
        0.417645,
        0.452812,
        0.455776,
        0.440177,
        0.436938,
        0.443417,
        0.440674,
        0.435334,
        0.438647,
        0.422744,
        0.414039,
        0.427199,
        0.431102,
        0.421605,
        0.398526,
        0.413291,
        0.414235,
        0.406909,
        0.425482,
        0.438925,
        0.437539,
        0.435204,
        0.42175,
        0.412751,
        0.427335,
        0.434275,
        0.436019,
        0.428656,
        0.418193,
        0.436547,
        0.436517,
        0.408281,
        0.409702,
        0.415712,
        0.426162,
        0.4513,
        0.437431,
        0.427517,
        0.437747,
        0.450307,
        0.450852,
        0.44931,
        0.430873,
        0.421772,
        0.435934,
        0.459257,
        0.458027,
        0.447099,
        0.449119,
        0.452023,
        0.44513,
        0.436083,
        0.432296,
        0.424426,
        0.429629,
        0.446569,
        0.460467,
        0.445436,
        0.441776,
        0.460714,
        0.436846,
        0.409354,
        0.414245,
        0.421777,
        0.40938,
        0.433952,
        0.475616,
        0.422059,
        0.419672,
        0.498717,
        0.489163,
        0.47315,
        0.553628,
        0.521884,
        0.580018,
        0.691415,
        0.588284,
        0.522694,
        0.521292,
        0.4595,
        0.55791,
        0.623768,
        0.487837,
        0.528097,
        0.574183,
        0.516164,
        0.464825,
        0.421758,
        0.571566,
        0.569024,
        0.613973,
        0.744541,
        0.602116,
        0.480914,
        0.552801,
        0.831684,
        0.744146,
        0.588173,
        0.558691,
        0.488069,
        0.470668,
        0.473728,
        0.468601,
        0.451075,
        0.426156,
        0.419371,
        0.424194,
        0.435548,
        0.437461,
        0.432314,
        0.448688,
        0.447455,
        0.418354,
        0.433768,
        0.453823,
        0.43028,
        0.41102,
        0.408906,
        0.415811,
        0.434433,
        0.436051,
        0.438062,
        0.425475,
        0.42169,
        0.41136,
        0.405677,
        0.422549,
        0.425757,
        0.420666,
        0.436164,
        0.427723,
        0.435129,
        0.456037,
        0.440984,
        0.427915,
        0.42786,
        0.423626,
        0.435727,
        0.432089,
        0.418137,
        0.424457,
        0.414331,
        0.413866,
        0.422009,
        0.43647,
        0.444112,
        0.444678,
        0.444098,
        0.42094,
        0.402242,
        0.420631,
        0.438953,
        0.409816,
        0.405899,
        0.415497,
        0.383989,
        0.383485,
        0.403793,
        0.416274,
        0.426246,
        0.434361,
        0.427411,
        0.413583,
        0.413911,
        0.429272,
        0.408019,
        0.398405,
        0.41026,
        0.404057,
        0.415052,
        0.431906,
        0.432814,
        0.420535,
        0.409976,
        0.430016,
        0.442817,
        0.447401,
        0.445269,
        0.42004,
        0.418705,
        0.415331,
        0.409752,
        0.432857,
        0.44681,
        0.444212,
        0.435471,
        0.42204,
        0.421772,
        0.445247,
        0.442462,
        0.441652,
        0.443248,
        0.440753,
        0.43322,
        0.40509,
        0.423846,
        0.431242,
        0.429554,
        0.447052,
        0.451225,
        0.430457,
        0.414348,
        0.405014,
        0.420206,
        0.423099,
        0.412061,
        0.42854,
        0.465463,
        0.461001,
        0.440151,
        0.448589,
        0.452202,
        0.45369,
        0.457249,
        0.453399,
        0.470808,
        0.495221,
        0.474001,
        0.433745,
        0.398596,
        0.405318,
        0.431477,
        0.433567,
        0.431541,
        0.419913,
        0.417417,
        0.427284,
        0.438085,
        0.419367,
        0.422787,
        0.451116,
        0.445656,
        0.455589,
        0.460614,
        0.438646,
        0.456415,
        0.484806,
        0.450204,
        0.453802,
        0.435747,
        0.402367,
        0.420551,
        0.437524,
        0.41185,
        0.414352,
        0.456843,
        0.466523,
        0.461765,
        0.436518,
        0.412971,
        0.456952,
        0.450048,
        0.439371,
        0.467659,
        0.446117,
        0.43165,
        0.413384,
        0.394121,
        0.426988,
        0.450257,
        0.469772,
        0.475528,
        0.443704,
        0.423912,
        0.42787,
        0.424836,
        0.458065,
        0.480353,
        0.427983,
        0.402731,
        0.435163,
        0.445349,
        0.437916,
        0.452802,
        0.448262,
        0.476556,
        0.486459,
        0.439964,
        0.439647,
        0.453096,
        0.458473,
        0.46487,
        0.457761,
        0.44163,
        0.443905,
        0.44266,
        0.448704,
        0.428341,
        0.42463,
        0.448596,
        0.454354,
        0.456971,
        0.426742,
        0.432935,
        0.473961,
        0.458804,
        0.447101,
        0.44641,
        0.432696,
        0.41584,
        0.411541,
        0.451426,
        0.455327,
        0.440209,
        0.456672,
        0.451394,
        0.466102,
        0.44976,
        0.440647,
        0.457678,
        0.462869,
        0.45828,
        0.460656,
        0.446864,
        0.453963,
        0.484323,
        0.472646,
        0.457735,
        0.4487,
        0.458905,
        0.466266,
        0.444688,
        0.429143,
        0.448324,
        0.481098,
        0.451049,
        0.463851,
        0.471932,
        0.480239,
        0.501071,
        0.491322,
        0.490521,
        0.494997,
        0.549053,
        0.575813,
        0.546765,
        0.554707,
        0.579685,
        0.595609,
        0.597294,
        0.594775,
        0.614806,
        0.620258,
        0.620564,
        0.635359,
        0.634686,
        0.610687,
        0.658461,
        0.671349,
        0.666079,
        0.685682,
        0.681771,
        0.723013,
        0.714491,
        0.70615,
        0.705543,
        0.711835,
        0.763266,
        0.769584,
        0.734904,
        0.748794,
        0.780529,
        0.820276,
        0.762864,
        0.708016,
        0.76142,
        0.778116,
        0.745014,
        0.747355,
        0.745705,
        0.73754,
        0.758826,
        0.754089,
        0.737334,
        0.736501,
        0.709664,
        0.738452,
        0.759001,
        0.759249,
        0.766439,
        0.738381,
        0.738151,
        0.762048,
        0.744872,
        0.725989,
        0.714943,
        0.738374,
        0.752476,
        0.74697,
        0.768192,
        0.781917,
        0.765275,
        0.788967,
        0.850005,
        0.8256,
        0.831594,
        0.826781,
        0.815397,
        0.839396,
        0.819725,
        0.836473,
        0.891069,
        0.84802,
        0.823589,
        0.869328,
        0.886689,
        0.905777,
        0.856455,
        0.779503,
        0.76248,
        0.780257,
        0.774959,
        0.746811,
        0.72939,
        0.712808,
        0.68624,
        0.639599,
        0.628708,
        0.599563,
        0.584681,
        0.601909,
        0.57018,
        0.530319,
        0.540452,
        0.557341,
        0.525813,
        0.480981,
        0.443667,
        0.429983,
        0.442572,
        0.445918,
        0.42889,
        0.397636,
        0.405952,
        0.43329,
        0.457986,
        0.451035,
        0.42628,
        0.412862,
        0.418016,
        0.442947,
        0.446669,
        0.452835,
        0.46492,
        0.421647,
        0.397842,
        0.416308,
        0.406512,
        0.407048,
        0.417232,
        0.414053,
        0.415044,
        0.423975,
        0.439817,
        0.441667,
        0.455997,
        0.461206,
        0.434788,
        0.391271,
        0.402753,
        0.445048,
        0.438435,
        0.449121,
        0.449143,
        0.432417,
        0.402562,
        0.398658,
        0.409964,
        0.428218,
        0.451809,
        0.429216,
        0.444741,
        0.438482,
        0.422927,
        0.446031,
        0.442054,
        0.424523,
        0.440115,
        0.471491,
        0.469357,
        0.461868,
        0.456359,
        0.433517,
        0.41493,
        0.430319,
        0.454361,
        0.431747,
        0.415942,
        0.450522,
        0.44525,
        0.431025,
        0.430725,
        0.417131,
        0.435623,
        0.426706,
        0.412799,
        0.432794,
        0.424118,
        0.444924,
        0.456537,
        0.435983,
        0.428111,
        0.406376,
        0.391191,
        0.417935,
        0.439253,
        0.420195,
        0.424408,
        0.430304,
        0.450083,
        0.454553,
        0.442041,
        0.421288,
        0.403617,
        0.418077,
        0.411618,
        0.423941,
        0.44338,
        0.436375,
        0.439244,
        0.427306,
        0.420761,
        0.440277,
        0.450606,
        0.43833,
        0.44137,
        0.460044,
        0.437284,
        0.437218,
        0.423783,
        0.422907,
        0.458506,
        0.434593,
        0.434354,
        0.439699,
        0.422224,
        0.445974,
        0.431556,
        0.413822,
        0.414532,
        0.406344,
        0.434379,
        0.419529,
        0.39058,
        0.423521,
        0.423587,
        0.425765,
        0.427273,
        0.377009,
        0.393803,
        0.418165,
        0.428295,
        0.397424,
        0.409064,
        0.474513,
        0.450364,
        0.403621,
        0.411362,
        0.4558,
        0.453287,
        0.413577,
        0.414205,
        0.44003,
        0.438519,
        0.441036,
        0.416955,
        0.403674,
        0.421986,
        0.424195,
        0.401651,
        0.413789,
        0.435225,
        0.454129,
        0.455184,
        0.450805,
        0.455906,
        0.455055,
        0.446908,
        0.420411,
        0.418819,
        0.456693,
        0.479919,
        0.459811,
        0.422521,
        0.419542,
        0.438149,
        0.430766,
        0.402598,
        0.390406,
        0.38978,
        0.416099,
        0.466947,
        0.431183,
        0.422438,
        0.441111,
        0.437403,
        0.431778,
        0.438371,
        0.463586,
        0.452228,
        0.433368,
        0.400867,
        0.398647,
        0.410907,
        0.393874,
        0.391563,
        0.422289,
        0.41513,
        0.442739,
        0.42965,
        0.405483,
        0.418782,
        0.3776,
        0.366835,
        0.435252,
        0.44377,
        0.421575,
        0.408509,
        0.41866,
        0.414944,
        0.410673,
        0.416958,
        0.434643,
        0.484677,
        0.457412,
        0.439026,
        0.44416,
        0.422317,
        0.370173,
        0.362327,
        0.419426,
        0.443266,
        0.434753,
        0.40283,
        0.398619,
        0.433385,
        0.441076,
        0.438998,
        0.44569,
        0.442771,
        0.434995,
        0.429748,
        0.432921,
        0.413552,
        0.416287,
        0.40737,
        0.403777,
        0.409522,
        0.412272,
        0.434042,
        0.441084,
        0.420002,
        0.410521,
        0.425842,
        0.434611,
        0.468332,
        0.48028,
        0.443161,
        0.440167,
        0.412121,
        0.395443,
        0.395501,
        0.395897,
        0.410983,
        0.402473,
        0.428827,
        0.477487,
        0.48671,
        0.463727,
        0.457287,
        0.402138,
        0.411488,
        0.433681,
        0.45776,
        0.509086,
        0.462961,
        0.494909,
        0.492434,
        0.437861,
        0.424133,
        0.439748,
        0.449464,
        0.448405,
        0.459472,
        0.458312,
        0.409123,
        0.381084,
        0.403279,
        0.460859,
        0.440893,
        0.46326,
        0.488261,
        0.455364,
        0.439274,
        0.460113,
        0.535415,
        0.504113,
        0.445399,
        0.471774,
        0.525855,
        0.473177,
        0.444678,
        0.457055,
        0.442368,
        0.477298,
        0.480611,
        0.481126,
        0.461719,
        0.440098,
        0.430668,
        0.465107,
        0.489063,
        0.422271,
        0.418237,
        0.466618,
        0.515964,
        0.435981,
        0.442107,
        0.480979,
        0.473288,
        0.509614,
        0.472913,
        0.45591,
        0.463397,
        0.468558,
        0.518905,
        0.490572,
        0.431943,
        0.477163,
        0.495128,
        0.484614,
        0.530962,
        0.529891,
        0.512514,
        0.588135,
        0.675441,
        0.57892,
        0.542876,
        0.587523,
        0.607676,
        0.556626,
        0.506436,
        0.5197,
        0.499715,
        0.482115,
        0.492814,
        0.540985,
        0.578211,
        0.555399,
        0.472265,
        0.476833,
        0.520781,
        0.528924,
        0.528236,
        0.482519,
        0.557545,
        0.584538,
        0.531759,
        0.539903,
        0.483385,
        0.473008,
        0.495398,
        0.45563,
        0.414249,
        0.432555,
        0.450514,
        0.431915,
        0.450688,
        0.48179,
        0.449505,
        0.461501,
        0.453947,
        0.476895,
        0.496458,
        0.428656,
        0.424676,
        0.422665,
        0.445568,
        0.549205,
        0.447712,
        0.355525,
        0.470398,
        0.480312,
        0.473458,
        0.36937,
        0.361191,
        0.472171,
        0.604877,
        0.495801,
        0.487543,
        0.451445,
        0.435822,
        0.46622,
        0.427249,
        0.362575,
        0.389836,
        0.426595,
        0.462889,
        0.410685,
        0.389682,
        0.417975,
        0.43028,
        0.461598,
        0.479012,
        0.48078,
        0.492078,
        0.49135,
        0.468266,
        0.439608,
        0.425893,
        0.449401,
        0.449823,
        0.437357,
        0.506263,
        0.452014,
        0.482282,
        0.509065,
        0.468082,
        0.478801,
        0.521772,
        0.50729,
        0.528335,
        0.569741,
        0.500698,
        0.463018,
        0.45963,
        0.447838,
        0.434682,
        0.54895,
        0.604223,
        0.602001,
        0.650374,
        0.532455,
        0.52887,
        0.491479,
        0.473594,
        0.483392,
        0.49476,
        0.545332,
        0.533344,
        0.476242,
        0.401448,
        0.383884,
        0.364201,
        0.358352,
        0.427991,
        0.434205,
        0.472564,
        0.437114,
        0.449295,
        0.503166,
        0.442586,
        0.394729,
        0.425581,
        0.516649,
        0.511039,
        0.438043,
        0.377631,
        0.352908,
        0.462512,
        0.529637,
        0.472026,
        0.455004,
        0.480341,
        0.459421,
        0.444686,
        0.442682,
        0.395412,
        0.421877,
        0.461974,
        0.433314,
        0.445594,
        0.460419,
        0.40996,
        0.355705,
        0.357558,
        0.396484,
        0.505942,
        0.506196,
        0.428764,
        0.389992,
        0.427033,
        0.399044,
        0.363299,
        0.381431,
        0.420314,
        0.462877,
        0.449862,
        0.44295,
        0.373834,
        0.342114,
        0.424422,
        0.513102,
        0.475345,
        0.432267,
        0.424128,
        0.387669,
        0.415768,
        0.428251,
        0.431653,
        0.42737,
        0.443904,
        0.436755,
        0.399876,
        0.440655,
        0.445842,
        0.375038,
        0.433357,
        0.560857,
        0.545115,
        0.466788,
        0.450526
      ]
    },
    "type": "gas"
  },
  "date": "2024-01-10T18:05:57.00000Z",
  "message": "Successfully retrieved sample data",
  "responseTo": "get_sample",
  "serialNumber": "X00030423A",
  "status": "done"
}
```

### <span id="run_validation_background">run_validation_background</span>

Not yet released.

### <span id="run_validation_sample">run_validation_sample</span>

Not yet released.

### <span id="run_advanced_validation">_run_advanced_validation_</span>

Not yet released.

### <span id="get_diagnostics">get_diagnostics</span>

The command is...

```json
{
  "command": "get_diagnostics"
}
```

The response is...

```json
{
  "data": {
    "datasysVersion": 0.0,
    "energy": 0.0,
    "firmware": "0.84",
    "fpga": 25,
    "instrumentVersion": 0.0,
    "laser": "Pass",
    "softwareVersion": "13.09",
    "tecTemperature": 0
  },
  "date": "2024-05-13T08:55:06.00000Z",
  "message": "Successfully retrieved diagnostics",
  "responseTo": "get_diagnostics",
  "serialNumber": "X01530523D",
  "status": "done"
}
```

### <span id="get_validations">get_validations</span>

The command is...

```json
{
  "command": "get_validations"
}
```

The response is...

```json
{
  "data": {
    "tests": [
      {
        "date": "2023-07-21T19:35:13.00000Z",
        "didPass": false,
        "name": "2023-07-21/19-35-13",
        "type": "Regular"
      },
      {
        "date": "2023-07-21T20:48:35.00000Z",
        "didPass": true,
        "name": "2023-07-21/20-48-35",
        "type": "Regular"
      },
      {
        "date": "2023-07-21T20:52:40.00000Z",
        "didPass": true,
        "name": "2023-07-21/20-52-40",
        "type": "Regular"
      },
      {
        "date": "2023-07-21T20:53:36.00000Z",
        "didPass": true,
        "name": "2023-07-21/20-53-36",
        "type": "Advanced"
      }
    ]
  },
  "date": "2023-07-25T14:59:49.00000Z",
  "message": "Successfully retrieved validations",
  "responseTo": "get_validations",
  "serialNumber": "X01530523D",
  "status": "done"
}
```

### <span id="get_validation">_get_validation_</span>

Not yet released.


