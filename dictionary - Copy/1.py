import re

def regular(in_string):


    
    return re.sub(r"how can i help",'',in_string)
    
sequence = "hey there how can i helpwhat plan am i onthan\
            hey there how can i helphow do i add more hot\
            hey there how can i helpchange"        
print(regular(sequence))