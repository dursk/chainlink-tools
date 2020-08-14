import argparse
import requests
import sys

from .constants import Subcommand
from . import api, scripts


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--credentials",
        required=True,
        help="Path to credentials file. This file should be similar to the .api file for the node. First line: username, second line: password",
    )
    parser.add_argument("--node-url", required=True, help="URL to the running node")

    subparsers = parser.add_subparsers(dest="subparser")

    sync_jobs_parser = subparsers.add_parser(
        Subcommand.SYNC_JOBS, help="Sync job specs from a directory to your node"
    )
    sync_jobs_parser.add_argument(
        "--jobs-dir", help="Path to the directory of job specs to sync", required=True
    )
    sync_jobs_parser.set_defaults(func=scripts.sync_jobs)

    create_job_parser = subparsers.add_parser(
        Subcommand.CREATE_JOB, help="Add an individual job spec to your node"
    )
    create_job_parser.add_argument(
        "--job", help="Path to the job spec file", required=True
    )
    create_job_parser.set_defaults(
        func=scripts.create_job, args_validator=scripts.validate_create_job_args
    )

    bootstrap_jobs_parser = subparsers.add_parser(
        Subcommand.BOOTSTRAP_JOBS, help="Bootstrap your node with the default job specs"
    )
    bootstrap_jobs_parser.add_argument(
        "--oracle-address", help="Contract address of your oracle", required=True
    )
    bootstrap_jobs_parser.set_defaults(func=scripts.bootstrap_jobs)

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
