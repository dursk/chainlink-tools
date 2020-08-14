import os
import unittest
from unittest.mock import patch, Mock

from chainlink_tools import scripts

JOB_SPECS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "job_specs")


class ScriptTest(unittest.TestCase):
    def setUp(self):
        self.chainlink = Mock()


class CreateJobTests(ScriptTest):
    def test_validation(self):
        args = Mock(job="something.txt")
        with self.assertRaises(Exception) as e:
            scripts.create_job(args, self.chainlink)
            self.assertEqual(
                str(e), "Specific job spec file something.txt is not a .json file"
            )

    def test_create_job(self):
        args = Mock(job=os.path.join(JOB_SPECS_DIR, "ethbool.json"))

        scripts.create_job(args, self.chainlink)

        self.chainlink.create_spec.assert_called_with(
            {
                "initiators": [
                    {
                        "type": "runlog",
                        "params": {"address": "<ORACLE_CONTRACT_ADDRESS>"},
                    }
                ],
                "tasks": [
                    {"type": "httpget"},
                    {"type": "jsonparse"},
                    {"type": "ethbool"},
                    {"type": "ethtx"},
                ],
            }
        )


class BootstrapJobsTests(ScriptTest):
    def test_bootstrap_jobs(self):
        args = Mock(oracle_address="0x3780c2c3a2cd89143fd7fdef850ca0d3a85dd138")

        scripts.bootstrap_jobs(args, self.chainlink)

        self.assertEqual(self.chainlink.create_spec.call_count, 5)

        for call_args in self.chainlink.create_spec.call_args_list:
            self.assertEqual(
                call_args[0][0]["initiators"][0]["params"]["address"],
                args.oracle_address,
            )


class SyncJobsTests(ScriptTest):
    def test_sync_jobs(self):
        args = Mock(jobs_dir=JOB_SPECS_DIR)

        self.chainlink.get_specs.return_value = []

        with patch("chainlink_tools.scripts._confirm_job_sync"):
            scripts.sync_jobs(args, self.chainlink)

        self.assertEqual(self.chainlink.create_spec.call_count, 1)

        self.chainlink.create_spec.reset_mock()

        self.chainlink.get_specs.return_value = [
            {
                "id": "foo",
                "createdAt": "some timestamp",
                "earnings": 0,
                "errors": None,
                "startAt": None,
                "endAt": None,
                "initiators": [
                    {
                        "type": "runlog",
                        "params": {"address": "<ORACLE_CONTRACT_ADDRESS>"},
                    }
                ],
                "tasks": [
                    {
                        "type": "httpget",
                        "ID": "bar",
                        "UpdatedAt": "some timestamp",
                        "CreatedAt": "some timestamp",
                        "DeletedAt": "some timestamp",
                        "confirmations": None,
                        "params": {},
                    },
                    {
                        "type": "jsonparse",
                        "ID": "bar",
                        "UpdatedAt": "some timestamp",
                        "CreatedAt": "some timestamp",
                        "DeletedAt": "some timestamp",
                        "confirmations": None,
                        "params": {},
                    },
                    {
                        "type": "ethbool",
                        "ID": "bar",
                        "UpdatedAt": "some timestamp",
                        "CreatedAt": "some timestamp",
                        "DeletedAt": "some timestamp",
                        "confirmations": None,
                        "params": {},
                    },
                    {
                        "type": "ethtx",
                        "ID": "bar",
                        "UpdatedAt": "some timestamp",
                        "CreatedAt": "some timestamp",
                        "DeletedAt": "some timestamp",
                        "confirmations": None,
                        "params": {},
                    },
                ],
            }
        ]

        with patch("chainlink_tools.scripts._confirm_job_sync"):
            scripts.sync_jobs(args, self.chainlink)

        self.assertEqual(self.chainlink.create_spec.call_count, 0)
