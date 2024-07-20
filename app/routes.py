# app/routes.py
from flask import Blueprint, request, jsonify
from . import db
from .models import Employee
from .schemas import employee_schema, employees_schema
from sqlalchemy.exc import SQLAlchemyError

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return "WELCOME TO THE EMPLOYEE MANAGEMENT SYSTEM"

# Create Employee
@routes.route('/employee', methods=['POST'])
def create_employee():
    if request.content_type != 'application/json':
        return jsonify({"message": "Content-Type must be application/json"}), 415

    data = request.get_json()
    new_emp = employee_schema.load(data)
    employee = Employee(name=new_emp['name'], dept=new_emp['dept'], position=new_emp['position'], salary=new_emp['salary'])
    
    try:
        db.session.add(employee)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    
    return employee_schema.jsonify(employee), 201

# Read specific employee by ID
@routes.route('/employee/<int:employee_id>', methods=['GET'])
def get_emp(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({"description": f"Employee with id {employee_id} not found!"}), 404
    return employee_schema.jsonify(employee), 200

# Update details for existing employee
@routes.route('/employee/<int:employee_id>', methods=['PUT'])
def update_emp(employee_id):
    if request.content_type != 'application/json':
        return jsonify({"message": "Content-Type must be application/json"}), 415

    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    data = request.get_json()
    updated_data = employee_schema.load(data, partial=True)
    if 'name' in updated_data:
        employee.name = updated_data['name']
    if 'dept' in updated_data:
        employee.dept = updated_data['dept']
    if 'position' in updated_data:
        employee.position = updated_data['position']
    if 'salary' in updated_data:
        employee.salary = updated_data['salary']
    
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    
    return jsonify({"message": "Employee updated successfully"}), 200

# Delete an employee
@routes.route('/employee/<int:employee_id>', methods=['DELETE'])
def delete_emp(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    try:
        db.session.delete(employee)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    
    return jsonify({"message": "Employee deleted successfully!"}), 200
