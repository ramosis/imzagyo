import sys

with open('portal.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix finalizeContract payload
# Replace user_id missing with user_id: 1
payload_old = '''body: JSON.stringify({
                        property_id: selectedProperty.id,
                        seller_id: selectedParties.seller.id,
                        buyer_id: selectedParties.buyer.id,
                        contract_type: selectedContractType,
                        special_conditions: specialConditions,
                        status: 'draft'
                    })'''
                    
payload_new = '''body: JSON.stringify({
                        property_id: selectedProperty.id,
                        user_id: 1, // Admin default
                        seller_id: selectedParties.seller.id,
                        buyer_id: selectedParties.buyer.id,
                        contract_type: selectedContractType,
                        special_conditions: specialConditions,
                        status: 'draft'
                    })'''

content = content.replace(payload_old, payload_new)

# Fix appointment payload
appt_payload_old = '''body: JSON.stringify({
                        property_id: null,
                        baslik1: title,
                        username: client,
                        phone: phone,
                        date: date,
                        status: 'Bekliyor'
                    })'''

appt_payload_new = '''body: JSON.stringify({
                        property_id: 1, // Gerekli alan
                        user_id: 1, // Admin user
                        baslik1: title,
                        username: client,
                        phone: phone,
                        date: date,
                        status: 'Bekliyor'
                    })'''

content = content.replace(appt_payload_old, appt_payload_new)

with open('portal.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("portal JS payloads patched.")
