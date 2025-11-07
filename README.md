# CMR Notifier

The CMR Notifier project provide AWS SNS topics applications can subscribe to for new granule notification for some of ASF's datasets which are used for monitoring applications. Currently, this repository provides:

* Sentinel-1 SLC Topic: TBD
* Sentinel-1 Bursts Topic: TBD

If you're interested in notification for another ASF-managed dataset, let us know by opening an issue: <https://github.com/ASFHyP3/CMR-notifier/issues/new>

## Knowledge Base

Currently, CMR Notifier uses CMR Ingest Subscriptions to as the source of new granule notifications:
* https://wiki.earthdata.nasa.gov/spaces/CMR/pages/404522012/CMR+Ingest+Subscriptions

> [!WARNING]
> As documented in the [CMR API docs](https://cmr.earthdata.nasa.gov/ingest/site/docs/ingest/api.html#subscription), each AWS SQS queue should have only one agreed upon subscription!

## Setup

This project uses `pixi` to manage software environments. To get started: 

1. Ensure that `pixi` is installed on your system: <https://pixi.sh/latest/installation/>.
2. Clone this repository and navigate to the root directory of this project
   ```bash
   git clone https://github.com/ASFHyP3/CMR-notifier.git
   cd CMR-notifier
   ```
3. Setup the development environment
   ```bash
    pixi run python -VV
   ```
4. (Optional) Activate the environment. Either:
   1. use the pixi shell:
      ```bash
      pixi shell
      ```
   2. or, for [traditional conda-like activation](https://pixi.sh/latest/workspace/environment/#traditional-conda-activate-like-activation), run:
      ```bash
      eval "$(pixi shell-hook)"
      ```

    >    [!TIP]
    >    If you've done (4), you don't need to prefix commands with `pixi run`.
5. (optional) Setup you IDE to work with pixi:
   * PyCharm: https://pixi.sh/dev/integration/editor/jetbrains/
   * VSCode: https://pixi.sh/dev/integration/editor/vscode/


## Usage

We use `pixi` as a task runner (similar to a `make`). To see all available tasks, run:
```bash
pixi task list
```
