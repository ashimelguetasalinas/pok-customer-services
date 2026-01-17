import requests
import json

try:
    response = requests.get("http://localhost:8000/api/inquiries/")
    data = response.json()
    
    print("Keys in root:", data.keys())
    
    if "results" in data:
        if len(data["results"]) > 0:
            first_item = data["results"][0]
            print("First item keys:", first_item.keys())
            print("First item sample:", json.dumps(first_item, indent=2))
        else:
            print("Results list is empty")
    elif isinstance(data, list):
        if len(data) > 0:
            first_item = data[0]
            print("First item keys:", first_item.keys())
        else:
            print("List is empty")
    else:
        print("Unknown structure")

except Exception as e:
    print(e)
