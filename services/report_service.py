import json
import csv
from datetime import datetime
from utils.decorators import log_execution

class ReportService:
    def __init__(self, student_service, course_service, grade_service):
        self.student_service = student_service
        self.course_service = course_service
        self.grade_service = grade_service
    def get_top_students(self, limit=5):
        s_gpa = [(s, self.grade_service.calculate_weighted_gpa(s.user_id)) for s in self.student_service.get_all()]
        return sorted(s_gpa, key=lambda x: x[1], reverse=True)[:limit]
    def get_hall_of_fame(self):
        s_gpa = [(s, self.grade_service.calculate_weighted_gpa(s.user_id)) for s in self.student_service.get_all()]
        return sorted([x for x in s_gpa if x[1] >= 3.5], key=lambda x: x[1],
                      reverse=True)

    def get_failing_students(self):
        s_gpa = []
        for s in self.student_service.get_all():
            if self.grade_service.get_student_grades(s.user_id):
                s_gpa.append((s, self.grade_service.calculate_simple_gpa(s.user_id)))
        return sorted([x for x in s_gpa if x[1] < 60.0], key=lambda x: x[1])

    @log_execution
    def full_report(self):
        all_s = self.student_service.get_all()
        all_c = self.course_service.get_all()

        gpas = []
        for s in all_s:
            if self.grade_service.get_student_grades(s.user_id):
                gpas.append(self.grade_service.calculate_simple_gpa(s.user_id))

        avg = sum(gpas) / len(gpas) if gpas else 0.0
        passing = len([g for g in gpas if g >= 60.0])
        failing = len([g for g in gpas if g < 60.0])
        hof = len(self.get_hall_of_fame())

        return {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_students": len(all_s),
            "total_courses": len(all_c),
            "average_gpa": round(avg, 1),
            "passing": passing,
            "failing": failing,
            "hof": hof
        }

    def export_report_json(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.full_report(), f, indent=4)

    def export_grades_csv(self, path):
        with open(path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Student ID", "Course ID", "Score", "Letter"])
            for g in self.grade_service.grades:
                writer.writerow([g.student_id, g.course_id, g.score, g.letter])