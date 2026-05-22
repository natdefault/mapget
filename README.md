this is a simple minecraft mapping lookup tool

you can input things like field_9989, func_1234, or other mapped/obfuscated names and it will try to return a readable name, class path, type, and some extra info depending on the mapping data.

it supports:
- yarn
- mojmap
- mcp (only older versions, 1.12 and below)
- auto mapping detection
- obfuscated mode (for yarn-style inputs)

## what it does

basically it takes minecraft internal names and tries to turn them into something readable so you can understand what they actually are.

example:

input:
field_9989

output:
resolved name (example: mossy_cobblestone or similar depending on mapping)
class path
type (field/method/class)
version info
extra debug info if available

## how to run

install dependencies:
pip install -r requirements.txt

run the app:
python main.py

## notes

mcp only works for versions it supports (1.12 and below)

first run might take longer because it downloads mapping data and caches it locally

## purpose

this is just a small tool for looking up minecraft mappings. feel free to use it or modify it however you want

## license

licensed under the gnu agpl-3.0 license.