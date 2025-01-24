# Project Overview
This is a backend application built using Django and Django Rest Framework for managing restaurants, menus, menu items, and orders. The system supports four user roles with varying levels of access and responsibilities:
* Normal User: Can register, log in, browse menus, and place orders.
* Owner User: Can create restaurants, menus, menu items, and manage employees and orders for their restaurant.
* Employee User: Can manage menus, menu items, and process orders for the restaurant they are associated with.
* Admin User: Has full control and can manage all aspects of the system from the admin panel.

# Features
* User Authentication and Authorization
* Users can register and log in with their credentials.
* Different user roles have distinct levels of access and permissions.
* Token-based authentication for secure access.
  
# Restaurant Management
* Owner User: Can create and manage restaurants.
* Owner User: Manage employees associated with their restaurant.
* Owner User: Create and manage menus and menu items for their restaurant.
*  Menu Browsing and Ordering
* Normal User: Browse menus of available restaurants.
* Normal User: Place orders for selected items.
* Admin Panel
* Admin User: Has access to an admin panel for comprehensive management.
* Admin User: Can manage users, restaurants, menus, menu items, and orders across the entire system.
  
# Installation

# Clone the repository
git clone https://github.com/ratulhasanshaon/remote_kitchen.git

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser for admin access
python manage.py createsuperuser

# Start the development server
python manage.py runserver

# Database
![DATABASE](../master/database.png)

# Here is the Postman Collection to test the endpoints
[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/12077630-05730ffa-3181-47da-bc05-bf21869bfdf8?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D12077630-05730ffa-3181-47da-bc05-bf21869bfdf8%26entityType%3Dcollection%26workspaceId%3D81bbe03c-9620-4eef-8930-3ad643175d61#?env%5Burl%5D=W3sia2V5IjoiVVJMIiwidmFsdWUiOiJodHRwOi8vMTI3LjAuMC4xOjgwMDAiLCJlbmFibGVkIjp0cnVlfV0=)

Admin Login Credentials
* username: ratulhasan
* password: fredfred1

# Thank You
