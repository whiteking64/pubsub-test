import argparse
from concurrent.futures import TimeoutError

from google.cloud import pubsub_v1


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received message: {repr(message)}")
    message.ack()


def main():
    parser = argparse.ArgumentParser(description="Pull messages from a Pub/Sub subscription.")
    parser.add_argument("--project-id", required=True, help="Your Google Cloud project ID.")
    parser.add_argument("--subscription-id", required=True, help="Your Pub/Sub subscription ID.")
    parser.add_argument("--timeout", type=float, default=5.0, help="Timeout in seconds.")

    args = parser.parse_args()

    project_id = args.project_id
    subscription_id = args.subscription_id
    timeout = args.timeout

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()


if __name__ == "__main__":
    main()
