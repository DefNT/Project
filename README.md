Student Grade Management System

Overview
A simple modular command line application for managing student records, course enrollements, and academic performance

Key Features
  Data Persistance: Full CRUD operations for Students, Courses, and Grades
  Analytic: Calculates simple and credit-weighted GPAs, identifies top     performers(Hall of Fame), and generates failing student reports
  Data Integrity: Includes Regex-based input validation and error handling
  Reporting: Export academic reports to JSON and grade logs to CSV

Structures
  /models: Core entities(Student, Course, GradeRecord)
  /services: Logic layers(StudentService, CourseServices, GradeServices, ReportService)
  /utils: Helpers(FileHandler, Validators, Decorators)
  /tests: unittest suite for all modules

How to Run
  1)Just clone the repo
  2)run "python main.py"

Team and Roles
  Beksultan: Project setup, validators utils student management
  Ataly: Core models, Main application structure, Analytics/Reporting services
  Turlykhan: Coures management, File handling, Course stats
  Yerassyl: Grade models, GPA calculation, Grade management

Technical part
  OOP: Used inheritance and encapsulation
  Advanced features: -Decorators: @log_execution for performance monitoring
    Properties: @property for dynamic GPA/letter-grade conversion
    Efficiency: Dictionary-based storage for O(1) look-up
    Functional: Used lambda functions and list comprehension for complex data sorting and filtering
