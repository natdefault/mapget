# mapget
**download from releases:** https://github.com/natdefault/mapget/releases
<br>
written by natdefault, 4xnico.

<br>
<img width="720" height="558" alt="mapget_preview" src="https://github.com/user-attachments/assets/87a2e360-5437-4d53-87ed-dcb56cc6e1eb" />
<br>

***

this is a simple minecraft mapping lookup tool

you can input things like field_9989, func_1234, or other mapped/obfuscated names and it will try to return a readable name, class path, type, and some extra info depending on the mapping data.

it supports:
- yarn
- mojmap
- mcp (only older versions, 1.12 and below)
- auto mapping detection
- obfuscated mode (for yarn-style inputs)

## main functions

it takes minecraft internal names and tries to turn them into something readable so you can understand what they actually are.

example:

input:
field_9989

output:
resolved name (example: mossy_cobblestone or similar depending on mapping)
class path
type (field/method/class)
version info
extra debug info if available

## other features
- choose from 5 distinct themes.
- fast cache
- automatic updating to latest version
- pyinstaller support

## how to use
there are two ways of using this program.
#### build with pyinstaller (to .exe)
to build with pyinstaller, you need to use the included build tool.
```
py build.py
```
the .exe file will be ready in the 'dist' directory.
### run with python
install dependencies:
```
pip install -r requirements.txt
```
run the app:
```
python main.py
```

## notes
mcp only works for versions it supports (1.12 and below)
first run might take longer because it downloads mapping data and caches it locally

## license
licensed under the gnu agpl-3.0 license.
