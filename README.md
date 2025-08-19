# Kewpie Labs

A web application for bar trivia hosts to create, manage, and distribute quiz content.

## Project Vision

This application helps trivia hosts and authors collaborate on creating quiz content. Users can author individual rounds, combine them into full games, and distribute content to other hosts in the network.

## Core Features

### 1. Round Creation
- **Title**: Auto-incrementing if duplicate exists (e.g., "Test Round", "Test Round 2")
- **Questions**: Variable number (default: 6)
- **Round Label**: Type identifier (1-6, or custom types like "Music", "Visual")
- **Attachments**: Support for images, PDFs, ZIP files
- **Questions & Answers**: Individual fields for each question
- **Database Storage**: Rounds can be attached to multiple games

### 2. Game Creation
- **Date-based**: Default name from hosting date
- **Editable Name**: Customizable game title
- **Round Assembly**: Select from round database
- **Round Preference**: Distinguish new vs. previously used rounds
- **Organization**: Ascending round numbers by default
- **Round Tracking**: Visual indicators for missing round types

### 3. Quiz Management
- **Upcoming Quizzes**: View and manage future games
- **Archive**: Access to past quizzes
- **Content Display**: Formatted view of all rounds and questions
- **Export Ready**: Format optimized for PDF/Google Doc export

## Technical Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (development) → PostgreSQL (production)
- **Frontend**: HTML/CSS/JavaScript with Bootstrap
- **Authentication**: Session-based (Phase 1) → OAuth (Phase 2)
- **File Storage**: Local filesystem → Cloud storage (Phase 2)
- **Deployment**: TBD (Vercel, Fly.io, AWS, Cloudflare options)

## Development Phases

### Phase 1: Foundation ✅ (Complete)
- [x] Git repository initialization
- [x] Virtual environment setup
- [x] Basic Flask application structure
- [x] Database models (User, Round, Game, Question)
- [x] User authentication system
- [x] Round creation functionality
- [x] Basic templates and styling

### Phase 2: Game Management
- [ ] Game creation interface
- [ ] Round selection and assembly
- [ ] Round preference tracking
- [ ] Game date management

### Phase 3: Content Display
- [ ] Quiz viewing interface
- [ ] Archive functionality
- [ ] Content formatting for export
- [ ] Search and filtering

### Phase 4: Advanced Features
- [ ] File attachment handling
- [ ] Export functionality (PDF/Google Doc)
- [ ] Advanced search and filtering
- [ ] User management improvements

### Phase 5: Deployment
- [ ] Production database setup
- [ ] Cloud file storage
- [ ] OAuth integration
- [ ] Deployment configuration

## Database Schema

### Users
- id (Primary Key)
- username
- email
- password_hash
- created_at
- is_active

### Rounds
- id (Primary Key)
- title
- round_label
- created_by (Foreign Key to Users)
- created_at
- attachment_path
- is_active

### Questions
- id (Primary Key)
- round_id (Foreign Key to Rounds)
- question_text
- answer_text
- question_number
- points (optional)

### Games
- id (Primary Key)
- name
- game_date
- created_by (Foreign Key to Users)
- created_at
- is_active

### GameRounds (Junction Table)
- id (Primary Key)
- game_id (Foreign Key to Games)
- round_id (Foreign Key to Rounds)
- round_order
- added_at

## File Structure

```
trivia-creator/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── routes.py            # Flask routes
│   ├── forms.py             # Form definitions
│   ├── auth.py              # Authentication logic
│   └── templates/           # HTML templates
│       ├── base.html
│       ├── auth/
│       ├── rounds/
│       └── games/
├── static/                  # CSS, JS, images
├── uploads/                 # File attachments
├── migrations/              # Database migrations
├── requirements.txt         # Python dependencies
├── config.py               # Configuration
├── run.py                  # Application entry point
└── README.md               # This file
```

## Getting Started

1. Clone the repository
2. Create virtual environment: `python3 -m venv venv`
3. Activate virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Initialize database: `flask db upgrade`
6. Run the application: `python run.py` (runs on http://localhost:5001)

## Current Status

**Phase 1 - Foundation**: ✅ Complete! Basic Flask application with authentication, database models, and core functionality is working.

**Next**: Phase 2 - Game Management (round selection, game assembly, round preference tracking)

## Notes

- Round labels are flexible (1-6 or custom types like "Music", "Visual")
- Round 4 typically visual, Round 2 typically music, but not enforced
- Round numbers indicate difficulty progression
- Authentication required for content creation, homepage public
- File attachments: images, PDFs, ZIP files supported
