from __future__ import annotations


class Student:

    def __init__(self, name: str, surname: str, gender: str) -> None:
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
    
    def rate_lecture(self, mentor: Mentor, course: str, grade: int) -> str | None:
        if isinstance(mentor, Lecturer) and course in self.courses_in_progress and course in mentor.courses_attached:
            if isinstance(grade, int) and 1 <= grade <= 10:
                if course in mentor.grades:
                    mentor.grades[course].append(grade)
                else:
                    mentor.grades[course] = [grade]
            else:
                return 'Ошибка'
        else:
            return 'Ошибка'
    
    def get_average_grade(self) -> float:
        all_average_grades = []
        courses = 0
        for course, grades in self.grades.items():
            if course and grades:
                all_average_grades.append(sum(grades) / len(grades))
                courses += 1
        if courses:
            average_grade = sum(all_average_grades) / courses
        else:
            average_grade = 0.0
        return average_grade

    def __str__(self) -> str:
        result = (f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {self.get_average_grade()}\n'
            f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\nЗавершенные курсы: {", ".join(self.finished_courses)}')
        return result
    
    def __eq__(self, other: Student) -> bool:
        return self.get_average_grade() == other.get_average_grade()
    
    def __lt__(self, other: Student) -> bool:
        return self.get_average_grade() < other.get_average_grade()
    
    def __gt__(self, other: Student) -> bool:
        return self.get_average_grade() > other.get_average_grade()


class Mentor:

    def __init__(self, name: str, surname: str) -> None:
        self.name = name
        self.surname = surname
        self.courses_attached = []
        
    def rate_hw(self, student: Student, course: str, grade: int) -> str | None:
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


class Lecturer(Mentor):

    def __init__(self, name: str, surname: str) -> None:
        super().__init__(name, surname)
        self.grades = {}

    def rate_hw(self, student: Student, course: str, grade: int) -> None:
        pass

    def get_average_grade(self) -> float:
        all_average_grades = []
        courses = 0
        for course, grades in self.grades.items():
            if course and grades:
                all_average_grades.append(sum(grades) / len(grades))
                courses += 1
        if courses:
            average_grade = sum(all_average_grades) / courses
        else:
            average_grade = 0.0
        return average_grade

    def __str__(self) -> str:
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.get_average_grade()}'
    
    def __eq__(self, other: Lecturer) -> bool:
        return self.get_average_grade() == other.get_average_grade()
    
    def __lt__(self, other: Lecturer) -> bool:
        return self.get_average_grade() < other.get_average_grade()
    
    def __gt__(self, other: Lecturer) -> bool:
        return self.get_average_grade() > other.get_average_grade()


class Reviewer(Mentor):

    def rate_hw(self, student: Student, course: str, grade: int) -> str | None:
        return super().rate_hw(student, course, grade)
    
    def __str__(self) -> str:
        return f'Имя: {self.name}\nФамилия: {self.surname}'


def get_global_average_grade_hw(students: list, course: str) -> float:
    average_grades = []
    for student in students:
        if student.grades.get(course):
            average_grade = sum(student.grades[course]) / len(student.grades[course])
            average_grades.append(average_grade)
    if len(average_grades) == 0:
        return 0.0
    return sum(average_grades) / len(average_grades)


def get_global_average_grade_lecture(lecturers: list, course: str) -> float:
    average_grades = []
    for lecturer in lecturers:
        if lecturer.grades.get(course):
            average_grade = sum(lecturer.grades[course]) / len(lecturer.grades[course])
            average_grades.append(average_grade)
    if len(average_grades) == 0:
        return 0.0
    return sum(average_grades) / len(average_grades)


lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
print(isinstance(lecturer, Mentor)) # True
print(isinstance(reviewer, Mentor)) # True
print(lecturer.courses_attached)    # []
print(reviewer.courses_attached)    # []
print()

lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
student = Student('Алёхина', 'Ольга', 'Ж')
 
student.courses_in_progress += ['Python', 'Java']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']
 
print(student.rate_lecture(lecturer, 'Python', 7))   # None
print(student.rate_lecture(lecturer, 'Java', 8))     # Ошибка
print(student.rate_lecture(lecturer, 'С++', 8))      # Ошибка
print(student.rate_lecture(reviewer, 'Python', 6))   # Ошибка
 
print(lecturer.grades)  # {'Python': [7]}  
print()

first_student = Student('Анатолий', 'Кузнецов', 'М')
first_student.courses_in_progress += ['Python', 'Git']
first_student.finished_courses += ['JavaScript']

second_student = Student('Анна', 'Скворцова', 'Ж')
second_student.courses_in_progress += ['Python', 'Git']
second_student.finished_courses += ['HTML']

first_reviewer = Reviewer('Антон', 'Подольский')
first_reviewer.courses_attached += ['Python', 'JavaScript', 'Git']

second_reviewer = Reviewer('Мария', 'Зайцева')
second_reviewer.courses_attached += ['Python', 'HTML', 'Git']

first_lecturer = Lecturer('Андрей', 'Евстигнеев')
first_lecturer.courses_attached += ['Python', 'C++']

second_lecturer = Lecturer('Анастасия', 'Чёрная')
second_lecturer.courses_attached += ['Python', 'Git']

lecturers_list = [first_lecturer, second_lecturer]
students_list = [first_student, second_student]

first_reviewer.rate_hw(first_student, 'Python', 8)
first_reviewer.rate_hw(second_student, 'Git', 9)
second_reviewer.rate_hw(first_student, 'Git', 10)
second_reviewer.rate_hw(second_student, 'Python', 7)

first_student.rate_lecture(first_lecturer, 'Python', 8)
first_student.rate_lecture(second_lecturer, 'Python', 9)
first_student.rate_lecture(second_lecturer, 'Git', 9)
second_student.rate_lecture(first_lecturer, 'Python', 7)
second_student.rate_lecture(second_lecturer, 'Python', 8)
second_student.rate_lecture(second_lecturer, 'Git', 10)

print(first_reviewer)
print()
print(second_reviewer)
print()
print(first_lecturer)
print()
print(second_lecturer)
print()
print(first_student)
print()
print(second_student)
print()
print('Средняя оценка по домашним заданиям по курсу "Python":')
print(get_global_average_grade_hw(students_list, 'Python'))
print()
print('Средняя оценка по домашним заданиям по курсу "Git":')
print(get_global_average_grade_hw(students_list, 'Git'))
print()
print('Средняя оценка за лекции по курсу "Python":')
print(get_global_average_grade_lecture(lecturers_list, 'Python'))
print()
print('Средняя оценка за лекции по курсу "Git":')
print(get_global_average_grade_lecture(lecturers_list, 'Git'))
print()
print('Равны ли средние оценки за ДЗ у first_student и second_student:')
print(first_student == second_student)
print()
print('Меньше ли средняя оценка за ДЗ у first_student, чем у second_student:')
print(first_student < second_student)
print()
print('Больше ли средняя оценка за ДЗ у first_student, чем у second_student:')
print(first_student > second_student)
print()
print('Равны ли средние оценки за лекции у first_lecturer и second_lecturer:')
print(first_lecturer == second_lecturer)
print()
print('Меньше ли средняя оценка за лекции у first_lecturer и second_lecturer:')
print(first_lecturer < second_lecturer)
print()
print('Больше ли средняя оценка за лекции у first_lecturer и second_lecturer:')
print(first_lecturer > second_lecturer)

