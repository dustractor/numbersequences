from pathlib import Path
from argparse import ArgumentParser
from json import dumps,loads
from copy import deepcopy
from sys import platform,exit
from shutil import copy
home = Path.home()

rack_dir = {
    "win32": home / "AppData" / "Local" / "Rack2",
    "darwin": home / "Library" / "Application Support" / "Rack2",
    "linux": home / ".local" / "share" / "Rack2"
}.get(platform,"unknownplatform")

if rack_dir == "unknownplatform":
    print("rack dir unknown for this platform.")
    exit()

args = ArgumentParser()
args.add_argument("--seq-dir",type=Path,default=home/"Documents"/"GitHub"/"numbersequences")
ns = args.parse_args()

oz_presetsdir = rack_dir / "presets" / "voxglitch" / "onezero"
op_presetsdir = rack_dir / "presets" / "voxglitch" / "onepoint"

# {{{1 json templates
oz_jdata = {
  "plugin": "voxglitch",
  "model": "onezero",
  "version": "2.32.0",
  "params": [
    {
      "value": 0.0,
      "id": 0
    },
    {
      "value": 0.0,
      "id": 1
    },
    {
      "value": 0.0,
      "id": 2
    },
    {
      "value": 1.0,
      "id": 3
    }
  ],
  "data": {
    "path": "placeholder_text"
  }
}
op_jdata = {
  "plugin": "voxglitch",
  "model": "onepoint",
  "version": "2.28.0",
  "params": [
    {
      "value": 0.0,
      "id": 0
    },
    {
      "value": 0.0,
      "id": 1
    },
    {
      "value": 0.0,
      "id": 2
    },
    {
      "value": 1.0,
      "id": 3
    }
  ],
  "data": {
    "path": "placeholder_text"
  }
}
# }}}1

gates_files = list((ns.seq_dir / "for_onezero").glob("**/*.txt"))
notes_files = list((ns.seq_dir / "for_onepoint").glob("**/*.txt"))


for file in gates_files:
    presetpath = (oz_presetsdir / file.relative_to(ns.seq_dir/"for_onezero")).with_suffix(".vcvm")
    presetpath.parent.mkdir(parents=True,exist_ok=True)
    jd = deepcopy(oz_jdata)
    jd["data"]["path"] = str(file)
    with open(presetpath,"w",encoding="utf-8") as f:
        f.write(dumps(jd))

for file in notes_files:
    presetpath = (op_presetsdir / file.relative_to(ns.seq_dir/"for_onepoint")).with_suffix(".vcvm")
    presetpath.parent.mkdir(parents=True,exist_ok=True)
    jd = deepcopy(op_jdata)
    jd["data"]["path"] = str(file)
    with open(presetpath,"w",encoding="utf-8") as f:
        f.write(dumps(jd))

