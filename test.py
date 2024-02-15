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



from IPython.display import display, HTML
# Function to highlight the word "reflection" in the log messages
def highlight_reflection(text, color='yellow'):
    highlighted_text = text.replace("reflection", f"<span style='background-color: {color};'>reflection</span>")
    return highlighted_text

# Assume query_results['results'] contains the logs
highlighted_results = []

for result in query_results['results']:
    # Assuming each result has a message field
    message = result.get('@message', '')
    # Highlight the word "reflection" in the message
    highlighted_message = highlight_reflection(message)
    # Add the timestamp for context (assuming result has a timestamp field)
    timestamp = result.get('@timestamp', '')
    highlighted_results.append(f"{timestamp}: {highlighted_message}")

# Combine all highlighted results into a single HTML string
html_results = "<br>".join(highlighted_results)

# Display the results as HTML
display(HTML(html_results))
