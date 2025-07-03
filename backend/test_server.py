import requests


def test_server():
    """Test if the server is responding."""
    try:
        # Test the root endpoint
        print("Testing root endpoint...")
        response = requests.get("http://localhost:8000/", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

        # Test the docs endpoint
        print("\nTesting docs endpoint...")
        response = requests.get("http://localhost:8000/docs", timeout=10)
        print(f"Status: {response.status_code}")

        # Test the auth register endpoint
        print("\nTesting auth register endpoint...")
        response = requests.get("http://localhost:8000/auth/register", timeout=10)
        print(f"Status: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("Connection error - server might not be running")
    except requests.exceptions.Timeout:
        print("Timeout error - server is not responding")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_server()
