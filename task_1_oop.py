class Journal:
    
    def __init__(self, klass):
        self.klass = klass
        self.stud_list = {}
  
          
    def add_student(self, students):
       for i in range(len(students)):
           
           self.stud_list[students[i]] = {}

        
    def add_subjects(self, subject):
        self.subject = subject
        
        for student in self.stud_list:
            self.stud_list[student][subject] = []
        
        
    def rate_students(self, fio, subject, mark):
        self.stud_list[fio][subject].append(mark)
        
            
    def print_statistics(self, fio, subject):
        print(self.stud_list[fio][subject])
        
        
    def print_middle(self, fio, subject):
        print(round(sum(self.stud_list[fio][subject]) / len(self.stud_list[fio][subject]), 2))
        
        
    def test(self):
        print(self.stud_list)
       
        
clas1 = Journal('10-И')
clas1.add_student(['Петр', 'Макан Маканов', 'Антон'])       
clas1.add_subjects('Информатика')
clas1.add_subjects('Физика')

clas1.rate_students('Петр', 'Физика', 5)
clas1.rate_students('Петр', 'Физика', 4)
clas1.rate_students('Петр', 'Физика', 3)
clas1.rate_students('Петр', 'Информатика', 1)
clas1.rate_students('Петр', 'Физика', 5)
clas1.rate_students('Петр', 'Физика', 2)
clas1.rate_students('Петр', 'Физика', 2)
clas1.rate_students('Петр', 'Информатика', 5)
clas1.rate_students('Петр', 'Физика', 4)
        
clas1.print_statistics('Петр', 'Информатика')
clas1.print_middle('Петр', 'Информатика')
        
clas1.print_statistics('Петр', 'Физика')
clas1.print_middle('Петр', 'Физика')
        
clas1.test()











        