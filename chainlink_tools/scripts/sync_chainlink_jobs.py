import os
import sys

from chainlink_tools import utils


def sync_chainlink_jobs(args, chainlink):
    if args.bootstrap:
        args.jobs_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), os.pardir, "bootstrap_jobs"
        )
    elif not args.jobs_dir:
        sys.exit("Either --jobs-dir or --bootstrap must be specified")

    all_jobs = utils.get_all_jobs(args.jobs_dir)

    for job_name, job_spec in all_jobs.items():
        error = utils.validate_job_spec(job_spec)

        if error:
            sys.exit(f"Error found in {job_name}:\n{error}")

    node_jobs = chainlink.get_specs()

    jobs_to_create = utils.get_jobs_to_create(all_jobs, node_jobs)

    if not jobs_to_create:
        print("No new jobs found.")
        sys.exit(0)

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
