TOPIC_NAME=$1

gcloud functions deploy python-pubsub-function \
--runtime=python312 \
--region=us-central1 \
--source=. \
--entry-point=subscribe \
--trigger-topic=$TOPIC_NAME
