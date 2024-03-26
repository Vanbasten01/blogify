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
    


import json
from bson import ObjectId

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)



import cloudinary.uploader


# Function to remove image from Cloudinary using the public ID
def remove_image_from_cloudinary(image_url):
    try:
        # Extract public ID from the image URL
        public_id = image_url.split("/")[-1].split('.')[0]  # Assuming the public ID is the second-to-last segment of the URL
        print(f"Public ID extracted from image URL: {public_id}")  # Add this line
        # Call destroy method to remove image from Cloudinary
        result = cloudinary.uploader.destroy(public_id)
        print(f"here is the result printed {result}")
        if result['result'] == 'ok':  # Check if the deletion was successful
            print(f"Image deleted successfully: {image_url}")
            return True
          
        else:
            print(f"Failed to delete image: {result['message']}")
            return False
    except Exception as e:
        # Handle any errors
        print(f"Error deleting image from Cloudinary: {e}")
        return False

