import argparse
import time
from concurrent import futures
from typing import Callable

from google.cloud import pubsub_v1


def get_callback(
    publish_future: pubsub_v1.publisher.futures.Future, data: str
) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
        try:
            print(publish_future.result(timeout=5))
        except futures.TimeoutError:
            print(f"Publishing {data} timed out.")

    return callback


def main():
    parser = argparse.ArgumentParser(description="Pull messages from a Pub/Sub subscription.")
    parser.add_argument("--project-id", required=True, help="Your Google Cloud project ID.")
    parser.add_argument("--topic-id", required=True, help="Your Pub/Sub topic ID.")

    args = parser.parse_args()

    project_id = args.project_id
    topic_id = args.topic_id

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    publish_futures = []

    for i in range(10):
        data = f"Message {i}"
        custom_attributes = {
            "origin": "python-sample",
            "username": "gcp",
        }
        publish_future = publisher.publish(topic_path, data.encode("utf-8"), **custom_attributes)
        publish_future.add_done_callback(get_callback(publish_future, data))
        publish_futures.append(publish_future)

        print(f"Published message {i} to {topic_path}.")
        time.sleep(1)

    # Wait for all the publish futures to resolve before exiting.
    futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

    print(f"Published messages with error handler to {topic_path}.")


if __name__ == "__main__":
    main()
