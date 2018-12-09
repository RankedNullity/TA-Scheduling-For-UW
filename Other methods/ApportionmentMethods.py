#!/usr/bin/env python
# coding: utf-8

# In[30]:


import math
import numpy as np
import time

#Standard_Divisor = Total_Students/Number_of_TAs
#Standard_Quota = Students_in_Slot/Standard_Divisor
#Lower_Quota = Floor(Standard_Quota)
#Upper_Quota = Ceiling(Standard_Quota)

# Returns the set of schedules for apportioning TAs using the Hamilton, Jefferson, Adam, Webster, and Huntington methods
#    @Student_Distribution    The distribution of students in various time slots for the IPL schedule. Each index should represent the number of students that came in at the time slot indexed in the list. Student_Distribution therefore needs to be a one dimensional list of integers.
#    @Total_TAs    The total number of TAs to be scheduled this quarter
#    @Number_Of_Shifts_Each_TA_Works    The number of shifts each TA is expected to work in the IPL each week. One shift is the equivalent of one time slot in the student distribution schedule.
#    @Get_Hamilton    A boolean value. Set to True if you want the program to compute Hamilton's method of apportionment, False otherwise.
#    @Get_Jefferson    A boolean value. Set to True if you want the program to compute Jefferson's method of apportionment, False otherwise.
#    @Get_Adam    A boolean value. Set to True if you want the program to compute Adam's method of apportionment, False otherwise.
#    @Get_Webster    A boolean value. Set to True if you want the program to compute Webster's method of apportionment, False otherwise.
#    @Get_Huntington    A boolean value. Set to True if you want the program to compute the Huntington-Hill method of apportionment, False otherwise.
#    @Get_Huntington_Arithmetic    A boolean value. Set to True if you want the program to compute the Huntington-Hill method of apportionment that uses the arithmetic mean instead of the geometric mean, False otherwise.
#    @return    The method returns a list of schedules using various apportionment methods.
def GetSchedules(Student_Distribution, Total_TAs, Number_Of_Shifts_Each_TA_Works, Get_Hamilton, Get_Jefferson, Get_Adam, Get_Webster, Get_Huntington, Get_Huntington_Arithmetic):
    
    Total_TAs *=Number_Of_Shifts_Each_TA_Works    # Each TA works a certain number of shifts, so we multiply the number of TAs by that number to get the total number of shifts that all the TAs will work
    Schedule_Length = len(Student_Distribution)

    # Constraint: At least 1 TA per time slot
    # This means that instead of initializing each slot at 0, we can just initialize at 1 and allocate the rest of the TAs
    #  The number of remaining TAs after initializing with values of 1 is:
    Total_TAs -= Schedule_Length
    # Note that this does not change the method of apportionment, only the values the method produces
    
    if Total_TAs < 0:
        raise ValueError("The number of shifts that all TAs will work is less than the number of shifts in the schedule. Therefore there is no schedule fitting the constraints. ")
    
    Total_Students = 0    # The total number of students in all slots
    for i in Student_Distribution:
        Total_Students += i
    
    Standard_Divisor = Total_Students/Total_TAs
    
    To_Return = [ [ "Hamilton", Get_Hamilton, [] ], [ "Jefferson" , Get_Jefferson, [] ], ["Adam", Get_Adam, [] ],  [ "Webster", Get_Webster, [] ], [ "Huntington (computed with geometric mean)", Get_Huntington, [] ],  ["Huntington (computed with arithmetic mean)", Get_Huntington_Arithmetic, [] ]]
    
    
    if Get_Hamilton:
        To_Return[0][2] = HamiltonMethod(Student_Distribution, Total_TAs, Standard_Divisor)
        if len(To_Return[0][2])<Schedule_Length:
            To_Return[0][2] = [0 for i in Student_Distribution]
            To_Return[0][1] = False
    if Get_Jefferson:
        To_Return[1][2] = JeffersonMethod(Student_Distribution, Total_TAs, Standard_Divisor)
        if len(To_Return[1][2])<Schedule_Length:
            To_Return[1][2] = [0 for i in Student_Distribution]
            To_Return[1][1] = False
    if Get_Adam:
        To_Return[2][2] = AdamMethod(Student_Distribution, Total_TAs, Standard_Divisor)
        if len(To_Return[2][2])<Schedule_Length:
            To_Return[2][2] = [0 for i in Student_Distribution]
            To_Return[2][1] = False
    if Get_Webster:
        To_Return[3][2] = WebsterMethod(Student_Distribution, Total_TAs, Standard_Divisor)
        if len(To_Return[3][2])<Schedule_Length:
            To_Return[3][2] = [0 for i in Student_Distribution]
            To_Return[3][1] = False
    if Get_Huntington:
        To_Return[4][2] = HuntingtonMethod(Student_Distribution, Total_TAs, Standard_Divisor)
        if len(To_Return[4][2])<Schedule_Length:
            To_Return[4][2] = [0 for i in Student_Distribution]
            To_Return[4][1] = False
    if Get_Huntington_Arithmetic:
        To_Return[5][2] = HuntingtonMethodArithmetic(Student_Distribution, Total_TAs, Standard_Divisor)
        if len(To_Return[5][2])<Schedule_Length:
            To_Return[5][2] = [0 for i in Student_Distribution]
            To_Return[5][1] = False
    
    return(To_Return)


    
