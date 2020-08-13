import glob
import os
import sys

from chainlink_tools import utils


def get_job_files(args):
    if args.subparser == "bootstrap-jobs":
        jobs_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), os.pardir, "bootstrap_jobs"
        )
        files = glob.glob(f"{jobs_dir}/*.json")
    elif args.subparser == "sync-jobs":
        files = glob.glob(f"{args.jobs_dir}/*.json")
    else:
        if not args.job.endswith(".json"):
            sys.exit(f"Specific job spec file ${args.job} is not a .json file")
        files = [args.job]

    return files


def validate_job_specs(jobs):
    for job_name, job_spec in jobs.items():
        error = utils.validate_job_spec(job_spec)

        if error:
            sys.exit(f"Error found in {job_name}:\n{error}")


def sync_chainlink_jobs(args, chainlink):
    files = get_job_files(args)

    all_jobs = utils.get_all_jobs(files)

    validate_job_specs(all_jobs)

    if args.subparser == "bootstrap-jobs":
        for _, job_spec in all_jobs.items():
            job_spec["initiators"][0]["params"]["address"] = args.oracle_address.lower()

    node_jobs = chainlink.get_specs()

    jobs_to_create = utils.get_jobs_to_create(all_jobs, node_jobs)

    if not jobs_to_create:
        print("No new jobs found.")
        sys.exit(0)

    if args.subparser != "create-job":
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
