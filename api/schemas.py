from marshmallow import Schema, fields, validate, ValidationError

class LeadSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    phone = fields.Str(required=True)
    email = fields.Email(required=False, allow_none=True)
    source = fields.Str(dump_default="portal")
    interest_property_id = fields.Int(required=False, allow_none=True)
    assigned_user_id = fields.Int(required=False, allow_none=True)
    status = fields.Str(dump_default="new")
    notes = fields.Str(required=False, allow_none=True)
    tags = fields.Str(required=False, allow_none=True)
    ai_score = fields.Int(required=False, allow_none=True)
    campaign_id = fields.Str(required=False, allow_none=True)
    created_at = fields.DateTime(dump_only=True)

class PortfolioSchema(Schema):
    id = fields.Int(dump_only=True)
    refNo = fields.Str(required=True)
    baslik1 = fields.Str(required=True)
    baslik2 = fields.Str(required=False, allow_none=True)
    kategori = fields.Str(required=False)
    lokasyon = fields.Str(required=False)
    fiyat = fields.Str(required=False)
    oda = fields.Str(required=False)
    alan = fields.Str(required=False)
    isitma = fields.Str(required=False)
    kat = fields.Str(required=False)
    hikaye = fields.Str(required=False)
    resim_hero = fields.Str(required=False)
    resim_hikaye = fields.Str(required=False)
    ozellikler_arr = fields.List(fields.Str(), required=False)
    status = fields.Str(dump_default="active")

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(load_only=True, required=False) # update'lerde boş olabilir
    role = fields.Str(required=False, dump_default="standart")
    email = fields.Email(required=False, allow_none=True)
    is_active = fields.Bool(dump_default=True)

# Instances for easy access
lead_schema = LeadSchema()
leads_schema = LeadSchema(many=True)
portfolio_schema = PortfolioSchema()
portfolios_schema = PortfolioSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
