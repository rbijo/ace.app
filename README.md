# ACE (AI Companion for Education)

ACE is an AI-powered education companion designed to assist students in managing academic tasks, processing syllabus documents, building timetables, generating study plans, and dynamically adapting schedules based on ongoing progress.

---

## Current Development State

**Current State**: `Planning / Foundation`

This repository is currently under initial structural foundation and setup. Subsystem implementations will follow planned backlog issues.

---

## Repository Structure

The ACE repository is organized into distinct logical components:

```text
ace.app/
├── frontend/        # Student dashboard, timetable UI, auth, syllabus upload interface
├── backend/         # API backend, auth logic, AI agent orchestrator, task processing
├── shared/          # Shared types, constants, schemas, and common data models
├── tests/           # Integration tests, E2E test suites, shared test fixtures
├── docs/            # Architecture notes, developer guides, Zensical source files
└── infrastructure/  # Docker configs, container definitions, CI/CD workflows
```

---

## Getting Started

### Prerequisites
- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/) (v18+ recommended)
- [Docker](https://www.docker.com/) (planned for local services)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/rbijo/ace.app.git
   cd ace.app
   ```
2. Copy environment template:
   ```bash
   cp .env.example .env
   ```

---

## Development & Contribution Guidelines

Detailed workflow and architecture guidelines are available on the [ACE Wiki](https://github.com/rbijo/ace.app/wiki).

- **Branch Naming**: Feature and chore branches should follow standard prefixes (`feature/`, `fix/`, `chore/`, `docs/`, `refactor/`).
- **Commit Messages**: Use lightweight conventional commit messages (e.g., `feat: ...`, `fix: ...`, `chore: ...`).
- **Secret Management**: Never commit secrets, credentials, or private API keys to git.

