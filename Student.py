#!/usr/bin/env python
class Student(object):

    total_marks = 500


    def __init__(self,name,marks):
        self.name = name
        self.marks = marks

    def getGrade(self):
        grade = int(marks * Student.total_marks / 100)

        if grade >= 33 and grade <= 45:
            return print "C Grade"
        elif grade > 45 and grade <= 59:
            return "B grade"
        elif grade > 59 and grade <= 100:
            return "A grade"
        else
            return "Incorrect value"
