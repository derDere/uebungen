# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tool management application with hierarchical checklist system. The app allows users to manage tools, create checklists from templates, and track completion status.

**Tech Stack (Planned):**
- Frontend: Svelte SPA with TypeScript
- Backend: FastAPI (Python)
- Database: SQLite

## Data Model Architecture

The application uses a template-instance pattern with the following entity hierarchy:

### Core Entities

**TOOL** → **CHECK_LIST** → **CHECK_LIST_POINT**

Each tool has multiple checklists, each checklist contains multiple points that can be checked off.

### Template System

**CHECK_LIST_TEMPLATE** ↔ **CHECK_LIST_POINT_TEMPLATE** (many-to-many)

Templates define reusable checklist structures. When a template is instantiated, it creates a new checklist with points based on the template's point definitions.

### Key Relationships

- `TOOL` (1) → (N) `CHECK_LIST`: Each tool owns multiple checklists
- `CHECK_LIST_TEMPLATE` (1) → (N) `CHECK_LIST`: Templates can be used to create multiple checklist instances
- `CHECK_LIST` ↔ `CHECK_LIST_POINT`: Many-to-many via `CHECK_LIST_CHECK_LIST_POINT` junction table
- `CHECK_LIST_TEMPLATE` ↔ `CHECK_LIST_POINT_TEMPLATE`: Many-to-many via `CHECK_LIST_TEMPLATE_POINT_TEMPLATE` junction table
- `CHECK_LIST_POINT_TEMPLATE` (1) → (N) `CHECK_LIST_POINT`: Each point instance must reference its template (but points can also be created independently)

### Junction Tables

**CHECK_LIST_CHECK_LIST_POINT**
- `check_list_id` (FK)
- `check_list_point_id` (FK)
- Allows points to be shared across multiple checklists

**CHECK_LIST_TEMPLATE_POINT_TEMPLATE**
- `check_list_template_id` (FK)
- `check_list_point_template_id` (FK)
- `sort_order` (int) - defines ordering within template
- Links point templates to checklist templates

## Feature Requirements

### Core Functionality
- CRUD operations for all entities (Tools, Checklists, Templates, Points)
- Template creation and editing
- Instantiate checklists from templates
- Check/uncheck points with live database updates
- Independent point creation (not just from templates)

### UI/UX
- Nested display: Tool → Checklist → Points
- Live status updates (no manual save button needed)
- Alphabetical sorting of checklist points by default

### Data Management
- Export functionality: CSV, Markdown, YAML, and JSON formats
- Search and filter across Tools, Checklists, and Points
- Automatic `created_at` and `updated_at` timestamps

## Database Schema Notes

All entities include:
- `id` (int, PK)
- `name` (varchar)
- `status` (enum) - implementation can use any reasonable status values (e.g., active/inactive, draft/published)
- `created_at` (datetime)
- `updated_at` (datetime)

Additional fields:
- `CHECK_LIST_POINT.is_checked` (boolean)
- `CHECK_LIST_POINT_TEMPLATE.datatype` (varchar) - can support text, number, boolean, etc.
- Foreign keys as shown in erd.md

See erd.md for complete ERD diagrams (both conceptual and relational models).

## Development Guidelines

- Use TypeScript for type safety in the frontend
- Implement proper foreign key constraints in SQLite
- Ensure junction tables properly enforce referential integrity
- Templates are immutable after instantiation (changes to template don't affect existing checklists)
- Points can exist independently without a template reference (`check_list_point_template_id` should be nullable)
