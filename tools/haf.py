"""Haibara's Architect 0.6 planning CLI. Model output is data, never a shell command."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ENGINE = Path(os.environ.get("HAF_ENGINE_ROOT", ROOT)).resolve()
sys.path.insert(0, str(ENGINE))
import hafusion
if str(ROOT / "hafusion") not in hafusion.__path__:
    hafusion.__path__.insert(0, str(ROOT / "hafusion"))
from hafusion.workflow06 import VERSION, case_command, dispatch_call, import_proposal, load_json, validate_request, verify_run, write_run


def main(argv=None):
    parser = argparse.ArgumentParser(description="Haibara's Architect 0.6 controlled planning workflow")
    parser.add_argument("--version", action="version", version="Haibara's Architect workflow " + VERSION)
    subs = parser.add_subparsers(dest="command", required=True)
    validate = subs.add_parser("validate", help="validate an explicit request without writing files")
    validate.add_argument("request", type=Path)
    plan = subs.add_parser("plan", help="create a new immutable planning run")
    plan.add_argument("request", type=Path)
    plan.add_argument("--runs-root", type=Path, required=True)
    plan.add_argument("--run", required=True)
    demo = subs.add_parser("demo", help="run the bundled small library planning example; no NBT")
    demo.add_argument("--runs-root", type=Path, required=True)
    demo.add_argument("--run", default="demo-001")
    verify = subs.add_parser("verify", help="recheck artifact hashes and replay planning validation")
    verify.add_argument("--runs-root", type=Path, required=True)
    verify.add_argument("--run", required=True)
    proposal = subs.add_parser("import-proposal", help="validate model-proposed modules in a new revision")
    proposal.add_argument("proposal", type=Path)
    proposal.add_argument("--runs-root", type=Path, required=True)
    proposal.add_argument("--parent", required=True)
    proposal.add_argument("--run", required=True)
    dispatch = subs.add_parser("dispatch", help="handle one model-neutral tool-call JSON; host binds paths and parent")
    dispatch.add_argument("call", type=Path)
    dispatch.add_argument("--runs-root", type=Path, required=True)
    dispatch.add_argument("--parent", required=True)
    case = subs.add_parser("build-case", help="show a registered legacy build command; explicit --execute runs it")
    case.add_argument("--case", required=True)
    case.add_argument("--run", required=True)
    case.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            result = validate_request(load_json(args.request))
        elif args.command in ("plan", "demo"):
            source = ROOT / "examples" / "workflow06" / "library-request.json" if args.command == "demo" else args.request
            result = write_run(load_json(source), args.runs_root, args.run)
        elif args.command == "verify":
            result = verify_run(args.runs_root, args.run)
        elif args.command == "import-proposal":
            result = import_proposal(args.runs_root, args.parent, args.run, load_json(args.proposal))
        elif args.command == "dispatch":
            result = dispatch_call(load_json(args.call), args.runs_root, args.parent)
        else:
            command = case_command(ENGINE, args.case, args.run)
            if args.execute:
                return subprocess.run(command, cwd=ENGINE, shell=False).returncode
            result = {"command_argv": command, "execute": False,
                      "note": "Registered case adapter only; this does not consume an arbitrary workflow plan. Add --execute to run."}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, TypeError, KeyError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
