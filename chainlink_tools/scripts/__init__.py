import argparse
import requests
import sys

from chainlink_tools import api
from .constants import Subcommand
from .sync_chainlink_jobs import sync_chainlink_jobs


def parse_args():
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
    sync_jobs_parser.set_defaults(func=sync_chainlink_jobs)

    create_job_parser = subparsers.add_parser(
        Subcommand.CREATE_JOB, help="Add an individual job spec to your node"
    )
    create_job_parser.add_argument(
        "--job", help="Path to the job spec file", required=True
    )
    create_job_parser.set_defaults(func=sync_chainlink_jobs)

    bootstrap_jobs_parser = subparsers.add_parser(
        Subcommand.BOOTSTRAP_JOBS, help="Bootstrap your node with the default job specs"
    )
    bootstrap_jobs_parser.add_argument(
        "--oracle-address", help="Contract address of your oracle", required=True
    )
    bootstrap_jobs_parser.set_defaults(func=sync_chainlink_jobs)

    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.credentials, "r") as f:
        email, password = f.read().splitlines()

    chainlink = api.Chainlink(args.node_url, email, password)

    try:
        args.func(args, chainlink)
    except requests.exceptions.HTTPError as e:
        sys.exit(str(e))
