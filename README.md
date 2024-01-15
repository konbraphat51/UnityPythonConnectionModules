# Unity-Python Connection Modules
These are encapsulated `Python` and `Unity` modules for continuous TCP communication between these.

## Entire Description
Use 
- `PythonSocket` for your `Python` project,
- `UnitySocket` for your `Unity` project.

### Data format
#### Usual Data
these 2 will send to the data to each other with the format below:
```
<s>{json_format_name}!{json}<e>
```

**Don't use:**
- `<s>` or `<e>` either in the `name` nor `json`
- `!` in `name`

The format decoding will get error.

#### Quit code
If either `Python` or `Unity` quit connection. They will send a quit code `end!`

## Python Socket
### Instalation
```
pip install "git+https://github.com/konbraphat51/UnityPythonConnectionModules.git#egg=UnityConnector&subdirectory=PythonSocket"
```

### How to code
You can observe [`ManualTester.py`](https://github.com/konbraphat51/UnityPythonConnectionModules/blob/main/PythonSocket/tests/ManualTester.py) for running example.

#### Making callbacks
Make 3 callbacks:
- data received.
  Called when received data from another one.
  2 params
- timeout  
  Called when the connection failed.
  No params given
- quit  
  Called when `Unity` sent a quit code.
  No params given

