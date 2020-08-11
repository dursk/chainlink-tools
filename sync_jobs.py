import argparse

from chainlink_toolkit import api
from chainlink_toolkit import utils


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--email")
    parser.add_argument("--password")
    parser.add_argument("--jobs-dir")
    parser.add_argument("--node-url")
    return parser.parse_args()


def main():
    args = parse_args()

    chainlink = api.Chainlink(args.node_url, args.email, args.password)

    jobs_to_create = utils.get_jobs_to_create(args.jobs_dir)

    print(f"Found {len(jobs_to_create)} jobs to create")

    for job in jobs_to_create:
        chainlink.create_spec(job)

    print("Success!")


if __name__ == "__main__":
    main()
