from models.course import Course

class CourseService:
    def __init__(self):
        self.courses = {}

    def add_course(self, cid, name, credits, instructor):
        if cid in self.courses:
            raise ValueError("Course already exists")
        self.courses[cid] = Course(cid, name, credits, instructor)

    def get_all(self):
        return list(self.courses.values())