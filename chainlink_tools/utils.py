import os
import json


def get_job_specs(files):
    jobs = {}

    for filename in files:
        with open(filename, "r") as f:
            job_name = os.path.basename(filename)
            job = json.loads(f.read())
            jobs[job_name] = job

    return jobs


def format_node_jobs(jobs):
    for job in jobs:
        for key in ["id", "createdAt", "earnings", "errors"]:
            del job[key]

        for task in job["tasks"]:
            for key in ["ID", "UpdatedAt", "CreatedAt", "DeletedAt"]:
                del task[key]


def format_job_specs(job_specs):
    for job_spec in job_specs:
        for field in ["startAt", "endAt"]:
            if field not in job_spec:
                job_spec[field] = None
        for task in job_spec["tasks"]:
            if "params" not in task:
                task["params"] = {}
            if "confirmations" not in task:
                task["confirmations"] = None


def validate_job_spec(job_spec):
    if "initiators" not in job_spec:
        return "Missing initiators"
    if "tasks" not in job_spec:
        return "Missing tasks"

    for task in job_spec["tasks"]:
        if "type" not in task:
            return "Missing task type"


def get_jobs_to_create(all_jobs, node_jobs):
    format_job_specs(all_jobs.values())
    format_node_jobs(node_jobs)

    jobs_to_create = {
        job_name: job_spec
        for job_name, job_spec in all_jobs.items()
        if all([node_job != job_spec for node_job in node_jobs])
    }

    return jobs_to_create


def validate_job_specs(jobs):
    for job_name, job_spec in jobs.items():
        error = validate_job_spec(job_spec)

        if error:
            return f"Error found in {job_name}:\n{error}"


def get_and_validate_job_specs(files):
    job_specs = get_job_specs(files)

    errors = validate_job_specs(job_specs)

    if errors:
        raise Exception(errors)

    return job_specs


def create_jobs(jobs, chainlink):
    for job_name, job_spec in jobs.items():
        print(f"Creating {job_name}")
        chainlink.create_spec(job_spec)


def set_oracle_address(job_specs, address):
    for job_spec in job_specs:
        job_spec["initiators"][0]["params"]["address"] = address.lower()
