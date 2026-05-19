import re
from models.user import Student

class StudentService:
    def __init__(self):
        self.students={} #dict for O(1) complexity
    
    #Add student in system
    def add_student(self,sid,name,email,major):
        if sid in self.students:
            raise ValueError("Student already exists")
        self.students[sid]=Student(sid, name, email,major)        

    #Get all list of students
    def get_all(self):
        return list(self.students.values())    
    
    #Search students by name with regex
    def search_students(self, query):
        results=[]
        for s in self.students.values():
            try:
                if re.search(query, s.name, re.IGNORECASE):
                    results.append(s)
            except re.error:
                if query.lower() in s.name.lower(): #Regex not correct
                    results.append(s)               #Simple case-insensititve search
        return results        