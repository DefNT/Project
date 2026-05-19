import os
from services.student_service import StudentService
from services.course_service import CourseService
from services.grade_service import GradeService
from services.report_service import ReportService
from utils.file_handler import FileHandler
from utils.validators import validate_not_empty, validate_score, validate_name
from utils.decorators import log_execution

class Application:
    def __init__(self):
        self.student_service=StudentService()
        self.course_service=CourseService()
        self.grade_service=GradeService(self.course_service)
        self.report_service=ReportService(self.student_service, self.course_service, self.grade_service)

        os.system('cls' if os.name == 'nt' else 'clear')
        print("==================================================")
        print("      STUDENT GRADE MANAGEMENT SYSTEM             ")
        print("==================================================")
        print("loading data...")
        self.load_data()
        print(f"Loaded: {len(self.student_service.get_all())} students, {len(self.course_service.get_all())} courses\n")
        self.pause()

    def pause(self):
        input("Press Enter to continue...")

    def run(self):
        while True:
            os.system('cls' if os.name=='nt' else 'clear')
            print("=============================================")
            print("      STUDENT GRADE MANAGEMENT SYSTEM")
            print("=============================================")

            s_count=len(self.student_service.students)
            c_count=len(self.course_service.courses)
            print(f"Students: {s_count} | Courses: {c_count}\n")

            print("[1] Students")
            print("[2] Courses")
            print("[3] Grades")
            print("[4] Analytics & Reports")
            print("[5] Save data")
            print("[0] Exit\n")

            choice=input("Choice: ").strip()

            if choice=="1": self._student_menu()
            elif choice =="2": self._course_menu()
            elif choice=="3": self._grade_menu()
            elif choice=="4": self._analytics_menu()
            elif choice=="5":
                self.save_data()
                print("\nData saved!\n")
                self.pause()
            elif choice=="0":
                self.save_data()
                break    
#Reading data 
    def load_data(self):
        try:
            students=FileHandler.read_csv("data/students.csv")
            for s in students:
                try:
                    self.student_service.add_student(
                        s['student_id'],
                        s['name'],
                        s.get('email', ''),
                        s.get('major', '')
                    )
                except Exception as e:
                    pass
        except FileNotFoundError:
            pass

        try:
            courses=FileHandler.read_csv("data/courses.csv")
            for c in courses:
                try:
                    self.course_service.add_course(
                        c['course_id'],
                        c['name'],
                        c['credits'],
                        c.get('instructor', '')
                    )
                except Exception as e:
                    pass    
        except FileNotFoundError:
            pass

        try:
            grades=FileHandler.read_csv("data/grades.csv")
            for g in grades:
                try:
                    self.grade_service.assign_grade(
                        g['student_id'],
                        g['course_id'],
                        g['score'],
                        g.get('comment', '')
                    )        
                except Exception as e:
                    pass
        except FileNotFoundError:
            pass            
    #Saving Csv
    def save_data(self):
        students_data=[{"student_id": s.user_id, "name": s.name, "email": s.email, "major": s.major} for s in self.student_service.get_all()]
        FileHandler.write_csv("data/students.csv", students_data, ["student_id", "name", "email", "major"])
        courses_data=[{"course_id": c.course_id, "name": c.name, "credits": c.credits, "instructor": c.instructor} for c in self.course_service.get_all()]
        FileHandler.write_csv("data/courses.csv", courses_data, ["course_id", "name", "credits", "instructor"])
        grades_data= [{"student_id": g.student_id, "course_id": g.course_id, "score": g.score, "comment":g.comment} for g in self.grade_service.grades]
        FileHandler.write_csv("data/grades.csv", grades_data, ["student_id", "course_id", "score", "comment"])
if __name__=="__main__":
    app=Application()
    app.run()       