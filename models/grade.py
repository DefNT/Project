class GradeRecord:
    def __init__(self, student_id, course_id, score, comment=" "):
        self.student_id = student_id
        self.course_id = course_id
        self.score = float(score)
        self.comment = comment
    @property
    def letter(self):
        if self.score >= 90: return 'A'
        if self.score >=80: return 'B'
        if self.score >=70: return 'C'
        if self.score >=60: return 'D'
        return 'F'
    
    @property
    def points(self):
        if self.score >= 90: return 4.0
        if self.score >=80: return 3.0
        if self.score >=70: return 2.0
        if self.score >=60: return 1.0
        return 0.0