#Hamilton's Method
def HamiltonMethod(Student_Distribution, Total_TAs, Standard_Divisor):
    
    #Step 1: Calculate each time slot's standard Quota
    #Step 2: Allocate the Lower Quota
    #Step 3: Give the surplus TAs to the time slots with the largest fractional parts
    
    To_Return = [0 for i in Student_Distribution]
    
    Standard_Quotas = [i/Standard_Divisor for i in Student_Distribution]    # Step 1
    
    Remainders = [0 for i in Student_Distribution]
    
    for i in range(len(Student_Distribution)):    # Step 2
        To_Return[i] = int(math.floor(Standard_Quotas[i]))
        Remainders[i] = Standard_Quotas[i]-To_Return[i]    # Keeping track of the fractional part of the quotas for step 3
        Total_TAs -= To_Return[i]    # Keeping track of the remaining TAs for step 3
    
    while Total_TAs > 0:    # Step 3
        Maximum_Remainder_Index = 0    # Index of the time slot with the largest remainder
        Maximum_Remainder = 0    # Largest remainder value
        for i in range(len(Remainders)):    # Loops through all of the time slots and finds the one with the largest remainder
            if Remainders[i] > Maximum_Remainder:
                Maximum_Remainder = Remainders[i]
                Maximum_Remainder_Index = i
        
        To_Return[Maximum_Remainder_Index] += 1    # Add a TA to the time slot with the highest remainder
        Total_TAs -= 1    # Decrement the total number of TAs remaining
        Remainders[Maximum_Remainder_Index] = 0    # Set the value of the remainder for the slot with the highest remainder to -1 (not a possible remainder) so that we don't add more TAs to that slot
    
    for j in range(len(To_Return)):
        To_Return[j] += 1
    return(To_Return)

