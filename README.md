### **Project Notes**

1. **Dockerized Setup**:
   - The project is Dockerized, making it easy to build and run.
   - To start the project, simply run the following command:
     ```bash
     docker-compose up --build
     ```
     This command will build the Docker images and start the containers for the Django application and PostgreSQL database.

2. **Admin Credentials**:
   - The admin username and password are provided in the `.env` file.
     - **Username**: `admin`
     - **Password**: `admin`

3. **Access the Application**:
   - Once the containers are running, you can access the Django application at:
     ```
     http://localhost:8000
     ```
   - Use the admin credentials to log in to the Django admin panel.
