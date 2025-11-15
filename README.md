# CMR Notifier

The CMR Notifier project provide public AWS SNS Topics that monitoring applications can subscribe to for new granule notification. Currently, this repository provides these topics:

* New Sentinel-1 SLC and burst granules: `arn:aws:sns:us-west-2:192755178564:ASF-sentinel1-cmr-notifier-prod`

  which will broadcast messages like:
  ```json
  {
    "granule_ur": "S1C_WV_SLC__1SSV_20250328T085056_20250328T085537_001639_002A31_AE2A-SLC",
    "metadata_url": "https://cmr.earthdata.nasa.gov/search/granules.umm_json?provider=ASF&granule_ur=S1C_WV_SLC__1SSV_20250328T085056_20250328T085537_001639_002A31_AE2A-SLC",
    "access_urls": ["https://datapool.asf.alaska.edu/SLC/SC/S1C_WV_SLC__1SSV_20250328T085056_20250328T085537_001639_002A31_AE2A.zip"]
  }
  ```

>[!TIP]
> If you're interested in notification for another ASF-managed dataset, let us know by opening an issue: <https://github.com/ASFHyP3/CMR-notifier/issues/new>

## Usage

>[!IMPORTANT]
> The topics provided here only allow subscriptions using the AWS `SNS` and `Lambda` protocols. 

Here is an example of a minimal CloudFormation template, which when deployed, will create a Sentinel-1 subscription for an AWS SQS Queue:
```yaml
Parameters:
  QueueArn:
    Type: String

Resources:
  Sentinel1Subscription:
    Type: AWS::SNS::Subscription
    Properties:
      TopicArn: arn:aws:sns:us-west-2:192755178564:ASF-sentinel1-cmr-notifier-prod
      Protocol: sqs
      Endpoint: !Ref QueueArn
```

You can add a `FilterPolicy` to the subscription properties so that only the messages you are interested in are accepted:
<https://docs.aws.amazon.com/sns/latest/dg/sns-subscription-filter-policies.html>

For example, this policy will only accept Sentinel-1 Bursts messages: 
```yaml
      FilterPolicyScope: MessageBody
      FilterPolicy: |
        {
          "granule_ur": [{"suffix": "-BURST"}]
        }
```

Or, this policy will only accept Sentinel-1C SLC messages:
```yaml
      FilterPolicyScope: MessageBody
      FilterPolicy: |
        {
          "granule_ur": [{"prefix": "S1C_"}, {"suffix": "-SLC"}]
        }
```

## Development

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

   >[!TIP]
   > If you've done (4), you don't need to prefix commands with `pixi run`.
5. (optional) Setup you IDE to work with pixi:
   * PyCharm: https://pixi.sh/dev/integration/editor/jetbrains/
   * VSCode: https://pixi.sh/dev/integration/editor/vscode/


### Tasks

We use `pixi` as a task runner (similar to a `make`). To see all available tasks, run:
```bash
pixi task list
```

When developing a new feature, you can ensure the code passes all static analyses and tests by running:
```bash
pixi run static
pixi run tests
```