#Jefferson's Method
def JeffersonMethod(Student_Distribution, Total_TAs, Standard_Divisor):
    
    # Step 1: Modify the divisor so that the lower quotas add up to the number of seats
        # Step 1a: Pick a divisor
        # Step 1b: If the sum of the lower quotas is greater than the number of TAs decrease the divisor. If the sum is less than the number of TAs, then increase
    # Step 2: Apportion the modified lower quota
    
    Standard_Divisor += 1
    
    
    Incrament_Step = Standard_Divisor*0.05
    Previous_Was_Decrament = False
    
    To_Return = [1 for i in Student_Distribution]
    
    Lower_Quotas = [math.floor(i/Standard_Divisor) for i in Student_Distribution]    # Step 1a

    Lower_Quota_Sum = 0
    
    for i in Lower_Quotas:    # Step 1b
        Lower_Quota_Sum += i

    if (Lower_Quota_Sum == Total_TAs):
        for i in range(len(Lower_Quotas)):
                Lower_Quotas[i] += 1
        return(Lower_Quotas)
    
    if Lower_Quota_Sum > Total_TAs:
        Standard_Divisor += Incrament_Step
    else:
        Standard_Divisor -= Incrament_Step
        Previous_Was_Decrament = True
    
    
    Incrament_Step = Standard_Divisor*0.05

    startTime = time.time()
    
    while (time.time()-startTime)<3 :
        Lower_Quotas = [math.floor(i/Standard_Divisor) for i in Student_Distribution]    # Step 1a

        Lower_Quota_Sum = 0
    
        for i in Lower_Quotas:    # Step 1b
            Lower_Quota_Sum += i
    
        if (Lower_Quota_Sum == Total_TAs):
            for i in range(len(Lower_Quotas)):
                Lower_Quotas[i] += 1
            return(Lower_Quotas)

        if Lower_Quota_Sum > Total_TAs:
            if Previous_Was_Decrament:
                Incrament_Step = Incrament_Step*0.9
            Standard_Divisor += Incrament_Step
            Previous_Was_Decrament = False
        
        else:
            if not(Previous_Was_Decrament):
                Incrament_Step = Incrament_Step*0.9
            Standard_Divisor -= Incrament_Step
            Previous_Was_Decrament = True

    return([])

#Adam's Method
def AdamMethod(Student_Distribution, Total_TAs, Standard_Divisor):
    
    # Step 1: Modify the divisor so that the upper quotas add up to the number of seats
        # Step 1a: Pick a divisor
        # Step 1b: If the sum of the lower quotas is greater than the number of TAs decrease the divisor. If the sum is less than the number of TAs, then increase
    # Step 2: Apportion the modified upper quota
    
    Standard_Divisor+=1
    
    Incrament_Step = Standard_Divisor*0.01
    Previous_Was_Decrament = False
    
    To_Return = [1 for i in Student_Distribution]
    
    Upper_Quotas = [math.ceil(i/Standard_Divisor) for i in Student_Distribution]    # Step 1a

    Upper_Quota_Sum = 0

    for i in Upper_Quotas:    # Step 1b
        Upper_Quota_Sum += i

    if (Upper_Quota_Sum == Total_TAs):
        for i in range(len(Upper_Quotas)):
                Upper_Quotas[i] += 1
        return(Upper_Quotas)
    
    if Upper_Quota_Sum > Total_TAs:
        Standard_Divisor += Incrament_Step
    else:
        Standard_Divisor -= Incrament_Step
        Previous_Was_Decrament = True
    
    Incrament_Step = Standard_Divisor*0.01

    startTime = time.time()
    
    while (time.time()-startTime)<3 :
        Upper_Quotas = [math.ceil(i/Standard_Divisor) for i in Student_Distribution]    # Step 1a

        Upper_Quota_Sum = 0

        for i in Upper_Quotas:    # Step 1b
            Upper_Quota_Sum += i

        if (Upper_Quota_Sum == Total_TAs):
            for i in range(len(Upper_Quotas)):
                Upper_Quotas[i] += 1
            return(Upper_Quotas)

        if Upper_Quota_Sum > Total_TAs:
            if Previous_Was_Decrament:
                Incrament_Step = Incrament_Step*0.9
            Standard_Divisor += Incrament_Step
            Previous_Was_Decrament = False
        
        else:
            if not(Previous_Was_Decrament):
                Incrament_Step = Incrament_Step*0.9
            Standard_Divisor -= Incrament_Step
            Previous_Was_Decrament = True

    return([])


