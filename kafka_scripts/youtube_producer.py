import os
from kafka import KafkaProducer
from dotenv import load_dotenv
import logging
import simplejson as json  # Enhanced JSON handling
from googleapiclient.discovery import build
from textblob import TextBlob  # For sentiment analysis

# Load environment variables
load_dotenv()

# Kafka topic names
video_id_topic = 'video-ids-stream'
comments_topic = 'youtube-comments-stream'

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',  # Use IPv4 explicitly
    value_serializer=lambda v: json.dumps(v, ignore_nan=True).encode('utf-8')
)

# Initialize YouTube API client
api_key = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def fetch_comments(video_id):
    comments = []
    try:
        # Fetch comments using the YouTube API
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=50,
            textFormat="plainText"
        ).execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            sentiment_score = analyze_sentiment(comment['textOriginal'])
            comments.append({
                'textOriginal': comment['textOriginal'],
                'authorDisplayName': comment['authorDisplayName'],
                'publishedAt': comment['publishedAt'],
                'sentiment': sentiment_score
            })

        if not comments:
            logger.warning(f"No comments found for video ID {video_id}.")
    except Exception as e:
        logger.error(f"Failed to fetch comments for video ID {video_id}: {e}")
        return []

    return comments

def send_video_id_to_kafka(video_id):
    if not video_id:
        logger.warning("Received an empty video_id, skipping...")
        return

    try:
        message = {'video_id': video_id}
        logger.debug(f"Sending message to Kafka: {message}")
        producer.send(video_id_topic, message)
        logger.info(f"Successfully sent video ID to Kafka: {video_id}")
    except Exception as e:
        logger.error(f"Failed to send video ID to Kafka: {str(e)}")

def send_comment_to_kafka(video_id, comment_data):
    try:
        if not all(comment_data.values()):
            logger.warning(f"Incomplete comment data for video ID {video_id}, skipping...")
            return

        logger.info(f"Sending comment data to Kafka for video ID {video_id}")
        producer.send(comments_topic, comment_data)
    except Exception as e:
        logger.error(f"Error sending comment data to Kafka: {str(e)}")

def main():
    video_ids = [
        'CD0bRU1e1ZM', 'WFcYF_pxLgA'  # Example video IDs
    ]

    try:
        # Send each video_id to the Kafka topic
        for video_id in video_ids:
            send_video_id_to_kafka(video_id)

        # Then, send the comments related to the video_id to the youtube-comments-stream Kafka topic
        for video_id in video_ids:
            comments = fetch_comments(video_id)
            for comment in comments:
                comment_data = {
                    'video_id': video_id,
                    'text': comment['textOriginal'],
                    'user': comment['authorDisplayName'],
                    'timestamp': comment['publishedAt'],
                    'sentiment': comment['sentiment']  # Sentiment score
                }
                send_comment_to_kafka(video_id, comment_data)

    except Exception as e:
        logger.error(f"Unexpected error in main processing loop: {str(e)}")

    finally:
        # Ensure all messages have been sent before closing
        producer.flush()
        producer.close()
        logger.info("Kafka producer closed gracefully.")

if __name__ == "__main__":
    main()
