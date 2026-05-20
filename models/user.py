class User:
    def __init__(self,user_id,name):
      self.user_id=user_id
      self.name=name

    def display_info(self):
      return f"User {self.name}, (ID : {self.user_id})"

class Student(User):
   def __init__(self,user_id,name,email,major):
      super().__init__(user_id,name)
      self.email=email
      self.major=major

   def display_info(self):
      return f"Student{self.name} (ID: {self.user_id}) - {self.major} - {self.email}"