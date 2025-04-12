# NGO Blacklist Checker API

A simple Flask API that checks if an NGO is blacklisted based on the blacklisted.json database.

## Setup

1. Make sure you have Python installed
2. Install the required packages:
   ```
   pip install flask
   ```
3. Run the server:
   ```
   python app.py
   ```
   
The server will start at http://127.0.0.1:5000

## API Usage

### Check if an NGO is blacklisted

**Endpoint:** `/api/check-ngo`

**Method:** POST

**Request Body:**
```json
{
  "name": "NGO Name to Check"
}
```

**Response:**

If blacklisted:
```json
{
  "status": "blacklisted",
  "details": {
    "Sr. No.": 1,
    "Name of NPODARPAN": "NGO Name",
    "NPODARPAN ID": "ID123456",
    "Blacklisted By": "Authority",
    "WEF": "Date",
    "Last Updated On": "Date"
  }
}
```

If not blacklisted:
```json
{
  "status": "not blacklisted"
}
```

## Example Usage

Using curl:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"name":"Akhil Sanskritik Sansthan"}' http://127.0.0.1:5000/api/check-ngo
```

Using Python requests:
```python
import requests

response = requests.post(
    "http://127.0.0.1:5000/api/check-ngo",
    json={"name": "Akhil Sanskritik Sansthan"}
)
print(response.json())
``` 