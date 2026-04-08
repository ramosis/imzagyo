from marshmallow import Schema, fields, validate, ValidationError

class LeadSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    phone = fields.Str(required=True)
    email = fields.Email(required=False, allow_none=True)
    source = fields.Str(dump_default="portal")
    interest_property_id = fields.Str(required=False, allow_none=True)
    assigned_user_id = fields.Int(required=False, allow_none=True)
    status = fields.Str(dump_default="new")
    notes = fields.Str(required=False, allow_none=True)
    tags = fields.Str(required=False, allow_none=True)
    ai_score = fields.Int(required=False, allow_none=True)
    campaign_id = fields.Str(required=False, allow_none=True)
    created_at = fields.DateTime(dump_only=True)

class PortfolioSchema(Schema):
    id = fields.Str(dump_only=True)
    ref_no = fields.Str(required=True, attribute="refNo")
    title = fields.Str(required=True, attribute="baslik1", validate=validate.Length(min=5))
    subtitle = fields.Str(required=False, allow_none=True, attribute="baslik2")
    category = fields.Str(required=False, attribute="koleksiyon") 
    location = fields.Str(required=False, attribute="lokasyon")
    price = fields.Str(required=False, attribute="fiyat")
    rooms = fields.Str(required=False, attribute="oda")
    area = fields.Str(required=False, attribute="alan")
    floor = fields.Str(required=False, attribute="kat")
    description = fields.Str(required=False, attribute="hikaye")
    image_hero = fields.Str(required=False, attribute="resim_hero")
    image_story = fields.Str(required=False, attribute="resim_hikaye")
    features = fields.List(fields.Str(), required=False, attribute="ozellikler_arr")
    status = fields.Str(dump_default="active")

class HeroSchema(Schema):
    id = fields.Int(dump_only=True)
    image_url = fields.Str(required=True, attribute="resim_url")
    alt_title = fields.Str(required=False, attribute="alt_baslik")

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(load_only=True, required=False) # update'lerde boş olabilir
    role = fields.Str(required=False, dump_default="standart")
    email = fields.Email(required=False, allow_none=True)
    is_active = fields.Bool(dump_default=True)

class ContractCreateSchema(Schema):
    contract_type = fields.Str(required=True, validate=validate.OneOf(['kiralama', 'satis', 'komisyon']))
    property_id = fields.Str(required=False, allow_none=True)
    lead_id = fields.Int(required=False, allow_none=True)
    price = fields.Float(required=True)
    currency = fields.Str(dump_default="TRY")
    commission_rate = fields.Float(required=False)
    start_date = fields.Str(required=False)
    end_date = fields.Str(required=False)
    parties = fields.List(fields.Dict(), required=False)

class ContractSchema(Schema):
    id = fields.Int(dump_only=True)
    contract_number = fields.Str(dump_only=True)
    contract_type = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)
    price = fields.Float()
    currency = fields.Str()
    created_at = fields.DateTime(dump_only=True)

# Instances for easy access
lead_schema = LeadSchema()
leads_schema = LeadSchema(many=True)
portfolio_schema = PortfolioSchema()
portfolios_schema = PortfolioSchema(many=True)
hero_schema = HeroSchema()
heros_schema = HeroSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
contract_schema = ContractSchema()
contracts_schema = ContractSchema(many=True)
