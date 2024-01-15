# Unity-Python Connection Modules
These are encapsulated `Python` and `Unity` modules for continuous TCP communication between these.

## Entire Description
Use 
- `PythonSocket` for your `Python` project,
- `UnitySocket` for your `Unity` project.

### Data format
these 2 will send the data with the format below:
```
<s>{json_format_name}!{json}<e>
```

**Don't use:**
- `<s>` or `<e>` either in the `name` nor `json`
- `!` in `name`

The format decoding will get error.

## Python Socket
```
pip install "git+https://github.com/konbraphat51/UnityPythonConnectionModules.git#egg=UnityConnector&subdirectory=PythonSocket"
```
