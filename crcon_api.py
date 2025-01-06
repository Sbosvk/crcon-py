import requests
from urllib.parse import urlencode
from endpoints import endpoints  # Import the endpoints module


class API:
    def __init__(self, base_url, token=None):
        """
        Initialize the API instance.

        :param base_url: Base URL of the API
        :param token: Bearer token for authentication
        """
        self.base_url = base_url
        self.token = token

    def request(self, endpoint, method="GET", args=None, debug=False):
        """
        Send an API request.

        :param endpoint: API endpoint
        :param method: HTTP method (GET or POST)
        :param args: Request parameters
        :param debug: If True, return the full response
        :return: Parsed API response
        """
        args = args or {}
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        # Make the request
        response = None
        if method == "GET":
            url += f"?{urlencode(args)}" if args else ""
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=args, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        # Handle the response
        try:
            response_data = response.json()
        except ValueError:
            response_data = response.text

        if not response.ok:
            raise requests.exceptions.HTTPError(f"HTTP error {response.status_code}: {response.reason}")

        if isinstance(response_data, dict) and response_data.get("failed"):
            raise ValueError(response_data.get("error", "API request failed."))

        return response_data if debug else response_data.get("result", response_data)


# Dynamically add methods for all endpoints
def create_endpoint_method(endpoint, methods, allowed_args):
    """
    Generate a method for a specific endpoint.

    :param endpoint: Endpoint name
    :param methods: Allowed HTTP methods
    :param allowed_args: Allowed arguments for the endpoint
    """
    def endpoint_method(self, args=None, method=None):
        args = args or {}
        selected_method = method or (methods[0] if "GET" in methods else "POST")

        # Validate arguments
        if "kwargs" not in allowed_args:
            invalid_args = [arg for arg in args if arg not in allowed_args]
            if invalid_args:
                raise ValueError(f"Invalid arguments for {endpoint}: {', '.join(invalid_args)}")

        # Validate HTTP method
        if selected_method not in methods:
            raise ValueError(f"Method {selected_method} not allowed for {endpoint}")

        # Perform the request
        return self.request(endpoint, selected_method, args)

    endpoint_method.__name__ = endpoint
    endpoint_method.__doc__ = f"""
    Dynamically generated method for the '{endpoint}' endpoint.

    :param args: Arguments to pass to the endpoint ({', '.join(allowed_args) if allowed_args else 'No arguments allowed'}).
    :param method: HTTP method to use ({', '.join(methods)}).
    """
    return endpoint_method


# Add all endpoints as methods to the API class
for endpoint in endpoints:
    endpoint_name = endpoint["endpoint"]
    methods = endpoint["methods"]
    allowed_args = endpoint["allowed_args"]
    setattr(API, endpoint_name, create_endpoint_method(endpoint_name, methods, allowed_args))


# Example Usage
if __name__ == "__main__":
    # Initialize the API
    api = API("https://your-api-url.com", token="your-api-token")

    # Example call to dynamically generated method
    try:
        response = api.get_players()
        print("Response:", response)
    except Exception as e:
        print("Error:", e)
