from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta, datetime
from pymongo import MongoClient
from kafka import KafkaConsumer
from googleapiclient.discovery import build
from textblob import TextBlob
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'execution_timeout': timedelta(minutes=30),
}

# Initialize YouTube API client
api_key = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

# Initialize MongoDB client
mongo_client = MongoClient('mongodb://mongodb:27017/')
db = mongo_client['youtube_comments']
video_ids_collection = db['video_ids']
comments_collection = db['comments']

# Task to fetch video IDs from Kafka and store them in MongoDB
def fetch_and_store_video_ids():
    consumer = KafkaConsumer(
        'video-ids-stream',
        bootstrap_servers='youtube_sentiment_pipeline-kafka-1:9092',
        group_id='airflow-video-id-group',
        auto_offset_reset='earliest',
        enable_auto_commit=False
    )

    max_poll_timeout = 30000  # Poll timeout of 30 seconds
    iteration_limit = 20  # Limit the number of iterations to avoid indefinite waiting

    iteration = 0
    while iteration < iteration_limit:
        messages = consumer.poll(timeout_ms=max_poll_timeout)
        if not messages:
            print("No messages received within the poll timeout, breaking the loop.")
            break

        for message in messages.values():
            for record in message:
                try:
                    data = json.loads(record.value)
                    video_id = data.get('video_id')
                    if not video_id:
                        print("Received empty or malformed video_id, skipping...")
                        continue  # Skip if video_id is empty or None

                    print(f"Storing video ID in MongoDB: {video_id}")
                    video_ids_collection.insert_one({'video_id': video_id, 'processed': False})
                    consumer.commit()

                except json.JSONDecodeError:
                    print("Error decoding JSON, skipping message...")
                except Exception as e:
                    print(f"Error processing message: {e}")

        iteration += 1

    consumer.close()

# Task to fetch comments for each video ID, analyze sentiment, and store in MongoDB
def fetch_and_store_comments():
    max_fetch_time = timedelta(minutes=10)  # Set a maximum time limit for fetching and processing comments
    start_time = datetime.now()

    for video_id_doc in video_ids_collection.find({'processed': False}):
        video_id = video_id_doc['video_id']
        print(f"Processing video ID: {video_id}")

        try:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=50,
                textFormat="plainText"
            ).execute()

            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                sentiment_score = TextBlob(comment['textOriginal']).sentiment.polarity
                comment_data = {
                    'video_id': video_id,
                    'text': comment['textOriginal'],
                    'user': comment['authorDisplayName'],
                    'timestamp': comment['publishedAt'],
                    'sentiment': sentiment_score
                }
                print(f"Storing comment in MongoDB: {comment_data}")
                result = comments_collection.insert_one(comment_data)
                print(f"Inserted document ID: {result.inserted_id}")

            # Mark video ID as processed
            video_ids_collection.update_one(
                {'_id': video_id_doc['_id']},
                {'$set': {'processed': True}}
            )

            # Check if the maximum fetch time has been exceeded
            if datetime.now() - start_time > max_fetch_time:
                print(f"Maximum fetch time exceeded, breaking the loop.")
                break

        except Exception as e:
            print(f"Failed to fetch comments for video ID {video_id}: {e}")

# Define the DAG
dag = DAG(
    'youtube_producer_and_sentiment_pipeline',
    default_args=default_args,
    description='Run YouTube producer to fetch data, send to Kafka, and perform sentiment analysis',
    schedule_interval=timedelta(hours=1),
    start_date=days_ago(1),
    tags=['youtube', 'kafka', 'sentiment', 'analysis'],
)

# Task 1: Run the YouTube producer script to fetch data and send to Kafka
run_youtube_producer = BashOperator(
    task_id='run_youtube_producer',
    bash_command='python /youtube_sentiment_pipeline/kafka_scripts/youtube_producer.py',
    dag=dag,
)

# Task 2: Fetch video IDs from Kafka and store them in MongoDB
fetch_video_ids_task = PythonOperator(
    task_id='fetch_and_store_video_ids',
    python_callable=fetch_and_store_video_ids,
    dag=dag,
)

# Task 3: Fetch comments for each video ID, analyze sentiment, and store in MongoDB
process_comments_task = PythonOperator(
    task_id='fetch_and_store_comments',
    python_callable=fetch_and_store_comments,
    dag=dag,
)

# Define task dependencies
run_youtube_producer >> fetch_video_ids_task >> process_comments_task
