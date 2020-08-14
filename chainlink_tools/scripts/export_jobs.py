import json

from chainlink_tools import utils


def export_jobs(args, chainlink):
    jobs = chainlink.get_specs()

    if args.prune_jobs:
        utils.format_node_jobs(jobs)

    for job in jobs:
        with open(os.path.join(f"{args.dest}")
