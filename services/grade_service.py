from models.grade import GradeRecord
class GradeService:
    def __init__(self, course_service):
        self.grades = []
        self.course_service = course_service

    def assign_grade(self,sid,cid,score, comment=""):
        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100")
        for g in self.grades:
            if g.student_id==sid and g.course_id==cid:
                raise ValueError("Grade already exists")
        self.grades.append(GradeRecord(sid,cid,score,comment))

    def update_grade(self,sid,cid,score):
        for g in self.grades:
            if g.student_id==sid and g.course_id==cid:
                g.score = float(score)
                return True
        return False

    def delete_grade(self,sid,cid):
        for g in self.grades:
            if g.student_id==sid and g.course_id==cid:
                self.grades.remove(g)
                return True
        return False

    def get_student_grades(self,sid):
        return [g for g in self.grades if g.student_id==sid]
    def calculate_gpa(self,sid):
        return self.calculate_simple_gpa(sid)
    def calculate_simple_gpa(self,sid):
        grades = self.get_student_grades(sid)
        if not grades:
            return 0.0
        return round(sum(g.score for g in grades)/len(grades),1)

    def calculate_weighted_gpa(self,sid):
        grades = self.get_student_grades(sid)
        if not grades:
            return 0.0

        pts = 0
        crds = 0

        for g in grades:
            c = self.course_service.courses.get(g.course_id)
            crd = c.credits if c else 3
            pts += g.score * crd
            crds += crd

        return round(pts/crds,1) if crds > 0 else 0.0