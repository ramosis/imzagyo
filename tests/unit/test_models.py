import pytest
from backend.core.properties.portfolio.models import Property

def test_property_creation(app):
    """Test property model."""
    with app.app_context():
        prop = Property(
            title_tr='Test Villa',
            price=5000000,
            location_tr='Bebek'
        )
        assert prop.title_tr == 'Test Villa'
        assert prop.price == 5000000
