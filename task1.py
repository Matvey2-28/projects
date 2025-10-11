class SchoolJournal:
    def __init__(self, subject,student):
        self.subject=subject
        self.student=student
        self.grade_list=[]
    def grade(self):
        self.grade_list=[1,2,3,4,5]
    def printer(self):
        self.student=int(input('Введите имя ученика: '))
        print(self.student)
        self.subject=int(input('Введите название предметов: '[]))
        print(self.subject)
        self.grade_list=int(input('Введите оценку ученика: '))
        print(self.grade_list)
