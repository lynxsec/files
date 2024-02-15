import botocore.session
from datetime import datetime, timedelta
import time

# Create a botocore session
session = botocore.session.get_session()

# Create a CloudWatch Logs client
client = session.create_client('logs', region_name='your-region')  # Specify your AWS region

# Calculate start and end times for the desired time range in milliseconds since Unix epoch
end_time = int(datetime.now().timestamp() * 1000)  # Current time in milliseconds
start_time = end_time - (5 * 24 * 60 * 60 * 1000)  # 5 days ago in milliseconds

# Define your query to select all logs
log_group = 'your-log-group-name'
query = "fields @timestamp, @message | sort @timestamp desc"  # Adjust your query as needed

# Start the query
query_start_response = client.start_query(
    logGroupName=log_group,
    startTime=start_time,
    endTime=end_time,
    queryString=query,
)

# Query ID from response
query_id = query_start_response['queryId']

# Wait for the query to complete (in real applications, implement a more robust waiting mechanism)
time.sleep(10)  # This is just a simple pause; adjust based on expected query completion time

# Get the query results
query_results = client.get_query_results(
    queryId=query_id
)

# Print the results
for result in query_results['results']:
    print(result)
