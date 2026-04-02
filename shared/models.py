""" 
İmza Gayrimenkul - Central Model Registry
Bu dosya, Alembic'in (Flask-Migrate) tüm modelleri görmesi için modüler modelleri tek bir noktada toplar.
"""
from shared.extensions import db

# 1. CORE & SHARED MODELS
from modules.core.models import HeroSlide, SystemSetting, UserInteraction, IncomingDoc
from modules.notification.models import Notification
from modules.audit.models import AuditLog

# 2. BUSINESS MODULE MODELS
from modules.auth.models import User, RefreshToken, UserIdentity, AuthAuditLog, PasswordReset
from modules.portfolio.models import PortfolioListing, PortfolioMedia, MLSListing, MLSDemand, MLSTrustScore, Ekip, PropertyInspection, ListingShadow, Project, ProjectLead
from modules.neighborhood.models import NeighborhoodFacility, NeighborhoodReservation, ApartmentPoll, PollVote, ShuttleSchedule, StaffLocation, Business, NeighborhoodPost, NeighborhoodDemand
from modules.crm.models import Lead, PipelineStage, PipelineHistory, LeadInteraction, MessageTemplate, Contact, Appointment, PurchasingPower
from modules.finance.models import Contract, ContractTemplate, ContractClause, ContractClauseLink, ContractParty, Tax, DuesPayment, ApartmentExpense, StaffExpense, UserShift, Commission, Campaign, CampaignLog
from modules.maintenance.models import MaintenanceRequest, PropertyUnit, Lease
from modules.integration.models import PlatformConnection, Publication
from modules.automation.models import AutomationRule, AutomationLog
