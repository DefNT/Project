# Student Grade Management System

## Overview

A simple modular command-line application designed for managing student records, course enrollments, and academic performance

## Key Features

* **Data Persistence:** Full CRUD operations for Students, Courses, and Grades using CSV storage.
* **Advanced Analytics:** Calculates simple and credit-weighted GPAs, identifies top performers (*Hall of Fame*), and generates failing student reports.
* **Data Integrity:** Implements Regex-based input validation and robust error handling.
* **Reporting:** Export academic reports to JSON and grade logs to CSV.

## Project Structure

```text
project/
├── data/           # Persistent CSV database files
├── models/         # Core entities (Student, Course, GradeRecord)
├── services/       # Business logic layer
├── tests/          # Unit test suite
├── utils/          # Helper modules (Validators, Decorators)
└── main.py         # Application entry point

```

## How to Run

1. **Clone the repository:**
```bash
git clone <repository-url>

```

2. **Launch the application:**
```bash
python main.py

```


## Team & Roles

| Name | Contribution Focus |
| --- | --- |
| **Beksultan** | Project setup, Validation utilities, Student management |
| **Ataly** | Core models, Main app structure, Analytics/Reporting |
| **Turlykhan** | Course management, File handling, Course statistics |
| **Yerassyl** | Grade models, GPA calculation engine, Grade management |

## Technical Highlights

* **OOP:** Utilizes inheritance and encapsulation for clean data modeling.
* **Advanced Features:**
* **Decorators:** `@log_execution` for performance monitoring.
* **Properties:** `@property` for dynamic GPA and letter-grade conversions.
* **Algorithm Efficiency:** Dictionary-based storage for **O(1)** retrieval.
* **Functional Programming:** Uses `lambda` functions and list comprehensions for complex data sorting and filtering.
