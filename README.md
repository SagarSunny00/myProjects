# myProjects

 Django REST API: User, Client, and Project Management
Python Version Django Version DRF Version License

This project provides a robust Django REST API for managing users, clients, and projects. It utilizes Django REST Framework (DRF) to offer powerful, flexible, and scalable API endpoints, including support for nested serializers and user-specific data retrieval.

✨ Features
User Management: Integrates with Django's built-in User model.
Client Management:
Register new clients.
Fetch, edit, and delete client information.
Retrieve client details with nested projects.
Project Management:
Add new projects for a specific client.
Assign multiple users to a single project.
Retrieve projects assigned to the currently logged-in user.
Authentication: Secure API access using Token Authentication.
Auditing: Automatically tracks created_at, updated_at, created_by, and updated_by for Clients and Projects.
Nested Serializers: Client detail view includes a list of associated Projects.
📋 Prerequisites
Before you begin, ensure you have the following installed on your system:

Python 3.9+:

bash

python --version
pip (Python Package Installer):

bash

pip --version
Git: ```bash git --version

🚀 Getting Started
Follow these steps to get your development environment up and running.

1. Clone the Repository
First, clone this repository to your local machine:

bash

git clone <repository_url> # Replace <repository_url> with your GitHub repo URL
cd Web # Navigate into the root project directory
2. Create a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

bash

python -m venv venv
3. Activate the Virtual Environment
On macOS/Linux:
bash

source venv/bin/activate
On Windows (Command Prompt):
bash

venv\Scripts\activate.bat
On Windows (PowerShell):

bash

venv\Scripts\Activate.ps1
4. Install Dependencies
Install all required Python packages using pip:

bash

pip install Django djangorestframework djangorestframework-simplejwt python-dotenv
After installation, you can generate a requirements.txt file for easy dependency management in the future:

bash

pip freeze > requirements.txt
5. Configure Environment Variables
Create a .env file in the root Web/ directory (where manage.py is located) to store your sensitive configuration.

bash

touch .env
Open the .env file and add your Django SECRET_KEY. You can generate a strong key using the command below:

bash

# Run this command in your terminal and copy the output
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
Paste the generated key into your .env file:

DJANGO_SECRET_KEY='your_generated_secret_key_here'
6. Run Database Migrations
Apply the initial database migrations and create the necessary tables for your models:

bash

python manage.py makemigrations management
python manage.py migrate
7. Create a Superuser
Create a superuser account. This will allow you to access the Django Admin panel and initially manage users, clients, and projects.

bash

python manage.py createsuperuser
Follow the prompts to set up a username, email (optional), and password.

8. Run the Development Server
Start the Django development server:

bash

python manage.py runserver
The API will now be accessible at http://127.0.0.1:8000/. You can visit http://127.0.0.1:8000/ in your browser, and it will redirect you to http://127.0.0.1:8000/api/.

🔑 API Authentication
This API uses Token Authentication. To access most endpoints, you first need to obtain a token by providing your username and password.

Obtain an Authentication Token
Endpoint: POST /api-token-auth/
Headers:
Content-Type: application/json
Body (JSON):

json

{
    "username": "your_username",
    "password": "your_password"
}
Example (using curl):

bash

curl -X POST -H "Content-Type: application/json" \
-d '{"username": "codespace", "password": "your_superuser_password"}' \
http://127.0.0.1:8000/api-token-auth/
Successful Response:
 
json

{
    "token": "59f0cb0e6df68e37d115566e717a21de24bde634" # Your unique token
}
IMPORTANT: Copy this token. You will use it for all subsequent authenticated API requests.
Using the Token
For all protected API endpoints, include the token in the Authorization header:

Authorization: Token YOUR_COPIED_TOKEN_HERE

📊 API Endpoints
Below are the available API endpoints. All requests that modify data (POST, PUT, PATCH, DELETE) require a Content-Type: application/json header in addition to the Authorization header.

Base URL: http://127.0.0.1:8000/api/

Clients
1. List all Clients
URL: /clients/
Method: GET
Authentication: Required
Example (curl):
 
bash

curl -X GET -H "Authorization: Token YOUR_TOKEN" \
http://127.0.0.1:8000/api/clients/    ```
Sample Response:
 
json

[
    {
        "id": 1,
        "client_name": "Nimap",
        "created_at": "2019-12-24T11:03:55.931739+05:30",
        "created_by": "Rohit",
        "updated_at": "2019-12-24T11:03:55.931739+05:30",
        "updated_by": "Rohit"
    }
]
2. Create a New Client
URL: /clients/
Method: POST
Authentication: Required
Body (JSON):
 
json

{
    "client_name": "Company A"
}
Example (curl):
 
bash

curl -X POST -H "Content-Type: application/json" \
-H "Authorization: Token YOUR_TOKEN" \
-d '{"client_name": "Company A"}' \
http://127.0.0.1:8000/api/clients/
Sample Response:

json

