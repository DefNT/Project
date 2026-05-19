import unittest
from models.user import User, student, Student
from models.course import Course
from models.grade import GradeRecord

class TestModels(unittest.TestCase):
    def test_student_inheritance(self):
        s = Student("S1", "Alice", "alice@example.com", "CS")
        self.assertEqual(s.name, "Alice")
        self.assertEqual(s.email, "alice@example.com")
        self.assertIn("Student", s.display_info())

    def test_course_inheritance(self):
        C = Course("C1", "Math", 4, "Dr. Smith")
        self.assertEqual(c.instructor, "Dr.Smith")

    def test_grade_logic(self):
        g = GradeRecord("s1","c1",85, "Good" )
        self.assertEqual(g.letter, "B")
        self.assertEqual(g.points, 3.0)


