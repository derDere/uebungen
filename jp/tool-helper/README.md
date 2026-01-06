# Tool Helper

A full-stack web application for managing tools and their associated checklists. Built with FastAPI (Python) backend and Svelte (TypeScript) frontend.

## Features

- **Tool Management**: Create, view, and manage tools
- **Checklist System**: Create checklists for each tool with checkable points
- **Template System**: Create reusable checklist templates with point templates
- **Template Instantiation**: Generate new checklists from templates
- **Live Updates**: Checkbox states update immediately to the database
- **Search & Filter**: Search across tools, checklists, and points
- **Export**: Export data in JSON, YAML, CSV, and Markdown formats
- **Alphabetical Sorting**: Checklist points are automatically sorted alphabetically

## Technology Stack

- **Backend**: FastAPI (Python) + SQLAlchemy + SQLite
- **Frontend**: Svelte SPA + TypeScript + Vite
- **Database**: SQLite

## Project Structure

```
tool-helper/
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── main.py          # Application entry point
│   │   ├── database.py      # Database configuration
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── crud.py          # Database operations
│   │   ├── seed_data.py     # Sample data seeding
│   │   └── routers/         # API route handlers
│   ├── requirements.txt
│   └── tool_helper.db       # SQLite database (created on first run)
├── frontend/                 # Svelte frontend
│   ├── src/
│   │   ├── lib/
│   │   │   ├── api.ts       # API client
│   │   │   ├── types.ts     # TypeScript interfaces
│   │   │   └── components/  # Svelte components
│   │   ├── App.svelte       # Main application
│   │   └── app.css          # Global styles
│   └── package.json
├── erd.md                    # Database ERD diagrams
├── questions.md              # Requirements documentation
└── CLAUDE.md                 # Claude Code guidance
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 20+
- npm

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

   The backend will be available at `http://localhost:8000`

   - API docs: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/health`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install npm dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

### First Run

On the first startup, the backend will automatically:
- Create the SQLite database
- Set up all tables
- Populate sample data (tools, templates, checklists)

## API Endpoints

### Tools
- `GET /tools/` - List all tools
- `POST /tools/` - Create a tool
- `GET /tools/{id}` - Get tool with checklists
- `PUT /tools/{id}` - Update tool
- `DELETE /tools/{id}` - Delete tool

### Checklists
- `GET /checklists/` - List checklists (optional: `?tool_id=1`)
- `POST /checklists/` - Create checklist
- `POST /checklists/from-template/{template_id}` - Create from template
- `GET /checklists/{id}` - Get checklist with points
- `PUT /checklists/{id}` - Update checklist
- `DELETE /checklists/{id}` - Delete checklist
- `PATCH /checklists/{id}/points/{point_id}/toggle` - Toggle point
- `POST /checklists/{id}/points` - Add point to checklist
- `DELETE /checklists/{id}/points/{point_id}` - Remove point

### Templates
- `GET /templates/checklist` - List checklist templates
- `POST /templates/checklist` - Create checklist template
- `GET /templates/point` - List point templates
- `POST /templates/point` - Create point template
- `POST /templates/checklist/{template_id}/points/{point_id}` - Link point to template

### Search & Export
- `GET /checklists/search/{query}` - Search all entities
- `GET /export/json` - Export as JSON
- `GET /export/yaml` - Export as YAML
- `GET /export/csv` - Export as CSV
- `GET /export/markdown` - Export as Markdown

## Usage

1. **Create Tools**: Add tools in the sidebar
2. **Select a Tool**: Click on a tool to view its checklists
3. **Create Checklists**: Create checklists manually or from templates
4. **Manage Points**: Check/uncheck points, add new points
5. **Templates**: Click "Show Templates" to create and manage templates
6. **Search**: Use the search bar in the header
7. **Export**: Use the export panel to download data

## Data Model

See `erd.md` for detailed entity-relationship diagrams and `CLAUDE.md` for architectural overview.

### Key Relationships

- Tool (1) → (N) CheckList
- CheckListTemplate (1) → (N) CheckList
- CheckList (M) ↔ (N) CheckListPoint (many-to-many)
- CheckListTemplate (M) ↔ (N) CheckListPointTemplate (many-to-many)
- CheckListPointTemplate (1) → (N) CheckListPoint

## Development

### Backend Development

The backend uses:
- FastAPI for the REST API
- SQLAlchemy for ORM
- Pydantic for validation
- SQLite for database

To modify the database schema, edit `models.py` and delete `tool_helper.db` to recreate.

### Frontend Development

The frontend uses:
- Svelte for reactive UI components
- TypeScript for type safety
- Vite for fast development and building
- Simple CSS (no framework)

API calls are proxied through Vite (see `vite.config.ts`).

## License

MIT
