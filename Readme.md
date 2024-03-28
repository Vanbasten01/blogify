# Blogify

Blogify is a Flask-based web application for creating and managing a personal blog. It provides an intuitive interface for users to write, edit, and publish blog posts, as well as interact with other users through likes, comments, and social sharing.

## Features

- **User Authentication:** Users can sign up, log in, and log out securely.
- **Create, Edit, and Delete Blog Posts:** Users can create new blog posts, edit existing ones, and delete posts.
- **View Blogs:** Visitors can view all published blog posts.
- **Interact with Blogs:** Users can like, comment on, and share blog posts on social media platforms.
- **Like and Comment on Comments:** Users can interact with comments by liking, commenting on, and deleting their own comments.
- **Profile Management:** Users can update their profile credentials, add a profile picture, and delete their profile.
- **Filtering Blogs by Categories:** Users can filter blogs by categories to find posts related to specific topics.
- **Search using a Keyword:** Users can search for blogs using a keyword to find posts related to specific topics.
- **API Endpoints for Application-to-Application Interaction:** Other applications can interact with Blogify's API endpoints to retrieve all blogs or a specific blog using JWT token-based authentication.


## Installation

1. Clone the repository:

```bash
git clone https://github.com/Vanbasten01/bgilogify.git
cd Blogify

2. Set up a virtual environment (optional but recommended):
python3 -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows

3. Install the required dependencies:
pip install -r requirements.txt

4. Set up the environment variables:
Create a .env file in the root directory of your project and add the following variables:

# GitHub OAuth credentials
GITHUB_CLIENT_ID="YOUR_GITHUB_CLIENT_ID"
GITHUB_CLIENT_SECRET="YOUR_GITHUB_CLIENT_SECRET"

# Flask Secret Key
FLASK_SECRET="YOUR_FLASK_SECRET_KEY"

# Google OAuth2 credentials
OAUTH2_CLIENT_ID="YOUR_GOOGLE_OAUTH2_CLIENT_ID"
OAUTH2_CLIENT_SECRET="YOUR_GOOGLE_OAUTH2_CLIENT_SECRET"
OAUTH2_META_URL="https://accounts.google.com/.well-known/openid-configuration"

# Cloudinary credentials
CLOUDINARY_CLOUD_NAME="YOUR_CLOUDINARY_CLOUD_NAME"
CLOUDINARY_API_KEY="YOUR_CLOUDINARY_API_KEY"
CLOUDINARY_API_SECRET="YOUR_CLOUDINARY_API_SECRET"

# MongoDB URI
MONGO_DB_URI="YOUR_MONGODB_URI"

Replace YOUR_GITHUB_CLIENT_ID, YOUR_GITHUB_CLIENT_SECRET, and so on with your actual credentials obtained from their respective services.

Run the application:
python app.py


5. Access the application in your web browser at http://localhost:5000.

## Technologies Used

- Flask: Python web framework used for building the backend of the application.
- MongoDB: NoSQL database used for storing blog data.
- Cloudinary: Cloud-based service used for managing and serving images.
- HTML: Markup language used for creating the structure of web pages.
- CSS: Styling language used for enhancing the presentation of web pages.
- JavaScript: Programming language used for adding interactivity and dynamic behavior to web pages.


[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/fouad-yasin-76a489270/)


