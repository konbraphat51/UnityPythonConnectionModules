# [Unity-Python Connection Modules](https://github.com/konbraphat51/UnityPythonConnectionModules)

These are encapsulated `Python` and `Unity` modules for continuous TCP communication between these.

## Entire Description
Use 
- `PythonSocket` for your `Python` project,
- `UnitySocket` for your `Unity` project.

`PythonSocket` is a server and `UnitySocket` is the client.  
Ignite `PythonSocket` **before** the `UnityScoket`

### Data format
#### Usual Data
these 2 will send the data to each other in the format below:
```
<s>{json_format_name}!{json}<e>
```

**Don't use:**
- `<s>` or `<e>` either in the `name` or `json`
- `!` in `name`

The format decoding will get an error.

#### Quit code
If either `Python` or `Unity` quits the connection. They will send a quit code `end!`

## Python Socket
### Installation
```
pip install "git+https://github.com/konbraphat51/UnityPythonConnectionModules.git#egg=UnityConnector&subdirectory=PythonSocket"
```

### How to code
You can observe [`ManualTester.py`](https://github.com/konbraphat51/UnityPythonConnectionModules/blob/main/PythonSocket/tests/ManualTester.py) for running example.

#### Brief Description
Use `UnityConnector`
```Python
from UnityConnector import UnityConnector
```

- `UnityConnector.start_listening()`   
  Ignite the `Python` server.  
  This will block until `Unity` is connected
  **When data is received,** the callback will be invoked.

- `UnityConnector.send(string, dict)`  
  Send JSON data to `Unity`

- `UnityConnector.stop_connection()`  
  Stop the connection and send **quit code** to `Unity`

#### Making callbacks
Make 3 callbacks:
- data received.
  Called when received data from another one.  
  2 params given: data_format_name(str) and data json(dict)
- timeout  
  Called when the connection failed.
  No params given
- quit  
  Called when `Unity` sent a quit code.
  No params given

## Unity Socket
### Installation
Put
- [`DataDecoder.cs`](https://github.com/konbraphat51/UnityPythonConnectionModules/blob/main/UnitySocket/Assets/Scripts/DataDecoder.cs)
- [`DataClass.cs`](https://github.com/konbraphat51/UnityPythonConnectionModules/blob/main/UnitySocket/Assets/Scripts/DataClass.cs)
- [`PythonConnector.cs`](https://github.com/konbraphat51/UnityPythonConnectionModules/blob/main/UnitySocket/Assets/Scripts/PythonConnector.cs)

to your `Unity` project.


Make
- Subclasses of `DataClass` for each of your data formats. [[Example]](https://github.com/konbraphat51/UnityPythonConnectionModules/blob/main/UnitySocket/Assets/Scripts/Test/TestDataClass.cs)
- A subclass of `DataDecoder` and **just override** `DataToType()` [[Example]](https://github.com/konbraphat51/UnityPythonConnectionModules/blob/main/UnitySocket/Assets/Scripts/Test/TestDecoder.cs)

and attach
- `PythonConnector`
- your inherited `DataDecoder`

to an `UnityObject` (anything OK, even a empty class)

#### Brief Description
You can observe [`ConnectionTest.cs`](https://github.com/konbraphat51/UnityPythonConnectionModules/blob/main/UnitySocket/Assets/Scripts/Test/ConnectionTest.cs)

- `PythonConnector.instance.RegisterAction(type, function)`  
  Register callback corresponds to the `type`
  `type` is `DataClass`

- `PythonConnector.instance.StartConnection()`  
  Starting connection with `Python`
  Call this **after** `Python` started.

- `PythonConnector.instance.Send(string, DataClass)`  
  Send data to `Python`
  Give data format name and dataclass (automatically converted into JSON if you use `Serialize`)

- `PythonConnector.instance.StopConnection()`  
  Send quit code to `Python` and stop connection.
