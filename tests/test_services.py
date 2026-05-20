import unittest
from services.student_service import StudentService
from services.course_service import CourseService
from services.grade_service import GradeService

class TestServices(unittest.TestCase):
    def setUp(self):
        self.cs = CourseService()
        self.ss = StudentService()
        self.gs = GradeService(self.cs)

    def test_add_student(self):
        self.ss.add_student("S1", "John", "John@gmail.com", "SE")
        self.assertEqual(len(self.ss.get_all()), 1)

    def test_gpa_calculator(self):
        self.cs.add_course("C1", "Math", 4, "TBA")
        self.cs.add_course("C2", "PE", 2, "TBA")
        self.gs.assign_grade("S1", "C1", 95)
        self.gs.assign_grade("S1", "C2", 75)

        gpa = self.gs.calculate_simple_gpa("S1")
        self.assertEqual(gpa, 85.0)

        wgpa = (self.gs.calculate_weighted_gpa("S1"))
        self.assertEqual(wgpa, 3.3)