#Webster's Method
def WebsterMethod(Student_Distribution, Total_TAs, Standard_Divisor):
    # Step 1: Modify the divisor so that the natural rounding of  the standard quotas add up to the number of seats
        # Step 1a: Pick a divisor
        # Step 1b: If the sum of the lower quotas is greater than the number of TAs decrease the divisor. If the sum is less than the number of TAs, then increase
    # Step 2: Apportion the modified upper quota
    
    Standard_Divisor+=1
    
    Incrament_Step = Standard_Divisor*0.01
    Previous_Was_Decrament = False
    
    To_Return = [0 for i in Student_Distribution]
    
    Standard_Quotas = [round(i/Standard_Divisor) for i in Student_Distribution]    # Step 1a

    Standard_Quota_Sum = 0

    for i in Standard_Quotas:    # Step 1b
        Standard_Quota_Sum += i

    if (Standard_Quota_Sum == Total_TAs):
        for i in range(len(Standard_Quotas)):
            Standard_Quotas[i] += 1
        return(Standard_Quotas)
    
    if Standard_Quota_Sum > Total_TAs:
        Standard_Divisor += Incrament_Step
    else:
        Standard_Divisor -= Incrament_Step
        Previous_Was_Decrament = True
    
    Incrament_Step = Standard_Divisor*0.01

    startTime = time.time()
    
    while (time.time()-startTime)<3 :
        Standard_Quotas = [round(i/Standard_Divisor) for i in Student_Distribution]    # Step 1a

        Standard_Quota_Sum = 0

        for i in Standard_Quotas:    # Step 1b
            Standard_Quota_Sum += i
            
        if (Standard_Quota_Sum == Total_TAs):
            for i in range(len(Standard_Quotas)):
                Standard_Quotas[i] += 1
            return(Standard_Quotas)

        if Standard_Quota_Sum > Total_TAs:
            if Previous_Was_Decrament:
                Incrament_Step = Incrament_Step*0.9
            Standard_Divisor += Incrament_Step
            Previous_Was_Decrament = False
        
        else:
            if not(Previous_Was_Decrament):
                Incrament_Step = Incrament_Step*0.9
            Standard_Divisor -= Incrament_Step
            Previous_Was_Decrament = True

    return([])

#Huntington-Hill Method
def HuntingtonMethod(Student_Distribution, Total_TAs, Standard_Divisor):
    
    To_Return = [1 for i in Student_Distribution]
    
    Standard_Quotas = [round(i/Standard_Divisor) for i in Student_Distribution]    # Step 1a
        
    Geometric_Means = [math.sqrt(math.floor(i)*math.ceil(i)) for i in Standard_Quotas]
    
    for i in range(len(Student_Distribution)):
        if Standard_Quotas[i] <= Geometric_Means[i]:
            To_Return[i] += math.floor(Standard_Quotas[i])
        else:
            To_Return[i] += math.ceil(Standard_Quotas[i])
    
    return(To_Return)

def HuntingtonMethodArithmetic(Student_Distribution, Total_TAs, Standard_Divisor):
    
    To_Return = [1 for i in Student_Distribution]
    
    Standard_Quotas = [round(i/Standard_Divisor) for i in Student_Distribution]    # Step 1a
        
    Arithmetic_Means = [math.sqrt((math.floor(i)**2)+(math.ceil(i)**2)) for i in Standard_Quotas]
    
    for i in range(len(Student_Distribution)):
        if Standard_Quotas[i] <= Arithmetic_Means[i]:
            To_Return[i] += math.floor(Standard_Quotas[i])
        else:
            To_Return[i] += math.ceil(Standard_Quotas[i])
    
    return(To_Return)


