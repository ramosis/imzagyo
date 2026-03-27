# Imza GYO Modular Architecture Mapping

This document tracks the migration from legacy `api/` to the new modular structure.

## 📁 Shared Infrastructure (`shared/`)
| Legacy File | New Location | Description |
| :--- | :--- | :--- |
| `database.py` | `shared/database.py` | Core DB logic & connection manager |
| `extensions.py` | `shared/extensions.py` | Shared Flask extensions (DB, Cache, Babel) |
| `models.py` | `shared/models.py` | Shared data models and base classes |
| `schemas.py` | `shared/schemas.py` | Marshmallow schemas for all domains |
| `utils.py` | `shared/utils.py` | Shared utilities (sanitization, errors) |
| `mail_service.py` | `shared/mail_service.py` | Global e-mail delivery service |
| `notifications.py` | `shared/notifications.py` | Global notification system |
| `page_service.py` | `shared/page_service.py` | **[NEW]** Page serving bridge for static content |

## 🧩 Domain Modules (`modules/`)
| Domain | Blueprint Prefix | Routes | Description |
| :--- | :--- | :--- | :--- |
| **Auth** | `/api/v1/auth` | `auth_bp` | Identity, Session, Social Login, EİDS |
| **Portfolio** | `/api/v1` | `portfolio_bp` | Listings, Hero, Valuation, Neighborhood |
| **CRM** | `/api/v1` | `crm_bp` | Leads, Pipeline, Appointments |
| **Finance** | `/api/v1/finance` | `finance_bp` | Accounting, TCMB Rates, Commissions |
| **Media** | `/api/v1/media` | `media_bp` | Cloudinary, PIL, File Management |
| **AI** | `/api/v1/ai` | `ai_bp` | Summary Generation, Intent Scoring, Translation |
| **Legal** | `/api/v1/legal` | `legal_bp` | Contracts, Templates, Parties |
| **Automation** | `/api/v1/automation` | `automation_bp` | Task Rules, Marketing Campaigns, HR |
| **Integrations**| `/api/v1/integrations` | `integrations_bp`| MLS Sync, Platform Bridge |
| **Maintenance** | `/api/v1/maintenance` | `maintenance_bp` | Ticket Management |
| **Compass** | `/api/v1/compass` | `compass_bp` | Regional Dashboard, Heatmaps |

## ⚙️ App Core
- `app/factory.py`: Centralized blueprint registration and configuration.
- `app/routes.py`: Dynamic route handlers and sitemap generation.
- `run.py`: Application entry point.

**Migration Status: 100% Complete**
**Legacy api/ directory: DECOMMISSIONED**
