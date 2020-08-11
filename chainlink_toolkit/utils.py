import glob
import json

from . import api


def get_all_jobs(job_dir):
    files = glob.glob(f"{job_dir}/*.json")

    jobs = []

    for file_ in files:
        with open(file_, "r") as f:
            jobs.append(json.loads(f.read()))

    return jobs


def prune_node_job(job):
    del job["id"]
    del job["createdAt"]

    for task in job["tasks"]:
        for key in ["ID", "UpdatedAt", "CreatedAt", "DeletedAt"]:
            del task[key]

    return job


def get_jobs_to_create(job_dir):
    all_jobs = get_all_jobs(job_dir)
    node_jobs = api.Chainlink(
        "https://localhost:6689", "madurskimr@gmail.com", "foobarfizzbuzz"
    ).get_specs()

    node_jobs = [prune_node_job(j) for j in node_jobs]

    jobs_to_create = []

    for job in all_jobs:
        print(json.dumps(job, indent=4, sort_keys=True))
        found = False
        for node_job in node_jobs:
            print(json.dumps(node_job, indent=4, sort_keys=True))
            if job == node_job:
                found = True
                break
        if not found:
            jobs_to_create.append(job)

    return jobs_to_create
