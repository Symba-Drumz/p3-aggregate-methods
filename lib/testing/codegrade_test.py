import unittest
from datetime import datetime, timedelta
from lib.enrollment import Student, Course, Enrollment

class TestAggregateMethods(unittest.TestCase):

    def setUp(self):
        # Clear Enrollment.all before each test
        Enrollment.all.clear()

    def test_course_count(self):
        student = Student("Alice")
        course1 = Course("Math")
        course2 = Course("Science")
        student.enroll(course1)
        student.enroll(course2)
        self.assertEqual(student.course_count(), 2)

        # Test with no enrollments
        student_empty = Student("Empty")
        self.assertEqual(student_empty.course_count(), 0)

    def test_aggregate_average_grade(self):
        student = Student("Bob")
        course1 = Course("History")
        course2 = Course("Art")
        enrollment1 = Enrollment(student, course1)
        enrollment2 = Enrollment(student, course2)
        student._grades[enrollment1] = 85
        student._grades[enrollment2] = 95
        average = student.aggregate_average_grade()
        self.assertAlmostEqual(average, 90)

        # Test with no grades
        student_empty = Student("Empty")
        self.assertEqual(student_empty.aggregate_average_grade(), 0)

        # Test with one grade
        student_one = Student("One")
        enrollment3 = Enrollment(student_one, course1)
        student_one._grades[enrollment3] = 100
        self.assertEqual(student_one.aggregate_average_grade(), 100)

    def test_aggregate_enrollments_per_day(self):
        student1 = Student("Charlie")
        student2 = Student("Dana")
        course = Course("Physics")

        # Create enrollments on different days
        enrollment1 = Enrollment(student1, course)
        enrollment1._enrollment_date = datetime.now() - timedelta(days=1)
        enrollment2 = Enrollment(student2, course)
        enrollment2._enrollment_date = datetime.now()

        counts = Enrollment.aggregate_enrollments_per_day()
        self.assertEqual(counts[enrollment1.get_enrollment_date().date()], 1)
        self.assertEqual(counts[enrollment2.get_enrollment_date().date()], 1)

        # Test with multiple enrollments on same day
        enrollment3 = Enrollment(student1, course)
        enrollment3._enrollment_date = enrollment2._enrollment_date
        counts = Enrollment.aggregate_enrollments_per_day()
        self.assertEqual(counts[enrollment2.get_enrollment_date().date()], 2)

        # Test with no enrollments
        Enrollment.all.clear()
        counts_empty = Enrollment.aggregate_enrollments_per_day()
        self.assertEqual(counts_empty, {})

if __name__ == "__main__":
    unittest.main()
