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
                students = FileHandler.read_csv("data/students.csv")
                for s in students:
                    try:
                        sid = str(s['student_id']).strip()
                        name = str(s['name']).strip()
                        email = str(s.get('email', '')).strip()
                        major = str(s.get('major', '')).strip()

                        self.student_service.add_student(sid, name, email, major)
                    except Exception as e:
                        pass
            except FileNotFoundError:
                pass

            try:
                courses = FileHandler.read_csv("data/courses.csv")
                for c in courses:
                    try:
                        cid = str(c['course_id']).strip()
                        cname = str(c['name']).strip()
                        credits = int(str(c['credits']).strip())
                        instructor = str(c.get('instructor', '')).strip()

                        self.course_service.add_course(cid, cname, credits, instructor)
                    except Exception as e:
                        pass
            except FileNotFoundError:
                pass

            try:
                grades = FileHandler.read_csv("data/grades.csv")
                for g in grades:
                    try:
                        sid = str(g['student_id']).strip()
                        cid = str(g['course_id']).strip()
                        score = float(str(g['score']).strip())
                        comment = str(g.get('comment', '')).strip()

                        self.grade_service.assign_grade(sid, cid, score, comment)
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

    def _student_menu(self):
        while True:
            os.system('cls' if os.name=='nt' else 'clear')
            print("=== STUDENTS ===")
            print("[1] List all students")
            print("[2] Add student")
            print("[3] Search student")
            print("[4] View student")
            print("[0] Back\n")

            choice = input("Choice: ").strip()

            if choice =="1":
                print("\n === ALL STUDENTS ===\n")
                print(f"{'ID':<5} {'Name':<20} {'Major':<18} {'GPA':<5} {'W.GPA':<5}")
                print("-" * 55)
                for s in self.student_service.get_all():
                    gpa = self.grade_service.calculate_simple_gpa(s.user_id)
                    wgpa = self.grade_service.calculate_weighted_gpa(s.user_id)
                    print(f"{s.user_id:<5} {s.name:<20} {s.major:<18} {gpa:<5.1f} {wgpa:<5.1f}")
                print()
                self.pause()

            elif choice =="2":
                print("\n === ADD STUDENTS ===\n")
                sid = input("Student ID: ")
                name = input(" Name: ")

                if not validate_name(name):
                    print("Error: Name must contain only letters, spaces and hyphens (2-50 chars)\n")
                    self.pause()
                    continue
                email = input("Email: ")
                major = input("Major: ")
                if validate_not_empty(sid) and validate_not_empty(major):
                    try:
                        self.student_service.add_student(sid, name, email, major)
                        print(f"\nStudent '{name}' added successfully!\n")
                    except Exception as e:
                        print(f"\nError: {e}\n")
                else:
                    print("\nError: Invalid ID or Major.\n")
                self.pause()

            elif choice =="3":
                print("\n === SEARCH STUDENTS ===\n")
                query = input("Search (name or regex): ")
                results = self.student_service.search_students(query)
                print(f"\nFound {len(results)} student(s):\n")
                for s in results:
                    gpa = self.grade_service.calculate_simple_gpa(s.user_id)
                    print(f"[Student] {s.name} (ID: {s.user_id}) | Major: {s.major} | GPA: {gpa}")
                print()
                self.pause()

            elif choice == "4":
                print("\n=== STUDENT REPORT ===\n")
                sid = input("Student ID: ")
                self._student_report(sid)
                print()
                self.pause()

            elif choice == "0":
                break


    @log_execution
    def _student_report(self, sid):
        student = self.student_service.students.get(sid)
        if not student:
            print("Error: Student not found.")
            return

        print(f"\nName: {student.name}")
        print(f"Major: {student.major}")

        gpa = self.grade_service.calculate_simple_gpa(sid)
        wgpa = self.grade_service.calculate_weighted_gpa(sid)
        print(f"Simple GPA: {gpa}")
        print(f"Weighted GPA: {wgpa}\n")

        grades = self.grade_service.get_student_grades(sid)
        print(f"{'Course':<10} {'Name':<23} {'Cr':<3} {'Score':<5} {'Grade'}")
        print("-" * 50)
        for g in grades:
            course = self.course_service.courses.get(g.course_id)
            c_name = course.name if course else "Unknown"
            c_cred = course.credits if course else 3
            print(f"{g.course_id:<10} {c_name:<23} {c_cred:<3} {g.score:<5.1f} {g.letter}")

    def _course_menu(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=== COURSES ===\n")
            print("[1] List all courses")
            print("[2] Add a course")
            print("[3] View course stats")
            print("[0] Back\n")

            choice = input("Choice: ").strip()

            if choice == "1":
                print("\n=== ALL COURSES ===\n")
                print(f"{'Code':<10} {'Name':<25} {'Credits':<7} {'Students'}")
                print("-" * 52)
                for c in self.course_service.get_all():
                    enrolled = len([g for g in self.grade_service.grades if g.course_id == c.course_id])
                    print(f"{c.course_id:<10} {c.name:<25} {c.credits:<7} {enrolled}")
                print()
                self.pause()

            elif choice == "2":
                print("\n === ADD COURSE ===\n")
                cid = input("Course code(e.g. CS101): ")
                name = input("Course name: ")
                credits = input("Course credits (1-10): ")
                instructor = input("Course instructor: ")
                if validate_not_empty(cid) and validate_not_empty(name):
                    try:
                        self.course_service.add_course(cid, name, credits, instructor)
                        print(f"\nCourse '{cid} - {name}' added!\n")
                    except Exception as e:
                        print(f"\nError: {e}\n")
                else:
                    print("\nError: Invalid input\n")
                self.pause()
            elif choice == "3":
                print("\n=== COURSE STATS ===\n")
                cid = input("Course code: ")
                self._course_stats(cid)
                print()
                self.pause()
            elif choice == "0":
                break

    def _course_stats(self, cid):
        c = self.course_service.courses.get(cid)
        if not c:
            print("Error: Course not found")
            return
        grades = [g for g in self.grade_service.grades if g.course_id == cid]
        print(f"\nCourse: {cid}")
        print(f"Students: {len(grades)}")
        if not grades: return

        scores = sorted([g.score for g in grades])
        mean = sum(scores) / len(scores)
        median = scores[len(scores)//2] if len(scores) % 2 != 0 else (scores[len(scores)//2 - 1] + scores[len(scores)//2])/2.0
        passing = len([s for s in scores if s >= 60])
        pass_rate = (passing/len(scores)) * 100

        print(f"Mean: {mean:.1f}")
        print(f"Median: {median:.1f}")
        print(f"Min: {scores[0]:.1f} Max: {scores[-1]:.1f}")
        print(f"Pass rate: {pass_rate:.1f}%\n")

        dist = {'A':0, 'B':0, 'C':0, 'D':0, 'F':0}
        for g in grades: dist[g.letter] += 1
        print(f"Distribution: A:{dist['A']} B:{dist['B']} C:{dist['C']} D:{dist['D']} F:{dist['F']}")

    def _grade_menu(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("GRADES")
            print("1. Assign grade")
            print("2. Update grade")
            print("3. Delete grade")
            print("0. Back")

            choice = input("Choice:")
            if choice == "1":
                print("Assign grade")
                sid = input("Student ID: ")
                cid = input("Course code: ")
                score = input ("Score (0-100): ")
                comment = input ("Comment (optional): ")
                valid, val = validate_score(score)
                if valid:
                    self._do_assign(sid,cid,val,comment)
                else:
                    print("Invalid score.")
                print()
                self.pause()

            elif choice == "2":
                print("Update grade")
                sid = input("Student ID: ")
                cid = input("Course code: ")
                score = input("New score (0-100): ")
                valid, val = validate_score(score)
                if valid:
                    self._do_update(sid,cid,val)
                else:
                    print("Invalid score.")
                print()
                self.pause()

            elif choice == "3":
                print("Delete grade")
                sid = input("Student ID: ")
                cid = input("Course code: ")

                if self.grade_service.delete_grade(sid, cid):
                    print("Grade deleted")
                else:
                    print("Grade not found")
                print()
                self.pause()

            elif choice == "0":
                    break

    @log_execution
    def _do_assign(self,sid,cid,val, comment):
        if sid not in self.student_service.students:
            print("Error: Student not found")
            return
        if cid not in self.course_service.courses:
            print("Error: Course not found")
            return

        try:
            self.grade_service.assign_grade(sid, cid, val, comment)
            g = next(
                g for g in self.grade_service.grades
                if g.student_id == sid and g.course_id == cid
            )
            print(f"Grade assigned: {cid}: {val}/100 ({g.letter})")
        except Exception as e:
            print(f"Error: {e}")

    @log_execution
    def _do_update(self, sid, cid, val):
        if sid not in self.student_service.students or cid not in self.course_service.courses:
            print("Error: Student or Course are not found")
            return
        if self.grade_service.update_grade(sid,cid,val):
            g = next(
                g for g in self.grade_service.grades
                if g.student_id == sid and g.course_id == cid
            )
            print (f"Grade updated: {cid}: {val}/100 ({g.letter})")
        else:
            print("Grade not found")

    def _analytics_menu(self):
        while True:
            os.system('cls' if os.name=='nt' else 'clear')
            print("==== Analytics ===")
            print("[1] Top students")
            print("[2] Hall of Fame (Gpa>=90)")
            print("[3] Failing students")
            print("[4] Full report")
            print("[5] Export report to JSON")
            print("[6] Export grades to CSV")
            print("[0] Back\n")
            choice = input("Choice: ").strip()

            if choice == "1":
                print("\n=== TOP STUDENTS (by weighted GPA) ===\n")
                limit_str = input("How many? (default 5):")
                limit = int(limit_str) if limit_str.isdigit() else 5
                top =self.report_service.get_top_students(limit)
                print(f"\n{'Rank':<5} {'Name':<20} {'Major':<17} {'W.GPA'}")
                print("-" *50)
                for i, (s,g) in enumerate(top, 1):
                    print(f"{i:<5} {s.name:<20} {s.major:<17} {g:.1f}")
                print()
                self.pause()
            elif choice =="2":
                print("\n== HALL OF FAME (Weighted GPA>=90) ===\n")
                hof= self.report_service.get_hall_of_fame()
                print(f"{'Name':<20} {'Major':<17} {'W.GPA'}")
                print("-"*45)
                for s,g in hof:
                    print(f"{s.name:<20} {s.major:<17} {g:.1f}")
                print()
                self.pause()
            elif choice == "3":
                print("\n=== FAILING STUDENTS (GPA<60) ===\n")
                fails = self.report_service.get_failing_students()
                if not fails:
                    print("No failing students")
                else:
                    for s,g in fails:
                        print(f"{s.name} - GPA: {g:.1f}")
                print()
                self.pause()
            elif choice == "4":
                print("\n=== FULL REPORT ===\n")
                rep = self.report_service.full_report()
                print(f"Date: {rep['date']}")
                print(f"Total students {rep['total_students']}")
                print(f"Total courses: {rep['total_courses']}")
                print(f"Average GPA: {rep['average_gpa']}")
                print(f"Passing: {rep['passing']}")
                print(f"Failing {rep['failing']}")
                print(f"Hall of Fame: {rep['hof']} students")
                print()
                self.pause()
            elif choice=="5":
                path= input("File path(default data/report.json:)") or "data/report.json"
                self.report_service.export_report_json(path)
                print(f"\nReport saved to {path}\n")
                self.pause()
            elif choice=="6":
                path=input("File Path (default: data/export_grades.csv)") or "data/export_grades.csv"
                self.report_service.export_grades_csv(path)
                print(f"\nGrades exported to {path}\n")
                self.pause()
            elif choice=="0":
                break
                         


if __name__=="__main__":
    app=Application()
    app.run()       