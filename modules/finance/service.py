from typing import Dict, Any

class FinanceService:
    @staticmethod
    def calculate_tax(price: float, tax_type: str) -> Dict[str, Any]:
        """Vergi hesaplama mantığı."""
        # Vergi oranları
        rates = {
            'kdv': 0.20,      # %20 KDV
            'stopaj': 0.20,   # %20 Stopaj
            'emlak': 0.004,   # %0.4 Emlak Vergisi
            'tapu_harci': 0.04 # %4 Tapu Harcı
        }
        
        tax_type = tax_type.lower()
        if tax_type not in rates:
            raise ValueError(f"Unknown tax type: {tax_type}")
            
        rate = rates[tax_type]
        tax_amount = price * rate
        
        return {
            'price': price,
            'tax_type': tax_type,
            'tax_rate': rate,
            'tax_amount': tax_amount,
            'total': price + tax_amount if tax_type != 'stopaj' else price - tax_amount
        }
