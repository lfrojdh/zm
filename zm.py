#!/usr/bin/python3

import os
import sys
import argparse
import pickle
import subprocess


def build(db, target, components):
    if target and components:
        if any(
            map(
                lambda component: os.path.isfile(component)
                and os.path.isfile(target)
                and os.stat(component).st_mtime > os.stat(target).st_mtime
                or not os.path.isfile(target),
                components.split(" "),
            )
        ):

            run(db[(target, components)])


def run(cmd):
    print("zm: " + cmd)
    return subprocess.run(cmd, shell=True).returncode == 0


if __name__ == "__main__":

    db = {}  # [("target", ["component"])] = "buildrule"

    CC = os.getenv("CC") and os.getenv("CC") or "gcc"

    parser = argparse.ArgumentParser()

    parser.add_argument("--clean", help="remove object files", action="store_true")
    parser.add_argument("--build", help="build", action="store_true")
    parser.add_argument("--purge", help="removed all stored data", action="store_true")
    parser.add_argument(
        "--make", help="generate template makefile", action="store_true"
    )

    args, unknown = parser.parse_known_args()

    args.build = args.build or len(sys.argv) == 1

    if os.path.isfile(".zm.pickle"):
        db = pickle.load(open(".zm.pickle", "rb"))

    if args.clean:
        for (target, component) in db:
            if target:
                print("rm " + target)
                try:
                    os.remove(target)
                except:
                    pass
        sys.exit(0)

    if args.purge:
        db = {}
        print("rm .zm.pickle")
        os.remove(".zm.pickle")
        sys.exit(0)

    if args.make:
        for (component, target) in db:
            print(component + ":\t" + target)
            print("\t" + db[(component, target)])
            print("")
        sys.exit(0)

    if args.build:

        if not len(db):
            print("zm: no build rules added")

        for (target, components) in db:
            build(db, target, components)

        sys.exit(0)

    # default execute and store buildrule
    if not run(CC + " " + " ".join(sys.argv[1:])):
        sys.exit(1)

    component = ""
    target = ""

    try:
        i = sys.argv.index("-c")
        if os.path.isfile(sys.argv[i + 1]):
            component = sys.argv[i + 1]
    except:
        pass

    try:
        i = sys.argv.index("-o")
        if os.path.isfile(sys.argv[i + 1]):
            target = sys.argv[i + 1]
    except:
        pass

    # implicit target
    if component and not target and component.endswith(".c"):
        target = component.replace(".c", ".o")

    # implicit a.out target (link target)
    if not component and not target:
        component = " ".join(
            list(filter(lambda x: x.endswith(".o") and os.path.isfile(x), sys.argv[1:]))
        )
        target = "a.out"

    db[(target, component)] = " ".join([CC] + sys.argv[1:])

    if db:
        pickle.dump(db, open(".zm.pickle", "wb"))
