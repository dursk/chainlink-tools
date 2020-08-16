import argparse
import requests
import sys

from .constants import Subcommand
from . import api, scripts


def create_subparser(subparsers, subcommand, func, **kwargs):
    args_validator = kwargs.pop("args_validator", None)

    subparser = subparsers.add_parser(subcommand, **kwargs)

    subparser.set_defaults(func=func, args_validator=args_validator)
    subparser.add_argument(
        "--credentials",
        required=True,
        help="Path to credentials file. This file should be similar to the .api file for the node. First line: username, second line: password",
    )
    subparser.add_argument("--node-url", required=True, help="URL to the running node")

    return subparser


def parse_args(args):
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="subparser")

    sync_jobs_parser = create_subparser(
        subparsers,
        Subcommand.SYNC_JOBS,
        scripts.sync_jobs,
        help="Sync job specs from a directory to your node",
    )
    sync_jobs_parser.add_argument(
        "--jobs-dir", help="Path to the directory of job specs to sync", required=True
    )

    create_job_parser = create_subparser(
        subparsers,
        Subcommand.CREATE_JOB,
        scripts.create_job,
        args_validator=scripts.validate_create_job_args,
        help="Add an individual job spec to your node",
    )
    create_job_parser.add_argument(
        "--job", help="Path to the job spec file", required=True
    )

    bootstrap_jobs_parser = create_subparser(
        subparsers,
        Subcommand.BOOTSTRAP_JOBS,
        scripts.bootstrap_jobs,
        help="Bootstrap your node with the default job specs",
    )
    bootstrap_jobs_parser.add_argument(
        "--oracle-address", help="Contract address of your oracle", required=True
    )

    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])

    if not args.subparser:
        sys.exit("No subcommand provided")

    try:
        with open(args.credentials, "r") as f:
            email, password = f.read().splitlines()
    except Exception as e:
        sys.exit(f"Could not read credentials file: {e}")

    try:
        chainlink = api.Chainlink(args.node_url, email, password)
    except Exception as e:
        sys.exit(f"Could not initialize Chainlink client: {e}")

    try:
        getattr(args, "args_validator", lambda x: None)(args)
        args.func(args, chainlink)
        print("Success!")
    except Exception as e:
        sys.exit(str(e))
