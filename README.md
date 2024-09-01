# YouTube Comment Sentiment Workflow: Airflow, Spark, MongoDB, Tableau, Docker
A scalable workflow for sentiment analysis on YouTube comments using Python, Kafka, Airflow, Spark, and MongoDB, with data visualization in Tableau. Key components are containerized in Docker for seamless deployment.

## Project Overview
The **YouTube Sentiment Analytics Workflow** is an advanced data processing solution designed to capture, process, and analyze sentiment from YouTube comments. This workflow provides a comprehensive approach to understanding audience sentiment, enabling content creators, marketers, and researchers to derive actionable insights. By leveraging scalable, automated processes, this workflow ensures that sentiment analysis is both efficient and insightful.

## Core Objectives
This workflow is engineered to achieve the following key objectives:

- **Automated Collection**: Use YouTube Data API to continuously extract comments in real-time for seamless analysis.
- **Scalable Processing**: Leverage Apache Spark for efficient management of large datasets through distributed processing.
- **Sentiment Analysis**: Classify audience sentiment using Python NLP, categorizing comments as positive, negative, or neutral.
- **Flexible Storage**: Store and query sentiment data efficiently with MongoDB, accommodating unstructured data.
- **Visual Insights**: Transform sentiment data into actionable visuals using Tableau, providing clear trends and patterns.
- **Adaptive Workflow**: Ensure the system evolves with changing needs through a modular and easily extensible design.
- **Real-Time Monitoring**: Utilize Apache Airflow to orchestrate, monitor, and retry workflow tasks, ensuring reliable execution.
- **Seamless Deployment**: Employ Docker to containerize the workflow, ensuring consistent environments and easy deployment.

## Workflow Components
This workflow is composed of several interconnected components, each playing a crucial role in the data processing pipeline:

### YouTube Data API
The **YouTube Data API** serves as the entry point for data into the workflow, fetching comments from specific videos or channels based on the analysis requirements.

- **Dynamic Targeting**: Configured to target specific videos, the API allows the workflow to focus on content that is most relevant for the analysis.
- **Efficiency**: The API efficiently manages large volumes of data, ensuring that comments are retrieved in a timely manner without overwhelming the system.

