import statistics
class SchoolJournal:
    def __init__(self,subject,student,grade_list):
        self.subject=subject
        self.student=student
        self.grade_list=[]
    def grade(self,a):
        self.a=a
        self.grade_list.append(a)
    def printer(self):
        print(self.subject)
        print(self.student)
        print(self.grade_list)
    def final_grade(self):
        print(statistics.mean(self.grade_list))
        


stud1=SchoolJournal('Химия','Игорь Байгашов',grade_list=[])
stud1.grade(4)
stud1.grade(5)
stud1.grade(3)
stud1.grade(2)
stud1.grade(5)
stud1.printer()
stud1.final_grade()