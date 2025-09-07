# NICE Cruise Management System

A full-stack database-driven application developed for **CS-GY 6083 Principles of Database System**. The system models and manages operations for NICE (Nature International Cruise Excellence), a cruise line operating across 35 ports in the USA, Canada, Mexico, and the Caribbean.

## Features
- **Passenger Portal**: Book trips, staterooms, and packages; view itineraries; update profiles.
- **Admin Dashboard**: Manage staterooms, prices, entertainment, and passenger information.
- **Dynamic Pricing**: Stateroom costs vary by trip and season.
- **Secure Access**:
  - Password hashing with PBKDF2-SHA256
  - SQLAlchemy ORM for database interaction
  - Input sanitization against XSS/SQL injection
  - Role-based session management
  - CORS restrictions for API requests

## Tech Stack
- **Frontend**: Vue.js, Vite, JavaScript
- **Backend**: Python (Flask), Postman (API testing)
- **Database**: SQLite (designed via Oracle Data Modeler)
- **Tools**: Visual Studio Code, GitHub, SQLAlchemy ORM

## Database Schema
- Entities include: Users, Groups, Passengers, Trips, Staterooms, Restaurants, Entertainment, Packages, Payments, Invoices, and Ports.
- Relationships capture booking, payments, group associations, and trip-specific amenities.

## Example Queries
- **Trip & Ports**: Identify start and end ports with city/country details.
- **High-Value Customers**: Find passengers/groups with above-average payments.
- **Pricing Insights**: Compare staterooms above average trip pricing.
- **User Overview**: UNION queries for admins and passengers.
- **Top-N Analysis**: Find the 10 lowest-priced staterooms for a trip.

## Lessons Learned
- Hands-on experience with **full-stack integration** (Vue.js + Flask + SQLite).
- Importance of **team collaboration** and clear API communication.
- Systematic debugging for smooth front-end/back-end integration.

---

### Team
- Chenghao Yang (cy2668)  
- Yihua Yang (yy5028)  
- Ziyi Liang (zl5604)

📅 **Submitted**: Dec 8, 2024
