import glob
import os
import sys

from chainlink_tools import utils
from .constants import Subcommand


def validate_args(args):
    if getattr(args, "job", None) and not args.job.endswith(".json"):
        sys.exit(f"Specific job spec file ${args.job} is not a .json file")


def get_job_files(args):
    jobs_dir = None

    if args.subparser == Subcommand.BOOTSTRAP_JOBS:
        jobs_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), os.pardir, "bootstrap_jobs"
        )
    elif args.subparser == Subcommand.SYNC_JOBS:
        jobs_dir = args.jobs_dir

    if jobs_dir:
        files = glob.glob(f"{jobs_dir}/*.json")
    elif args.subparser == Subcommand.CREATE_JOB:
        files = [args.job]
    else:
        sys.exit("No jobs directory or job specified")

    return files


def set_oracle_address(job_specs, address):
    for job_spec in job_specs:
        job_spec["initiators"][0]["params"]["address"] = address.lower()


def sync_chainlink_jobs(args, chainlink):
    validate_args(args)

    files = get_job_files(args)

    job_specs = utils.get_job_specs(files)

    utils.validate_job_specs(job_specs)

    if args.subparser == Subcommand.BOOTSTRAP_JOBS:
        set_oracle_address(job_specs.values(), args.oracle_address)

    if args.subparser == Subcommand.SYNC_JOBS:
        node_jobs = chainlink.get_specs()
        jobs_to_create = utils.get_jobs_to_create(job_specs, node_jobs)
    else:
        jobs_to_create = job_specs

    if not jobs_to_create:
        print("No new jobs found.")
        sys.exit(0)

    if args.subparser == Subcommand.SYNC_JOBS:
        print(f"Found {len(jobs_to_create)} jobs to create:")
        print("\n".join([job_name for job_name in jobs_to_create]))
        print("Continue? [y/n]")

        response = input()

        if response.lower() != "y":
            print("Aborting!")
            sys.exit(0)

    for job_name, job_spec in jobs_to_create.items():
        print(f"Creating {job_name}")
        chainlink.create_spec(job_spec)

    print("Success!")
