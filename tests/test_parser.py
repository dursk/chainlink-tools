import unittest

from chainlink_tools import parse_args


class ArgParserTests(unittest.TestCase):
    def test_create_job(self):
        args = parse_args(
            [
                "create-job",
                "--job",
                "ethbool.json",
                "--credentials",
                ".api",
                "--node-url",
                "http://example.com",
            ]
        )

        self.assertEqual(args.job, "ethbool.json")
        self.assertEqual(args.credentials, ".api")
        self.assertEqual(args.node_url, "http://example.com")

    def test_bootstrap_jobs(self):
        args = parse_args(
            [
                "bootstrap-jobs",
                "--oracle-address",
                "some address",
                "--credentials",
                ".api",
                "--node-url",
                "http://example.com",
            ]
        )

        self.assertEqual(args.oracle_address, "some address")
        self.assertEqual(args.credentials, ".api")
        self.assertEqual(args.node_url, "http://example.com")

    def test_sync_jobs(self):
        args = parse_args(
            [
                "sync-jobs",
                "--jobs-dir",
                "some dir",
                "--credentials",
                ".api",
                "--node-url",
                "http://example.com",
            ]
        )

        self.assertEqual(args.jobs_dir, "some dir")
        self.assertEqual(args.credentials, ".api")
        self.assertEqual(args.node_url, "http://example.com")
