class Course:
    def __init__(self, course_id, name, credits, instructor):
        self.course_id = course_id
        self.name = name
        self.credits = int(credits)
        self.instructor = instructor