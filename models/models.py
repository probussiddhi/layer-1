from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask import Blueprint

db=Blueprint('models', __name__)


# db = SQLAlchemy()

class DailyContent(db.Model):
    __tablename__ = 'daily_content'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    policy_no = db.Column(db.String, nullable=False)
    company_id = db.Column(db.Integer, nullable=False)
    company_code = db.Column(db.String, nullable=True)
    product_id = db.Column(db.Integer, nullable=True)
    product_name = db.Column(db.String, nullable=True)
    subproduct_id = db.Column(db.Integer, nullable=True)
    subproduct_name = db.Column(db.String, nullable=True)
    segment_id = db.Column(db.Integer, nullable=True)
    segment_name = db.Column(db.String, nullable=True)
    policy_issue_date = db.Column(db.Date, nullable=True)
    policy_start_date = db.Column(db.Date, nullable=True)
    policy_end_date = db.Column(db.Date, nullable=True)
    cust_salutation = db.Column(db.String, nullable=True)
    cust_name = db.Column(db.String, nullable=False)
    cust_mobile_no = db.Column(db.String, nullable=True)
    cust_email_id = db.Column(db.String, nullable=True)
    cust_address = db.Column(db.String, nullable=True)
    cust_pincode = db.Column(db.Integer, nullable=True)
    cust_city = db.Column(db.String, nullable=True)
    cust_state = db.Column(db.String, nullable=True)
    prv_company_id = db.Column(db.Integer, nullable=True)
    prv_company_code = db.Column(db.String, nullable=True)
    prv_policy_no = db.Column(db.String, nullable=True)
    prv_policy_exp_date = db.Column(db.Date, nullable=True)
    vehicle_regi_no = db.Column(db.String, nullable=True)
    engine_no = db.Column(db.String, nullable=True)
    chassis_no = db.Column(db.String, nullable=True)
    vehicle_mfg_year = db.Column(db.Integer, nullable=True)
    vehicle_mfg_month = db.Column(db.Integer, nullable=True)
    vehicle_regi_date = db.Column(db.Date, nullable=True)
    rto_code = db.Column(db.String, nullable=True)
    vehicle_make = db.Column(db.String, nullable=True)
    vehicle_model = db.Column(db.String, nullable=True)
    vehicle_variant = db.Column(db.String, nullable=True)
    cubic_capacity = db.Column(db.Integer, nullable=True)
    seating_capacity = db.Column(db.Integer, nullable=True)
    gross_vehicle_weight = db.Column(db.Integer, nullable=True)
    fuel_id = db.Column(db.Integer, nullable=True)
    fuel_type = db.Column(db.String, nullable=True)
    ncb_percentage = db.Column(db.Integer, nullable=True)
    sum_insurred = db.Column(db.Integer, nullable=True)
    net_od_premium = db.Column(db.Integer, nullable=True)
    net_tp_premium = db.Column(db.Integer, nullable=True)
    net_premium = db.Column(db.Integer, nullable=True)
    gst = db.Column(db.Integer, nullable=True)
    final_premium = db.Column(db.Integer, nullable=True)
    cpa_premium = db.Column(db.Integer, nullable=True)
    zero_dep_premium = db.Column(db.Integer, nullable=True)
    plan_name = db.Column(db.String, nullable=True)
    no_of_insured_person = db.Column(db.Integer, nullable=True)


class CompanyMaster(db.Model):
    __tablename__ = 'Company_master'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    gi_li = db.Column(db.String(50), nullable=False)

class SegmentMaster(db.Model):
    __tablename__='segmant_master'

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(255), nullable=False)

class ProductMaster(db.Model):
    __tablename__ = 'product_master'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    # Define a one-to-many relationship with SubProduct
    sub_products = relationship('SubProduct', back_populates='product')

class SubProduct(db.Model):
    __tablename__ = 'sub_product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    product_id = db.Column(Integer, ForeignKey('product_master.id'))

    # Define the relationship with ProductMaster
    product = relationship('ProductMaster', back_populates='sub_products')

class MotorFuelMaster(db.Model):
    __tablename__='motor_fuel_master'
    fuel_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    fuel_type=db.Column(db.String(255), nullable=False)



from app import db
db.create_all()
