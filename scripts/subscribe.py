"""Script to set up a CMR ingest subscription."""


# TODO: Setup subscription
#  1. load umm-sub template
#  2. render umm-sub. Needs:
#      - username
#      - collection concept id
#      - SQS endpoint arn
#  3. validate umm-sub with json schema?
#  4. get auth token for EDL user
#  5. POST umm-sub


# TODO: Confirm subscription
#  6. poll SQS for confirmation message
#  7. "visit" (GET) "SubscribeURL" from confirmation message
#  8. delete message from queue
