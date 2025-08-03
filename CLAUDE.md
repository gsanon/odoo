# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Odoo Framework Overview

Odoo is an open-source business application suite with a modular architecture. This is the main Odoo repository containing:

- **Core framework** (`/odoo/`) - Main framework code, ORM, web client, CLI
- **Addons** (`/addons/`) - Official modules/apps (accounting, CRM, inventory, etc.)
- **Configuration** - Database config, deployment files

### Key Architecture Components

- **ORM & Models**: Located in `odoo/models.py` and `odoo/fields.py` - Odoo's custom ORM system
- **Web Framework**: `odoo/http.py` - HTTP routing and web controllers
- **CLI System**: `odoo/cli/` - Command-line interface with multiple subcommands
- **Module System**: Each addon is a Python package with `__manifest__.py` defining dependencies and metadata

### Addon Structure

Each addon follows a consistent structure:
```
addon_name/
├── __init__.py
├── __manifest__.py      # Module definition and dependencies
├── models/             # Business logic and data models
├── views/              # XML view definitions
├── static/             # CSS, JS, images
├── data/               # CSV/XML data files
├── security/           # Access rights and rules
└── tests/              # Unit and integration tests
```

## Common Development Commands

### Running Odoo

```bash
# Start Odoo server
./odoo-bin -d <database_name> -i <addon_name>

# Start with config file
./odoo-bin -c config/odoo.conf

# Start in development mode (auto-reload on file changes)
./odoo-bin -d <database_name> --dev=all

# Update specific addon
./odoo-bin -d <database_name> -u <addon_name>
```

### Database Operations

```bash
# Create database
./odoo-bin -d <database_name> --init=base --stop-after-init

# Backup database
./odoo-bin -d <database_name> --backup-db

# Run shell with database context
./odoo-bin shell -d <database_name>
```

### Testing

```bash
# Run tests for specific addon
./odoo-bin -d <test_database> -i <addon_name> --test-enable --stop-after-init

# Run specific test file
./odoo-bin -d <test_database> --test-file=addons/<addon_name>/tests/test_file.py --test-enable --stop-after-init

# Run all tests
./odoo-bin -d <test_database> --test-enable --init=all --stop-after-init
```

### Scaffolding

```bash
# Create new addon
./odoo-bin scaffold <addon_name> <target_directory>
```

### Code Analysis

```bash
# Count lines of code
./odoo-bin cloc

# Generate TypeScript configuration
./odoo-bin tsconfig
```

## Development Workflow

### Module Development

1. **Create addon structure**: Use `./odoo-bin scaffold` or copy existing addon template
2. **Define models**: Create Python classes inheriting from `models.Model`
3. **Create views**: Define XML views (forms, trees, search views)
4. **Add security**: Define access rights in `security/ir.model.access.csv`
5. **Write tests**: Add unit tests in `tests/` directory
6. **Update manifest**: Declare dependencies and data files in `__manifest__.py`

### Testing Strategy

- **Unit tests**: Test individual model methods and business logic
- **Integration tests**: Test workflows and module interactions
- **Tour tests**: Frontend JavaScript tests for user interactions
- Test files follow pattern: `test_*.py` in `tests/` directories

### Database Management

Odoo uses PostgreSQL with a custom schema per database. The framework handles:
- Automatic table creation from model definitions
- Migration scripts for addon updates
- Multi-company and multi-currency support

## Key File Patterns

- `__manifest__.py` - Module metadata and dependencies
- `models/*.py` - Business logic and database models  
- `views/*.xml` - User interface definitions
- `data/*.xml` or `*.csv` - Default data and configuration
- `security/*.csv` - Access control definitions
- `static/src/` - Frontend assets (JS, CSS, images)
- `tests/test_*.py` - Python unit/integration tests
- `static/tests/*.js` - JavaScript frontend tests

## Configuration

Default configuration: `config/odoo.conf` (basic setup provided)
Docker support: `docker-compose.yml` available for containerized development

## Important Notes

- Python version support: 3.10-3.13
- Main executable: `./odoo-bin` (not `python -m odoo`)
- Database required for most operations
- Addons must be explicitly installed (`-i`) or updated (`-u`)
- Development mode (`--dev=all`) enables auto-reload and enhanced debugging