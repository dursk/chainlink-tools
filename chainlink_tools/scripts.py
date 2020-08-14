import glob
import os
import sys

from .constants import Subcommand
from . import utils


def validate_create_job_args(args):
    if not args.job.endswith(".json"):
        raise Exception(f"Specific job spec file ${args.job} is not a .json file")


def _confirm_job_sync(jobs_to_create):
    print(f"Found {len(jobs_to_create)} jobs to create:")
    print("\n".join([job_name for job_name in jobs_to_create]))
    print("Continue? [y/n]")

    response = input()

    if response.lower() != "y":
        raise Exception("Aborting!")


def sync_jobs(args, chainlink):
    job_specs = utils.get_and_validate_job_specs(glob.glob(f"{args.jobs_dir}/*.json"))
    node_jobs = chainlink.get_specs()
    jobs_to_create = utils.get_jobs_to_create(job_specs, node_jobs)

    if not jobs_to_create:
        print("No new jobs found.")
        return

    _confirm_job_sync(jobs_to_create)

    utils.create_jobs(jobs_to_create, chainlink)


def create_job(args, chainlink):
    job_specs = utils.get_and_validate_job_specs([args.job])
    utils.create_jobs(job_specs, chainlink)


def bootstrap_jobs(args, chainlink):
    jobs_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "bootstrap_jobs"
    )
    print(jobs_dir)
    job_specs = utils.get_and_validate_job_specs(glob.glob(f"{jobs_dir}/*.json"))

    utils.set_oracle_address(job_specs.values(), args.oracle_address)

    utils.create_jobs(job_specs, chainlink)
