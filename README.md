# Ecommerce
Based on the Flask application code and functionalities you've described, here's a summary of what your website is about:

### Summary

Purpose:
   - The website serves as an e-commerce platform where users can browse products, add them to their wishlist, add them to their cart, place orders, and track their order history.

Key Features:
   - User Authentication: Users can register, log in, and log out securely.
   - Product Catalog: Display of products with details like name, price, and seller information.
   - Shopping Cart: Users can add products to their cart and proceed to checkout.
   - Order Placement: Users can place orders from their cart, which are stored in the database.
   - Order Tracking: Users can view their order history and track the progress of their orders.
   - Profile Management: Basic user profile features, such as editing personal information.

Technologies Used:
   - Flask: Python web framework used for backend development.
   - SQLAlchemy: Object-relational mapping (ORM) library for database interactions.
   - Jinja2: Templating engine for rendering HTML templates with Flask.
   - Flask-Login: Provides user session management, login, and logout functionality.
   - Flask-Admin: Administrative interface for managing application data, including CRUD operations on products, orders, etc.
   - Flask-WTF: Integration for handling forms and form validation in Flask applications.
   - Bootstrap: Front-end framework for responsive design and UI components.

Database Integration:
   - Database: Used SQLite to store user data, product information, carts, orders, and order details.

User Experience:
   - Navigation: Clear navigation with links such as product categories, cart, orders, and user profile.
   - Responsive Design: Mobile-friendly design using Bootstrap ensures usability across devices.
   - Security: Implemented user authentication and authorization to protect user data and transactions.

Future Enhancements:
   - Potential features include reviews and ratings for products, advanced search and filtering options, payment gateway integration, and more personalized user experiences.
