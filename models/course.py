class Course:
    def __init__(self, course_id, name, credits, instructor):
        self.course_id = course_id
        self.name = name
        try:
            self.credits = int(credits)
        except (ValueError, TypeError):
            self.credits = 3
        self.instructor = instructor