from abc import ABC
from finance import Wallet
from managing import Resource


class Person(ABC) :
    ID_counter = 1

    def __init__(self, name: str):
        if not name:
            raise ValueError("Name cannot be empty")
        self.name = name
        self.id = "P-" + str(Person.ID_counter)
        Person.ID_counter += 1
        self.wallet = Wallet(self.id, 0)

    def __str__(self) -> str:
        return f"{self.name} ({self.__class__.__name__})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Person):
            return False
        return self.id == other.id


class Mentor(Person):    
    def approve_request(self, resource: Resource, student: 'Student') -> bool:
        if resource.status == 'available':
            print(f"APPROVAL: Approved {resource.type} for {student.name}")
            return True
        print(f"DENIAL: Denied {resource.type} for {student.name} (Unavailable)")
        return False


class Course:
    max_students = 20 

    def __init__(self, title: str, cost: float, mentor: Mentor):
        self.title = title
        self.cost = cost
        self.mentor = mentor
        self.students = []

    def add_student(self, student: 'Student') -> None:
        if len(self.students) >= self.max_students:
            raise ValueError(f"Course: {self.title} is full")
        self.students.append(student)


class Student(Person):
    def __init__(self, name: str):
        super().__init__(name)
        self._progress = 0
        self.enrolled_courses = []
        self.borrowed_resources = []

    @property
    def progress(self) -> int:
        return self._progress

    @progress.setter
    def progress(self, value: int) -> None:
        if not (0 <= value <= 100):
            raise ValueError("Progress must be between 0 and 100")
        self._progress = value

    def enroll(self, course: Course) -> None:
        if self.wallet.balance < course.cost:
            raise ValueError(f"Insufficient funds to enroll in {course.title}")
        
        self.wallet.withdraw(course.cost)
        course.add_student(self)
        self.enrolled_courses.append(course)
        print(f"ENROLLED: {self.name} -> {course.title} (Mentor: {course.mentor.name})")

    def borrow_resource(self, resource: Resource, mentor: Mentor) -> None:
        if mentor.approve_request(resource, self):
            resource.status = 'borrowed'
            self.borrowed_resources.append(resource)
            print(f"BORROW: Resource {resource.id}")

    def needs_resource(self) -> bool:
        return len(self.borrowed_resources) < 2


class PremiumStudent(Student):

    def enroll(self, course: Course) -> None:
        super().enroll(course) 
        print(f"PREMIUM ENROLL: {self.name} -> {course.title} (Mentor: {course.mentor.name})")

    def needs_resource(self) -> bool:
        return len(self.borrowed_resources) < 4