![YouTube Data API](https://github.com/user-attachments/assets/5c2aa9b8-089b-4fe9-b944-237a010b8cd4)

### Apache Kafka
**Apache Kafka** is the backbone of the data streaming process, enabling real-time ingestion and transmission of comments throughout the workflow.

- **Real-Time Streaming**: Kafka ensures that data is streamed efficiently, making comments available for immediate processing as soon as they are ingested.
- **Scalability**: With its distributed architecture, Kafka can handle the high throughput required for processing large volumes of comments from popular YouTube channels.

![image](https://github.com/user-attachments/assets/682e9ca7-6323-4a59-8c86-16810895cf91)

![image](https://github.com/user-attachments/assets/583f7321-90ee-469d-b79c-fd1bdb635798)

![image](https://github.com/user-attachments/assets/b7ced301-6f1b-4e5c-bc82-fb9b24f0747d)

### Apache Airflow
**Apache Airflow** orchestrates the entire workflow, managing the execution of tasks from data ingestion to visualization.

- **Workflow Orchestration**: Airflow uses Directed Acyclic Graphs (DAGs) to define the sequence of operations, ensuring that each task is executed in the correct order.
- **Monitoring & Retry**: Airflow provides robust monitoring capabilities, allowing for the automatic retry of failed tasks and easy tracking of the workflow’s progress.

![Airflow DAG](https://github.com/user-attachments/assets/f7075e1d-5365-4272-8028-f5eec8d2b8c3)

![Airflow Task Execution](https://github.com/user-attachments/assets/12611e00-67a2-4f23-8960-4f6cbe4d516e)

![image](https://github.com/user-attachments/assets/870b1acb-7267-43a3-8df8-00bc587704f7)

![image](https://github.com/user-attachments/assets/1fc145a8-1787-4a4b-afab-5aa664164ddd)

### Apache Spark
**Apache Spark** plays a critical role in processing the data. It cleans, transforms, and prepares the comments for sentiment analysis, all while handling large datasets efficiently.

- **Data Transformation**: Spark is responsible for filtering out irrelevant data and preparing the comments for analysis, ensuring that only meaningful information is passed on for sentiment evaluation.
- **Parallel Processing**: Spark’s ability to process data in parallel across multiple nodes makes it ideal for real-time analytics in a high-volume environment.

### Sentiment Analysis with Python
The sentiment analysis is conducted using Python’s NLP libraries, which analyze and categorize each comment based on its emotional tone.

- **Sentiment Classification**: Python’s NLP tools classify comments into positive, negative, or neutral categories, helping to quantify audience sentiment.
- **Text Processing**: Techniques like tokenization, lemmatization, and the use of sentiment lexicons ensure accurate and reliable sentiment analysis.

![Python Sentiment Analysis](https://github.com/user-attachments/assets/62d0eed8-15fa-4f0e-a50b-de686fbcdd2e)
![Sentiment Analysis Output](https://github.com/user-attachments/assets/6ff095d7-730a-4257-a3f7-bba026dac04e)

### MongoDB
**MongoDB** stores the processed data, offering a flexible and scalable solution for managing unstructured data like YouTube comments.

- **Data Storage**: MongoDB stores each comment along with its sentiment score and metadata, providing a comprehensive database for further analysis.
- **Querying Capabilities**: MongoDB’s powerful querying capabilities make it easy to retrieve specific data points or aggregate sentiment scores for broader analysis.

![MongoDB Data Structure](https://github.com/user-attachments/assets/31a74439-0d40-4366-a993-d11a8139d630)

![image](https://github.com/user-attachments/assets/ed2f2e17-1f05-4c84-a184-90651c4972d9)

![MongoDB Query Results](https://github.com/user-attachments/assets/1dd090dd-b553-431c-bf66-4e226a0496e3)

### 7. Docker Containerization
**Docker** is used to containerize the core components of the workflow, ensuring that the environment is consistent across different deployments. Docker simplifies dependency management and allows the entire workflow to be easily deployed on different machines or cloud environments.

- **Setup Process**: The Docker setup involves creating a `docker-compose.yml` file that defines and configures the services required by the workflow, including Kafka, Zookeeper, Spark, and MongoDB. This file ensures that all services are started with the correct configurations and can communicate with each other within the Docker network.

- **Advantages of Containerization**: By containerizing the workflow’s components, Docker ensures that the same environment is used in development, testing, and production. This eliminates issues related to inconsistent environments and makes it easier to scale and manage the workflow.

![Docker Setup](https://github.com/user-attachments/assets/968eba38-3c5b-43fc-b9bc-d611224a4968)
![image](https://github.com/user-attachments/assets/9d85859a-fb27-4db0-bbfd-50e4d7c07ade)

- **Docker Compose Configuration**: The `docker-compose.yml` file provides the blueprint for setting up the services required by the workflow. It includes configurations for Kafka, Zookeeper, Spark, and MongoDB, ensuring that each service is properly connected and operational.

- **Building and Starting Containers**: 
  - Navigate to the project root directory where the `docker-compose.yml` file is located.
  - Execute the following command to build and start the containers:
    ```bash
    docker-compose up -d
    ```
  - This command pulls the necessary Docker images and starts the services in detached mode, allowing the workflow to run in the background.

  ![Build and Start Containers](https://github.com/user-attachments/assets/20e7e466-8f5a-4892-95e9-c39aedf3bf28)

- **Verifying Running Containers**: 
  - To verify all services are running correctly, use the command:
    ```bash
    docker ps
    ```
  - This displays a list of running containers, including Kafka, Zookeeper, Spark, MongoDB, and other services defined in your `docker-compose.yml` file.

  ![Verify Containers](https://github.com/user-attachments/assets/ea164721-647f-4788-a102-552bc213b30a)

- **Accessing Services**: 
  - Once containers are running, you can access the services via their respective ports as defined in the `docker-compose.yml` file.
    - Kafka: `localhost:9092`
    - MongoDB: `localhost:27017`
    - Spark: `localhost:8080`
  - These services can be accessed from your local machine or from other containers in the Docker network, facilitating smooth interactions with the workflow components.

  ![Accessing Services](https://github.com/user-attachments/assets/0020a1ae-e9ac-42ca-9e27-d3809ddabee1)

- **Shutting Down Containers**: 
  - To stop the running containers, use the command:
    ```bash
    docker-compose down
    ```
  - This command stops and removes the containers while preserving data volumes, ensuring that no data is lost during the shutdown.

- **Persistent Data Storage**: 
  - The `docker-compose.yml` file is configured to mount data volumes for MongoDB and other services, ensuring data persistence between container restarts. This is crucial for retaining the processed comments and sentiment analysis results in MongoDB, even when the containers are stopped and restarted.

### 8. Tableau Visualization
**Tableau** is the final component of the workflow, used to visualize the sentiment analysis results. By connecting Tableau to MongoDB, users can create interactive dashboards and reports that depict sentiment trends across videos, time periods, or other dimensions of interest.

- **Visualization Capabilities**: Tableau provides powerful visualization tools that allow users to explore the data in depth. Users can create custom dashboards that display sentiment scores over time, compare sentiment across different videos, or analyze the impact of specific events on audience sentiment.

- **Connecting to MongoDB**: Tableau connects to MongoDB via the MongoDB BI Connector or other suitable methods, enabling users to query the sentiment data stored in MongoDB and create visualizations directly from this data.

- **Insight Generation**: The visualizations created in Tableau help stakeholders understand how audience sentiment changes over time, which videos resonate most with viewers, and how different factors (such as video content, publication time, or promotional efforts) influence sentiment.

![Tableau Dashboard](https://github.com/user-attachments/assets/3777844e-d5ab-46e1-9a88-1818eb6f5c8f)
![Tableau Insights](https://github.com/user-attachments/assets/d9ef17e7-8015-4199-bbd1-ada58241226f)
![Tableau Data Visualization](https://github.com/user-attachments/assets/e8d52be2-79ff-478d-8a32-b05f15abfb36)

## Advantages and Applications
The YouTube Sentiment Analytics Workflow offers several significant advantages:

- **Immediate Insights**: The workflow allows stakeholders to analyze and respond to emerging trends or audience feedback in near real-time. This responsiveness is crucial for content creators and marketers who need to adjust their strategies based on audience reactions.

- **Scalability**: The use of distributed processing and scalable components like Kafka and Spark ensures that the workflow can handle increasing data volumes without performance degradation. This scalability is essential for processing data from popular YouTube channels with millions of comments.

- **Actionable Intelligence**: The sentiment analysis provides actionable insights that can inform content strategy, marketing campaigns, and audience engagement efforts. By understanding audience sentiment, stakeholders can make data-driven decisions that enhance the effectiveness of their content and marketing initiatives.

- **Flexibility**: The modular design of the workflow facilitates easy customization and the integration of advanced features or new data sources. This flexibility ensures that the workflow can evolve with changing requirements and continue to deliver valuable insights.

## Future Enhancements
Future enhancements to this workflow could include:

- **Advanced Sentiment Analysis**: Implementing more sophisticated sentiment analysis techniques, such as deep learning models, to improve the accuracy and depth of sentiment classification.

- **Additional Data Sources**: Integrating other social media platforms or data sources to provide a more comprehensive view of audience sentiment across multiple channels.

- **Enhanced Visualizations**: Expanding the Tableau dashboards to include more complex visualizations, such as sentiment over time, comparisons between videos, or demographic-based sentiment analysis.

- **Automated Reporting**: Adding automated reporting features to generate and distribute sentiment analysis reports to stakeholders on a regular basis.

## Conclusion
The YouTube Sentiment Analytics Workflow is a powerful tool for extracting, processing, and analyzing sentiment data from YouTube comments. By leveraging a robust tech stack and following best practices in data engineering, this workflow demonstrates an efficient, scalable, and insightful approach to understanding audience sentiment. Whether you're a content creator looking to gauge audience reactions or a marketer interested in the impact of campaigns, this workflow provides the insights needed to make data-driven decisions.
