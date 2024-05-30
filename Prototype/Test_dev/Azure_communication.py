import requests

# Define the endpoint URL and your API key
endpoint_url = "https://dcomdacrbk-openai.openai.azure.com/"
api_key = "1a6633b6dd5b4a919dbdc9460b5c7229"

endpoint_url = "https://dcomdacrbk.openai.azure.com/openai/deployments/connection_test/chat/completions?api-version=2023-03-15-preview"
# Make a GET request to the endpoint
response = requests.get(
    endpoint_url,
    headers={
        "Authorization": f"Bearer {api_key}"
    }
)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print("Connection successful")
    print("Response body:")
    print(response.text)
else:
    # Print error message if request failed
    print(f"Error: {response.status_code} - {response.text}")

