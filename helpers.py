import requests

def get_user_info_from_github(access_token):
    print(access_token)
    # Define the headers with the access token for GitHub API
    headers = {
        'Authorization': f'token {access_token}'
    }

    # Make a GET request to the GitHub API's user endpoint
    response = requests.get('https://api.github.com/user', headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response to extract user information
        user_info = response.json()

        return user_info
    else:
        # If the request was not successful, print an error message
        print(f"Failed to retrieve user information from GitHub API: {response.status_code}")
        return None
