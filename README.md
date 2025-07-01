# FixOurCity

<div align="center">
  <h3>Transform Your City Together</h3>
  <p>A community-driven platform for reporting and resolving urban infrastructure issues</p>
</div>

## 📋 Overview

FixOurCity is a web-based platform that empowers citizens to report, track, and resolve urban infrastructure problems in their communities. The platform connects residents, local authorities, and contractors to efficiently address issues like road damage, street lighting problems, and more.

## ✨ Features

- **Issue Reporting**: Users can report infrastructure issues with detailed descriptions, photos, and location data
- **Role-based Access**: Customized dashboards for Public Users, Authorities, Contractors, and Admins
- **Upvoting System**: Community members can upvote issues to increase visibility and priority
- **Issue Tracking**: Real-time status updates as issues move from "New" to "Pending" to "Completed"
- **Contractor Assignment**: Authorities can assign issues to specialized contractors for resolution
- **Performance Metrics**: Contractor leaderboard to track resolution efficiency and quality

## 📊 Issue Categories

- Roads & Highways
- Street Lighting
- Water Supply
- Parks & Recreation
- Waste Management
- Public Transport

## 🔄 Process Flow

1. **Report Issue**: Citizens submit infrastructure problems through the platform
2. **Verification**: Authorities review and verify reported issues
3. **Assignment**: Issues are assigned to appropriate contractors
4. **Resolution**: Contractors fix problems and document the completed work

## 💻 Technology Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Django
- **Database**: SQLite
- **Authentication**: Django Authentication System
- **Template Engine**: Django Templates
- **Maps Integration**: Leaflet.js ,Nominatim API,Browser Geolocation API

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- virtualenv (recommended)
- SQLite

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/ssomeshetty/fixourcity.git
   cd fixourcity
   ```

2. Create and activate a virtual environment
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables
   ```bash
   cp .env.example .env
   # Edit .env with your configuration for database, secret key, etc.
   ```

5. Initialize the database
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser (admin)
   ```bash
   python manage.py createsuperuser
   ```

7. Collect static files
   ```bash
   python manage.py collectstatic
   ```

8. Start the development server
   ```bash
   python manage.py runserver
   ```

9. Access the site
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/


## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 📞 Contact

- Email: bremblue189@gmail.com
