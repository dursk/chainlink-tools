![Python package](https://github.com/dursk/chainlink-tools/workflows/Python%20package/badge.svg)

# Chainlink Tools

`chainlink-tools` is a command line utility designed to make life easier for Chainlink node operators.

### Notes

Authentication with the node is managed by the same `.api` file as outlined in the [official Chainlink documentation](https://docs.chain.link/docs/miscellaneous#config).

## Install
```
$ pip install chainlink-tools
```

## Bootstrapping a node
The `bootstrap-jobs` subcommand allows for easy bootstrapping when setting up a node for the first time.
```
$ chainlink-tools \
    --credentials "/path/to/.api/file" \
    --node-url "http://localhost:6688" \
    bootstrap-jobs \
    --oracle-address "YOUR_ORACLE_CONTRACT_ADDRESS"
```
This will add the five default jobs to the node, as outlined in the [Chainlink docs](https://docs.chain.link/docs/fulfilling-requests#add-jobs-to-the-node):
* EthBytes32 (GET)
* EthBytes32 (POST)
* EthInt256
* EthUint256
* EthBool

The address you pass in for `--oracle-address` will be set as the address for the `RunLog` initiator.

## Adding new jobs to a node
`chainlink-tools` provides two different mechanisms for adding new jobs to a node.
### Syncing a directory of jobs
The `sync-jobs` subcommand allows for syncing a directory of job specs to a running node.
```
$ chainlink-tools \
    --credentials "/path/to/.api/file" \
    --node-url "http://localhost:6688" \
    sync-jobs \
    --jobs_dir "/path/to/jobs/dir"
```
`--jobs-dir` should be the path to a directory of `.json` files of job specs:
```
chainlink-jobs
|   ethusd.json
|   btcusd.json
|   linkusd.json
```
`sync-jobs` will first check to see if the job already exists in the node. This is done by doing a comparison of all initators, tasks, and other top level fields. For any jobs in the specified directory not already found on the node, `sync-jobs` will add them to the node.

This allows you to keep a single running directory of all your jobs and run `sync-jobs` on the whole directory every time you add a new one.

*Note: For comparison purposes, all ETH addresses that appear in a job spec should be lowercase.*
### Specifying a single job to add to a node
Alternatively, if you would like to manually create each individual job, the `create-job` subcommand allows for specifying a single job to add to a node.
```
$ chainlink-tools \
    --credentials "/path/to/.api/file" \
    --node-url "http://localhost:6688" \
    create-job \
    --job "/path/to/job1.json"
```
