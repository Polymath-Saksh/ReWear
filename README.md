# ReWear ![Django](https://img.shields.io/badge/Django-%23092E20.svg?logo=django&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff) ![Azure](https://img.shields.io/badge/Azure-%230072C6.svg?logo=microsoft-azure&logoColor=white) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?logo=postgresql&logoColor=white) ![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?logo=bootstrap&logoColor=white)

> **Odoo Hackathon 2025 Round 1 (Virtual) – July 12, 2025**

ReWear is a web-based platform designed to promote sustainable fashion and reduce textile waste. It enables users to exchange unused clothing through direct swaps or a point-based redemption system, encouraging the reuse of wearable garments instead of discarding them.

---

## 🌱 Problem Statement

**ReWear – Community Clothing Exchange**

The fashion industry is one of the world's largest pollutants, with millions of tons of textile waste ending up in landfills each year. Many people have unused clothing items sitting in their closets that could be valuable to others. ReWear addresses this problem by creating a community-driven platform where users can:

- Exchange unused clothing through direct swaps
- Redeem items using a point-based system
- Reduce textile waste and promote sustainable fashion
- Build a community around conscious clothing consumption

---

## 💡 Solution Overview

ReWear provides a seamless experience for users to list, browse, and swap clothing items. The platform features a modern UI with animations, point system for redemptions, direct swap requests, and comprehensive admin moderation tools.

### **Key Features**

- **🔐 User Authentication**
  - Email/password signup and login
  - Secure social login (Google, Facebook)
  - Profile management with avatar and bio

- **🏠 Landing Page**
  - Eye-catching platform introduction
  - Calls-to-action: "Start Swapping", "Browse Items", "List an Item"
  - Featured items carousel with animations
  - Environmental impact statistics

- **📊 User Dashboard**
  - Profile details and points balance
  - Uploaded items overview with status tracking
  - Ongoing and completed swaps management
  - Activity timeline and statistics

- **👕 Item Management**
  - Detailed item pages with image galleries
  - Advanced search and filtering system
  - Upload items with multiple images
  - Comprehensive item details (title, description, category, size, condition, tags)

- **🔄 Swap System**
  - Direct swap requests between users
  - Point-based redemption system
  - Swap tracking and status updates
  - User ratings and reviews

- **⚖️ Admin Panel**
  - Moderate and approve/reject item listings
  - Remove inappropriate or spam content
  - User management and suspension tools
  - Platform analytics and reporting

---

## 🚀 Tech Stack

- **Backend:** Django 5.2.4, Django REST Framework
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5.3.0
- **Authentication:** Django Allauth (Email, Google, Facebook)
- **Database:** PostgreSQL (Azure Cosmos DB for Postgres)
- **Cloud Storage:** Microsoft Azure Blob Storage
- **Styling:** Custom CSS with animations, Font Awesome icons
- **Other:** Python-dotenv, CORS headers, Azure storage integration

---

## 🏁 Hackathon Details

- **Event:** Odoo Hackathon 2025 Round 1 (Virtual)
- **Date:** July 12, 2025
- **Team:** Team Kairos

---

## 👥 Team Kairos

### Team Members

- **Aloukik Joshi** (Team Leader)  
    Email: aloukikjoshi@gmail.com  
    GitHub: [aloukikjoshi](https://github.com/aloukikjoshi)

- **Saksham Kumar** (Member)  
    Email: sakshamkumarprasad03@gmail.com  
    GitHub: [Polymath-Saksh](https://github.com/Polymath-Saksh)

- **Nihal Pandey** (Member)  
    Email: nihalvyas1234@gmail.com  
    GitHub: [NihalPandey5060](https://github.com/NihalPandey5060)

## ⚡️ Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL or Azure Cosmos DB for Postgres
- Azure Storage Account (for media files)

### 1. Clone the Repository

```bash
git clone https://github.com/Polymath-Saksh/Team-Kairos.git
cd Team-Kairos
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Database Configuration
DB_HOST=your_postgres_host
DB_PORT=your_postgres_port
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password

# Azure Storage Configuration
AZURE_ACCOUNT_NAME=your_azure_account_name
AZURE_ACCOUNT_KEY=your_azure_account_key
AZURE_CONTAINER=your_azure_container
MEDIA_URL=https://your_azure_account_name.blob.core.windows.net/your_azure_container/

# Django Secret Key (generate a new one for production)
SECRET_KEY=your_django_secret_key
```

### 4. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser

```bash
python manage.py createsuperuser
```

### 6. Collect Static Files

```bash
python manage.py collectstatic
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

Access the application at [http://localhost:8000](http://localhost:8000)

---

## 🛠 Usage Guide

### For Users

1. **Sign Up:** Create an account using email or social login
2. **Browse Items:** Explore available clothing with advanced filters
3. **List Items:** Upload your unused clothing with detailed descriptions
4. **Request Swaps:** Send swap requests to other users
5. **Manage Points:** Earn and spend points for item redemptions
6. **Track Activity:** Monitor your swaps and earnings in the dashboard

### For Admins

1. **Access Admin Panel:** Login with superuser credentials
2. **Moderate Content:** Review and approve new item listings
3. **Manage Users:** Handle user reports and suspensions
4. **Monitor Platform:** View analytics and platform statistics

---


## 📈 Environmental Impact

ReWear contributes to sustainability by:
- **Reducing Textile Waste:** Extending the life cycle of clothing items
- **Lowering Carbon Footprint:** Reducing demand for new clothing production
- **Promoting Circular Economy:** Encouraging reuse and recycling
- **Building Awareness:** Educating users about sustainable fashion

---

## 📞 Contact & Support

- **Team Lead:** Aloukik Joshi (aloukikjoshi@gmail.com)

---
## 🙏 Acknowledgments

- **Odoo Hackathon 2025** for providing the platform and inspiration
- **Microsoft Azure** for cloud services and storage solutions
- **Django Community** for the excellent framework and documentation
- **Bootstrap Team** for the responsive design framework

---

*Made with ❤️ by Team Kairos*