def Main(Student_Distribution, Total_TAs, Number_Of_Shifts_Each_TA_Works, Get_Hamilton, Get_Jefferson, Get_Adam, Get_Webster, Get_Huntington, Get_Huntington_Arithmetic):
    
    # Type checks
    if not(isinstance(Student_Distribution, list)):
        raise TypeError("The student distribution for each time slot needs to be a one dimensional instance of list. Argument passed for Student_Distribution was of type {}".format(type(Student_Distribution)))
    if not(type(Total_TAs) is int):
        raise TypeError("The number of TAs to be assigned needs to be an integer value. Argument passed for Total_TAs was of type {}".format(type(Total_TAs)))
    if not(type(Number_Of_Shifts_Each_TA_Works) is int):
        raise TypeError("The number of shifts each TA is expected to work needs to be an integer value. Argument passed for Number_Of_Shifts_Each_TA_Works was of type {}".format(type(Number_Of_Shifts_Each_TA_Works)))
    if not(type(Get_Hamilton) is bool):
        raise TypeError("The value of Get_Hamilton needs to be of type boolean. Argument passed for Get_Hamilton was of type {}".format(type(Get_Hamilton)))
    if not(type(Get_Jefferson) is bool):
        raise TypeError("The value of Get_Jefferson needs to be of type boolean. Argument passed for Get_Jefferson was of type {}".format(type(Get_Jefferson)))
    if not(type(Get_Adam) is bool):
        raise TypeError("The value of Get_Adam needs to be of type boolean. Argument passed for Get_Adam was of type {}".format(type(Get_Adam)))
    if not(type(Get_Webster) is bool):
        raise TypeError("The value of Get_Webster needs to be of type boolean. Argument passed for Get_Webster was of type {}".format(type(Get_Webster)))
    if not(type(Get_Huntington) is bool):
        raise TypeError("The value of Get_Huntington needs to be of type boolean. Argument passed for Get_Huntington was of type {}".format(type(Get_Huntington)))
    if not(type(Get_Huntington_Arithmetic) is bool):
        raise TypeError("The value of Get_Huntington_Arithmetic needs to be of type boolean. Argument passed for Get_Huntington_Arithmetic was of type {}".format(type(Get_Huntington_Arithmetic)))
 
    # Checking that Student_Distribution contains only integer values
    for i in range(len(Student_Distribution)):
        if not(type(Student_Distribution[i]) is int):
            raise TypeError("The student distribution needs to be a one dimensional list of integer values. Argument passed for Student_Distribution has a non-integer value at index {}.\nArgument passed for Student_Distribution:\n {}".format(i, Student_Distribution))
        
        # Value checks
        if Student_Distribution[i] < 0:
            raise ValueError("The number of students in any index of Student_Distribution needs to be non-negative. Argument passed for Student_Distribution has a negative value at index {}.\nArgument passed for Student_Distribution:\n".format(i, Student_Distribution))
    if Total_TAs < 0:
        raise ValueError("The number of TAs to be assigned needs to non-negative. Argument passed: Total_TAs: {}".format(Total_TAs))
    
    Schedules = GetSchedules(Student_Distribution, Total_TAs, Number_Of_Shifts_Each_TA_Works, Get_Hamilton, Get_Jefferson, Get_Adam, Get_Webster, Get_Huntington, Get_Huntington_Arithmetic)
    R = Schedules[0][2]
    for i in Schedules:
        for j in range(len(i[2])):
            if i[2][j] >R[j]:
                R[j] = i[2][j]
    print("Max Collum Schedule: \n"+str(R))
    print()
    
    T = [0 for i in R]
    for i in Schedules:
        if i[1]:
            print("Schedule produced by "+i[0]+"'s method:")
            print(i[2])
            L = [R[j]-i[2][j] for j in range(len(R))]
                
            print("Difference from Max Collumn Schedule: \n"+str(L))
            total = 0
            for j in range(len(L)):
                total +=L[j]
                if L[j] > T[j]:
                    T[j] =L[j]
            print("Total difference from Max Collumn Schedule: "+str(total))
            print()
        else:
            print(i[0]+"'s method did not return a schedule.")
            print()
    
    print("Maximum difference from Max Collumn Schedule:\n"+str(T))
    total = 0
    for i in T:
        total += i
    print("Total extra shifts: "+str(total))
    
Main([319, 375, 348, 393, 407, 443, 418, 327, 326, 367, 327, 436, 460, 474, 500, 625, 588, 349, 357, 315, 370, 430, 440, 471, 519, 494, 385, 369, 455, 442, 420, 498, 565, 566, 442, 357, 364, 321, 397, 361, 312, 221, 284, 265, 247, 277], 76, 2, True, True, True, True, True, True)


# In[ ]:




