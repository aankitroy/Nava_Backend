# Nava_Backend

# FastAPI Application

This FastAPI application provides a user management system with features for creating and managing admin and organization accounts. The application includes auto-creation of two accounts: a super admin and a regular admin.

## Features

- **User Authentication**: Secure login and token-based authentication.
- **Admin Management**: Create, delete, and manage admin accounts.
- **Organization Management**: Create and manage organizations.

## Auto-Creation of Accounts

Upon starting the application, two accounts are automatically created:

1. **Super Admin Account**

   - **Email**: `super_admin@gmail.com`
   - **Password**: A randomly generated password (printed in the console during startup).

2. **Admin Account**
   - **Email**: `new_admin@example.com`
   - **Password**: A randomly generated password (printed in the console during startup).

These accounts are created to facilitate initial access and management of the application.

## Getting Started

### Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/) for dependency management
- Docker for containerization

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/aankitroy/Nava_Backend
   cd your-repo
   ```

2. **Install Dependencies**

   Use Poetry to install the required dependencies:

   ```bash
   poetry install
   ```

3. **Set Environment Variables**

   Create a `.env` file in the root directory and add the following environment variables:

   ```env
   JWT_SECRET_KEY=your_jwt_secret_key
   JWT_REFRESH_SECRET_KEY=your_jwt_refresh_secret_key
   SUPER_ADMIN_PASSWORD=your_super_admin_password
   FIRST_ADMIN_PASSWORD=your_first_admin_password
   ```

### Running the Application

1. **Activate the Virtual Environment**

   ```bash
   poetry shell
   ```

2. **Start the FastAPI Server**

   Run the following command to start the server:

   ```bash
   uvicorn main:app --reload
   ```

   The application will be available at `http://127.0.0.1:8000`.

3. **Access the API Documentation**

   Visit `http://127.0.0.1:8000/docs` to access the interactive API documentation provided by Swagger UI.

### Running the Application with Docker

1. **Build the Docker Image**

   ```bash
   docker build -t nava-backend .
   ```

2. **Run the Docker Container**

   ```bash
   docker run -d -p 8000:8000 --env-file .env nava-backend
   ```

   The application will be available at `http://127.0.0.1:8000`.

### Testing

Run the test suite using `pytest`:

## Code Structure

- **`app/api_v1/user/service.py`**: Contains the logic for user and admin management.
- **`app/api_v1/org/service.py`**: Contains the logic for organization management.
- **`app/utils/database.py`**: Handles database operations and persistence.

## Important Code Snippets

### Auto-Creation of Accounts

The auto-creation of accounts is handled in the following code snippet:

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact [aankitroy1990@gmail.com](mailto:aankitroy1990@gmail.com).
