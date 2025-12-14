from people import Student, PremiumStudent, Mentor, Course
from managing import Resource, ResourceCatalog


def run_demo() -> None:
    print("DEMO:")
    print("-------------------------------------------")

    mentor_omar = Mentor("Omar")

    zahra = Student("Zahra")
    malik = PremiumStudent("Malik")

    zahra.wallet.deposit(500)
    malik.wallet.deposit(600)

    print(f"Wallet Zahra: {zahra.wallet.balance}")
    print(f"Wallet Malik: {malik.wallet.balance}\n")

    python_course = Course("Async Python", 150, mentor_omar)
    oop_course = Course("OOP Fundamentals", 200, mentor_omar)
    git_course = Course("Git Basics", 100, mentor_omar)

    zahra.enroll(python_course)
    malik.enroll(oop_course)
    malik.enroll(git_course)

    print("-------------------------------------")

    print("Before transfer:")
    print(f"Zahra balance: {zahra.wallet.balance}")
    print(f"Malik balance: {malik.wallet.balance}")

    zahra.wallet.transfer(malik.wallet, 150)

    print("After transfer:")
    print(f"Zahra balance: {zahra.wallet.balance}")
    print(f"Malik balance: {malik.wallet.balance}\n")

    printer = Resource("3D Printer")
    lab = Resource("Lab")
    laptop = Resource("Laptop")

    catalog = ResourceCatalog()
    catalog.add_resource(printer)
    catalog.add_resource(lab)
    catalog.add_resource(laptop)

    print(f"Catalog size: {len(catalog)}")

    print("\nCatalog items:")
    for resource in catalog:
        print(resource)

    print("-------------------------------------")

    zahra.borrow_resource(printer, mentor_omar)
    malik.borrow_resource(lab, mentor_omar)

    print("-------------------------------------")

    catalog.allocate(zahra)
    catalog.allocate(malik)


if __name__ == "__main__":
    run_demo()
