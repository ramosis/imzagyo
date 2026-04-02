import pytest
from modules.crm.service import LeadService
from modules.crm.models import Lead

def test_lead_lifecycle(app):
    """Tests lead creation and duplicate detection logic."""
    with app.app_context():
        # 1. Create a fresh lead
        lead_data = {
            "name": "Test Adayı",
            "phone": "5551234567",
            "email": "test@imza.com",
            "notes": "İlk başvuru notu"
        }
        
        result = LeadService.calculate_and_create(lead_data)
        assert result['name'] == "Test Adayı"
        assert result['ai_score'] > 0
        
        # Verify in DB
        lead = Lead.query.filter_by(phone="5551234567").first()
        assert lead is not None
        assert lead.name == "Test Adayı"

        # 2. Duplicate detection: same phone, different name
        dup_data = {
            "name": "Aynı Telefon Farklı İsim",
            "phone": "5551234567",
            "email": "farkli@imza.com",
            "notes": "İkinci başvuru"
        }
        
        updated_result = LeadService.calculate_and_create(dup_data)
        assert updated_result['id'] == result['id'] # Must be the same ID
        
        # Verify update
        updated_lead = Lead.query.get(result['id'])
        assert "İkinci başvuru" in updated_lead.notes
        assert "İlk başvuru" in updated_lead.notes

def test_lead_validation_missing_name(app):
    """Ensures validation fails if required fields are missing."""
    with app.app_context():
        invalid_data = {
            "phone": "5550000000"
            # name missing
        }
        with pytest.raises(Exception):
            LeadService.calculate_and_create(invalid_data)
