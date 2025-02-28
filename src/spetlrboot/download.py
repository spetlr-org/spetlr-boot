import json
import os
import sys
from pathlib import Path

from pip._internal.cli.main import main as pip_main

from spetlrboot.arguments import DEPENDENCIES, REQUIREMENTS, unpack_argv
from spetlrboot.libraries import keep_new, pipfreeze2dict


def download():
    params = unpack_argv()
    dependencies = params.pop(DEPENDENCIES)
    raw_requirements = params.pop(REQUIREMENTS)
    requirements = [r.strip() for r in json.loads(raw_requirements) if r.strip()]

    if "*" in dependencies:
        dependencies = str(Path(dependencies).parent)

    print("Specified requirements:")
    for r in requirements:
        print(" -", r)
    print()
    print("Specified download directory:")
    print(dependencies)
    print()

    print("Now establishing baseline packages that are already installed.")
    print("The will not be downloaded in dependencies folder.")
    default_libs = pipfreeze2dict()

    print("Ensuring download destination exists...")
    Path(dependencies).mkdir(parents=True, exist_ok=True)

    print("Ensuring that specified download directory is empty...")
    if len(os.listdir(dependencies)) != 0:
        print("ERROR: the download directory is not empty.")
        sys.exit(1)

    pip_main(["install", "--no-deps"] + requirements)

    all_libs = pipfreeze2dict()
    lib_dependencies = keep_new(all_libs, default_libs)

    print("Identified packages for download:")
    lib_specs = []
    for lib, version in lib_dependencies.items():
        spec = f"{lib}=={version}"
        print("  ", spec)
        lib_specs.append(spec)

    if not lib_specs:
        print("ERROR: No packages for download.")
        sys.exit(1)

    print("Now downloading all from pypi...")

    os.chdir(dependencies)
    pip_main(["download"] + lib_specs)

    print("All done.")