{
    "id": 3,
    "client_name": "Company A",
    "created_at": "2019-12-24T11:03:55.931739+05:30",
    "created_by": "Rohit",
    "updated_at": "2019-12-24T11:03:55.931739+05:30",
    "updated_by": "Rohit"
}
3. Retrieve Client Info (with nested Projects)
URL: /clients/:id/
Method: GET
Authentication: Required
Example (curl):
 
bash

curl -X GET -H "Authorization: Token YOUR_TOKEN" \
http://127.0.0.1:8000/api/clients/1/ # Replace 1 with actual client ID
Sample Response:
 
json

{
    "id": 1,
    "client_name": "Nimap",
    "created_at": "2019-12-24T11:03:55.931739+05:30",
    "created_by": "Rohit",
    "updated_at": "2019-12-24T11:03:55.931739+05:30",
    "updated_by": "Rohit",
    "projects": [
        {
            "id": 1,
            "project_name": "Project A"
        }
    ]
}
4. Update Client Info
URL: /clients/:id/
Method: PUT (full update) / PATCH (partial update)
Authentication: Required
Body (JSON):
 
json

{
    "client_name": "Updated Company Name"
}
Example (curl - PATCH):
 
bash

curl -X PATCH -H "Content-Type: application/json" \
-H "Authorization: Token YOUR_TOKEN" \    -d '{"client_name": "Updated Company Name"}' \
http://127.0.0.1:8000/api/clients/1/ # Replace 1 with actual client ID
Sample Response: (Similar to Create, with updated client_name and updated_at/updated_by)
5. Delete Client
URL: /clients/:id/
Method: DELETE
Authentication: Required
Example (curl):
 
bash

curl -X DELETE -H "Authorization: Token YOUR_TOKEN" \
http://127.0.0.1:8000/api/clients/1/ # Replace 1 with actual client ID
Successful Response: HTTP 204 No Content
Projects
1. Create a New Project for a Client
URL: /clients/:id/projects/ (where :id is the Client ID)* Method: POST
Authentication: Required
Body (JSON):
 
json

{
    "project_name": "Project Alpha",
    "users": [1, 2] # List of existing User IDs to assign to this project
}
Example (curl):
 
bash

curl -X POST -H "Content-Type: application/json" \
-H "Authorization: Token YOUR_TOKEN" \
-d '{"project_name": "Project Alpha", "users": [1, 2]}' \
http://127.0.0.1:8000/api/clients/1/projects/ # Replace 1 with actual client ID
Sample Response:
 
json

{
    "id": 3,
    "project_name": "Project Alpha",
    "client": "Nimap",
    "users": [
        {
            "id": 1,
            "name": "Rohit"
        },
        {
            "id": 2,
            "name": "Ganesh"
        }
    ],
    "created_at": "2023-10-27T10:00:00.000000Z",
    "created_by": "Nimap_1",
    "updated_at": "2023-10-27T10:00:00.000000Z",
    "updated_by": "Nimap_1"
}
2. List Projects Assigned to the Logged-in User
URL: /projects/
Method: GET
Authentication: Required
Example (curl):
 
bash

curl -X GET -H "Authorization: Token YOUR_TOKEN" \
http://127.0.0.1:8000/api/projects/
Sample Response:
 
json

[
    {
        "id": 1,
        "project_name": "Project A",
        "client": "Infotech",
        "users": [
            {                    "id": 1,
                "name": "Rohit"
            }
        ],
        "created_at": "2019-12-24T11:03:55.931739+05:30",
        "created_by": "Ganesh",
        "updated_at": "2019-12-24T11:03:55.931739+05:30",
        "updated_by": "Ganesh"
    }
]
🛠️ Testing with Other Tools
You can use various API client software to test these endpoints:

Postman: A popular API testing tool.

Create a new request.
Set the HTTP method (GET, POST, PUT, DELETE, PATCH).
Enter the URL.
Go to the "Headers" tab and add Content-Type: application/json (for requests with a body) and Authorization: Token YOUR_TOKEN.
For POST/PUT/PATCH, go to the "Body" tab, select "raw" and "JSON", then paste your JSON data.
Click "Send".
Insomnia: Another excellent API client similar to Postman. The steps are largely identical.

VS Code Extensions: Many extensions like "REST Client" allow you to send HTTP requests directly from .http files within VS Code.

💡 Future Enhancements
This project can be further enhanced with:

User Registration API: An endpoint for users to register themselves directly via API, instead of only through Django Admin.
JWT Authentication: Migrate from Token Authentication to JSON Web Tokens (JWT) for stateless authentication.
Granular Permissions: Implement object-level or role-based permissions (e.g., only project creators can modify their projects, or only specific user roles can delete clients).
API Documentation: Integrate tools like drf-spectacular or drf-yasg for automatic OpenAPI/Swagger documentation generation.
Pagination: Implement proper pagination for large list endpoints to improve performance and usability.
Filtering & Searching: Add capabilities to filter and search clients and projects based on various criteria.
Comprehensive Testing: Add unit and integration tests for models, serializers, and views.
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

Note: Remember to replace <repository_url>, YOUR_TOKEN, and other placeholder values with your actual data.