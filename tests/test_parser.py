import unittest

from chainlink_tools import parse_args


class ArgParserTests(unittest.TestCase):
    def test_create_job(self):
        args = parse_args(
            [
                "--credentials",
                ".api",
                "--node-url",
                "http://example.com",
                "create-job",
                "--job",
                "ethbool.json",
            ]
        )

        self.assertEqual(args.job, "ethbool.json")
        self.assertEqual(args.credentials, ".api")
        self.assertEqual(args.node_url, "http://example.com")

    def test_bootstrap_jobs(self):
        args = parse_args(
            [
                "--credentials",
                ".api",
                "--node-url",
                "http://example.com",
                "bootstrap-jobs",
                "--oracle-address",
                "some address",
            ]
        )

        self.assertEqual(args.oracle_address, "some address")

    def test_sync_jobs(self):
        args = parse_args(
            [
                "--credentials",
                ".api",
                "--node-url",
                "http://example.com",
                "sync-jobs",
                "--jobs-dir",
                "some dir",
            ]
        )

        self.assertEqual(args.jobs_dir, "some dir")
