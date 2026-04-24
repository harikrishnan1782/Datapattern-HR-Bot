# DataPattern HR Automation Agent 🏢

A unified, AI-powered HR automation platform that streamlines offer letter generation and expense reimbursement processing using an intelligent Streamlit interface.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Features in Detail](#features-in-detail)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## Overview

DataPattern HR Automation Agent is a comprehensive HR automation solution designed to simplify and accelerate HR operations. This application combines two powerful modules:

1. **Offer Letter Generator** - Automates the creation of professional offer letters with customizable templates
2. **Expense Reimbursement System** - Streamlines the processing and approval of employee expense claims

Built with Streamlit for an intuitive user interface and powered by Python for robust backend processing, this system leverages Google Cloud APIs for authentication and document management.

## Features

### 🎯 Offer Letter Generator
- **Template-Based Generation** - Use pre-designed DOCX templates for consistency
- **Automated Field Population** - Intelligently populate offer letters with candidate information
- **Document Preview** - View generated documents before downloading
- **PDF/DOCX Export** - Export generated offers in multiple formats
- **Batch Processing** - Generate multiple offers efficiently
- **Data Validation** - Ensure all required fields are filled before generation

### 💸 Expense Reimbursement System
- **Claim Submission** - Easy-to-use interface for employees to submit expenses
- **Multi-Category Support** - Support for various expense categories (travel, meals, accommodation, etc.)
- **Receipt Management** - Attach and manage receipt documents
- **Approval Workflow** - Streamlined approval process with manager verification
- **Status Tracking** - Real-time tracking of claim status from submission to reimbursement
- **Audit Trail** - Complete history of all claims and approvals for compliance

### 🔧 General Features
- **Unified Dashboard** - Single portal for both offer generation and reimbursement
- **Secure Authentication** - OAuth integration with Google Cloud
- **Responsive Design** - Works seamlessly across desktop and tablet devices
- **Environment-Based Configuration** - Flexible configuration through environment variables
- **Modular Architecture** - Easily extendable codebase for future enhancements

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Frontend** | Streamlit | ≥ 1.35.0 |
| **Backend** | Python | 3.8+ |
| **Cloud APIs** | Google Cloud API | Latest |
| **Authentication** | OAuth 2.0 | - |
| **Document Processing** | python-docx | Included |
| **Environment Management** | python-dotenv | ≥ 1.0.0 |

### Language Composition
- **Python**: 83.2%
- **CSS**: 16.8%

## Project Structure

```
Datapattern-HR-Bot/
├── app.py                                    # Main application entry point
├── requirements.txt                          # Python dependencies
├── .gitignore                               # Git ignore rules
│
├── core/                                     # Core business logic
│   ├── __init__.py
│   ├── offer_processor.py               # Offer letter generation logic
│   ├── reimbursement_processor.py       # Expense reimbursement logic
│   └── utils.py                          # Common utilities
│
├── modules/                                  # Feature modules
│   ├── offer_letter/
│   │   ├── __init__.py
│   │   ├── DataPattern Offer Letter_sample.docx  # Template file
│   │   └── generator.py                  # Letter generation functions
│   │
│   └── expense/
│       ├── __init__.py
│       └── processor.py                  # Expense processing functions
│
├── ui/                                       # UI Components & Rendering
│   ├── __init__.py
│   ├── offer_ui.py                      # Offer letter UI component
│   ├── reimburse_ui.py                  # Reimbursement UI component
│   └── render.py                         # Main UI routing
│
└── assets/                                   # Static assets
    ├── styles.css                       # Custom Streamlit styling
    └── images/                          # Logo and icons
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Google Cloud Project with OAuth 2.0 credentials
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/harikrishnan1782/Datapattern-HR-Bot.git
cd Datapattern-HR-Bot
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory:

```bash
# Google Cloud Configuration
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8501/

# Application Configuration
APP_ENV=development
DEBUG=False

# API Keys
GOOGLE_API_KEY=your_api_key_here
```

## Configuration

### Google Cloud Setup

1. **Create a Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable the Google Sheets API and Google Drive API

2. **Create OAuth 2.0 Credentials**
   - Navigate to "Credentials" in the left sidebar
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - Select "Web application"
   - Add `http://localhost:8501/` to authorized redirect URIs
   - Copy the Client ID and Client Secret
   - Paste them into your `.env` file

3. **Set Up Service Account (Optional)**
   - Create a Service Account for backend operations
   - Download the JSON key file
   - Place it in the project root and reference in `.env`

## Usage

### Running the Application

```bash
# Ensure virtual environment is activated
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Offer Letter Generator

1. Navigate to the **"📝 Offer Letter Generator"** tab
2. Fill in the candidate information:
   - Name, Position, Department
   - Salary, Start Date, Benefits
   - Custom terms (if applicable)
3. Click **"Preview"** to review the generated offer
4. Click **"Download"** to save as DOCX or PDF
5. Optionally, email the offer directly through the application

### Expense Reimbursement

1. Navigate to the **"💸 Expense Reimbursement"** tab
2. Submit a new expense claim:
   - Select expense category
   - Enter amount and date
   - Add receipt/documentation
   - Add notes or comments
3. Submit the claim for manager approval
4. Track approval status in the "My Claims" section
5. Receive reimbursement notification upon approval

## Features in Detail

### Offer Letter Generation Pipeline

```
User Input
    ↓
Data Validation
    ↓
Template Loading
    ↓
Field Population
    ↓
Document Rendering
    ↓
Preview/Download
```

### Expense Reimbursement Workflow

```
Employee Submission
    ↓
Initial Validation
    ↓
Manager Review
    ↓
Approval/Rejection
    ↓
Finance Processing
    ↓
Reimbursement
```

## Architecture

### Design Patterns

- **Modular Design** - Separation of concerns with distinct modules for different features
- **MVC Pattern** - Clear separation between UI (views), business logic (controllers), and data (models)
- **Session State Management** - Efficient state handling using Streamlit's session_state
- **Configuration Management** - Environment-based configuration for flexibility

### Authentication Flow

```
User Login (Google OAuth 2.0)
    ↓
Token Exchange
    ↓
User Verification
    ↓
Session Creation
    ↓
Access to Dashboard
```

## Future Enhancements

- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Integration with HR management systems (Workday, SAP)
- [ ] Mobile application
- [ ] Advanced reporting and compliance features
- [ ] AI-powered document processing
- [ ] Real-time collaboration features

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError` when running the app
- **Solution**: Ensure virtual environment is activated and all dependencies are installed
  ```bash
  pip install -r requirements.txt
  ```

**Issue**: OAuth credentials not working
- **Solution**: Verify `.env` file has correct credentials and redirect URI matches Google Cloud settings

**Issue**: Template file not found
- **Solution**: Ensure the template DOCX file is in `modules/offer_letter/` directory

**Issue**: Streamlit port already in use
- **Solution**: Run on a different port
  ```bash
  streamlit run app.py --server.port=8502
  ```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure:
- Code follows PEP 8 style guidelines
- All functions have docstrings
- New features include appropriate tests
- Documentation is updated

## Code Style

This project follows PEP 8 guidelines. Use the following tools for linting:

```bash
# Install linting tools
pip install pylint flake8 black

# Run linters
pylint *.py
flake8 .
black --check .
```

## Performance Optimization

- **Document Generation**: Caches templates to reduce load time
- **API Calls**: Implements rate limiting and request batching
- **UI Rendering**: Uses Streamlit caching for expensive computations

```python
@st.cache_data
def load_template():
    # Cached function execution
    pass
```

## Security Considerations

- **Sensitive Data**: Never hardcode credentials; always use environment variables
- **Authentication**: OAuth 2.0 prevents unauthorized access
- **Data Encryption**: All API communications use HTTPS
- **Input Validation**: All user inputs are validated before processing
- **Audit Logging**: All actions are logged for compliance and debugging

## Support

For issues, questions, or suggestions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/harikrishnan1782/Datapattern-HR-Bot/issues)
3. Create a new GitHub Issue with:
   - Clear problem description
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment details (Python version, OS, etc.)

## Changelog

### Version 1.0.0 (2026-04-23)
- Initial release
- Offer Letter Generator module
- Expense Reimbursement System module
- OAuth 2.0 authentication
- Unified Streamlit dashboard

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- **Hari Krishnan** (@harikrishnan1782) - Creator and Maintainer
- **Anand kumar** - Creater and Maintainer

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Cloud APIs](https://cloud.google.com/)
- Inspired by modern HR automation best practices

---

**Last Updated**: April 23, 2026

For more information and updates, visit the [repository](https://github.com/harikrishnan1782/Datapattern-HR-Bot)
