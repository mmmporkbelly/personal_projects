import requests
import time

url = input("Enter the URL you want to scan: ")
api_key = "API KEY"

# Submit URL for scan
submit_url = "https://www.virustotal.com/api/v3/urls"
submit_headers = {  "accept": "application/json",
              'x-apikey': api_key,
              "content-type": "application/x-www-form-urlencoded"}
submit_data = {'url': url}
submit_response = requests.post(submit_url, data=submit_data, headers=submit_headers )

# Extract scan ID from response
scan_id = submit_response.json()["data"]["id"].split("-")[1]

# Wait for 90 seconds with countdown
print("Waiting for 90 seconds...")
for i in range(90, 0, -1):
print(f"Scanning URL: {i} seconds remaining", end="\r")
time.sleep(1)
print("Scanning URL: Done")

# Request report using scan ID
report_url = f"https://www.virustotal.com/api/v3/urls/{scan_id}"
report_headers = {  "accept": "application/json",
              'x-apikey': api_key}
report_response = requests.get(report_url, headers=report_headers)
# Write report to HTML file

file_name = f"report_{scan_id}.txt"
with open(file_name, "w") as f:
f.write(report_response.text)

# Display file name and location
print(f"The report has been written to {file_name} in the current directory.")