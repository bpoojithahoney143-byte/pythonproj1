from flask import Flask, request, jsonify

from flasgger import Swagger

from fastapi import FastAPI
#app = Flask(__name__)
app = FastAPI()
#swagger = Swagger(app)

## Employee namangement system
# Add employee
# View employee details, 
#     get employee details by id
#     get all employee details
#update employee details
# delete employee details

class Employee: 
    emp_id: int
    name: str
    salary: float

    def __init__(self, emp_id, name, salary):
        self.emp_id = emp_id
        self.name = name
        self.salary = salary


#Creation of employee data table
#In-Memory database to store employee details
employees : dict = {} # Dictionary of employees, with key -Empid, and Value is employee detail

@app.route("/add", methods=["POST"])
def add_employee():
       if request.content_type == "application/json" or request.content_type == "text/json":
            data = request.get_json()
    
            emp_id = data.get("emp_id")
            name = data.get("name")
            salary = data.get("salary")

            new_employee = Employee(emp_id, name, salary)
            employees[emp_id] = new_employee
            return jsonify({"message": "Employee added successfully"})
       else:
            return jsonify({"message": "Invalid content type. Please send JSON data."}), 400



@app.route("/<int:emp_id>", methods=["GET"])
def get_employee_by_id(emp_id):
    employee = employees.get(emp_id)
    if employee:
        return jsonify({"emp_id": employee.emp_id, "name": employee.name, "salary": employee.salary})
    else:
        return jsonify({"message": "Employee not found"}), 404
    



@app.route("/<name>", methods = ["GET"])
def get_emp_by_name(name):
    emps = employees.values()

    existing_employee = None

    for emp in emps:
         if emp.name == name:
              existing_employee = emp
              break
         
    if existing_employee:
         return jsonify({"emp_id": existing_employee.emp_id, "name": existing_employee.name, "salary": existing_employee.salary})
    else:
         return jsonify({"message":"not found error"}),404


@app.route("/all", methods=["GET"])
def get_all_employees():
    all_employees = []
    for emp in employees.values():
        all_employees.append({"emp_id": emp.emp_id, "name": emp.name, "salary": emp.salary})
    return jsonify(all_employees)


@app.route("/update", methods=["PUT"])     
def update_employee(): 
        if request.content_type == "application/json" or request.content_type == "text/json" :
           data = request.get_json()
           emp_id = data.get("emp_id")
           name = data.get("name")      
           salary = data.get("salary")

           existing_employee = employees.get(emp_id)

           if existing_employee:
               existing_employee.name = name
               existing_employee.salary = salary
               employees[emp_id] = existing_employee               
               return jsonify({"message": "Employee updated successfully"})
           else:
               return jsonify({"message": "Employee not found"}), 404
         
        else: 
            return jsonify({"message": "Invalid content type. Please send JSON data."}), 400



@app.route("/delete/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
     existing_employee = employees.get(emp_id)

     if existing_employee:
          del employees[emp_id]
          return jsonify({"message": "Employee deleted successfully"})
     else:
          return jsonify({"message": "Employee not found"}), 404

if __name__ == "__main__":
    #app.run(debug=True)
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
    
