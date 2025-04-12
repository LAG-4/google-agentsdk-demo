import requests
import json

def test_blacklisted_ngo():
    # Test a blacklisted NGO
    response = requests.post(
        "http://127.0.0.1:5000/api/check-ngo",
        json={"name": "Akhil Sanskritik Sansthan"}
    )
    print("Testing a blacklisted NGO:")
    print(json.dumps(response.json(), indent=2))
    print()

def test_non_blacklisted_ngo():
    # Test a non-blacklisted NGO
    response = requests.post(
        "http://127.0.0.1:5000/api/check-ngo",
        json={"name": "Random NGO Name That Doesn't Exist"}
    )
    print("Testing a non-blacklisted NGO:")
    print(json.dumps(response.json(), indent=2))
    print()

if __name__ == "__main__":
    print("Make sure the Flask server is running before executing this script")
    print("Run 'python app.py' in a separate terminal if you haven't already\n")
    
    test_blacklisted_ngo()
    test_non_blacklisted_ngo() 