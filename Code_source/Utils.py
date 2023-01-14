import math
#This function will be used to resolve conflicts between 2 robots
def best_robot_within_2_conflict(list_robots,list_battery,L,task_position,alpha,beta,gamma,d_max,T_max) :

  Robot1 = list_robots[L[0][0]]
  Robot2 = list_robots[L[1][0]]
  t1 = L[0][1]
  t2 = L[1][1]
  b1 = list_battery[L[0][0]]
  b2 = list_battery[L[1][0]]
  #Calculate utilities of each strategy
  u1 = utiliy(alpha, beta ,gamma,Robot1,task_position,t1,b1,Robot2,task_position,t2,b2,d_max,T_max) # R1 <- Task1 et R2 <- Task1
  u2 = utiliy(alpha, beta ,gamma,Robot1,task_position,t1,b1,Robot2,0,t2,b2,d_max,T_max)# R1 <- Task1 et R2 <- repos
  u3 = utiliy(alpha, beta , gamma,Robot1,0,t1,b1,Robot2,task_position,t2,b2,d_max,T_max) # R1 <- repos et R2 <- Task1
  u4 = utiliy(alpha, beta , gamma,Robot1,0,t1,b1,Robot2,0,t2,b2,d_max,T_max) # R1 <- repos et R2 <- repos
  u1 = sum(list(u1))
  u2 = sum(list(u2))
  u3 = sum(list(u3))
  u4 = sum(list(u4))
  a_list = [u1,u2,u3,u4]
  max_value = max(a_list)
  max_index = a_list.index(max_value)
  #We find the Nash Equilibrium
  if max_index == 1 :
    return L[0][0]
  else :
    return L[1][0]


def utiliy(alpha, beta ,gamma, Robot1,Task1,t1,b1,Robot2,Task2,t2,b2, d_max,Tmax):
  #This is our utility function
  if Task1==0 and  Task2==0 :
    #If R1 and R2 are in resting position (Repos)
    return (0,0)
  if Task1==Task2 :
    # If R1 and R2  have chosen the same task to perform
    return (-1,-1)
  elif Task1==0 :
    # If R1 is at resting position and R2 is performing a task
    distance_robot2_task2 = 3- (beta* math.sqrt( (Robot2[0] - Task2[0])**2 + (Robot2[1] - Task2[1])**2 ))/d_max
    u=distance_robot2_task2-alpha*t2/Tmax + gamma* b2/100
    return (0,u)
  elif Task2==0 :
    # If R2 is at resting position and R1 is performing a task
    distance_robot1_task1 = 3- ( beta*math.sqrt( (Robot1[0] - Task1[0])**2 + (Robot1[1] - Task1[1])**2 ))/d_max
    u=distance_robot1_task1-alpha*t1/Tmax + gamma*b1/100
    return (u,0)
  else :
    #Else : if R1 and R2 are performing 2 differents tasks
    u1 = 3-(beta*math.sqrt( (Robot1[0] - Task1[0])**2 + (Robot1[1] - Task1[1])**2 ))/d_max -alpha*t1/Tmax + gamma* b1/100
    u2 = 3-  (beta*math.sqrt( (Robot2[0] - Task2[0])**2 + (Robot2[1] - Task2[1])**2 ))/d_max -alpha*t2/Tmax + gamma* b2/100
    return (u1,u2)


import math
from matplotlib import pyplot as plt
#alpha beta and gamma are the degrees of freedom, their sum = 1
#list_tasks : The list of tasks that contains the coordinates (x,y) of the tasks // Type : dictionary, Example : list_tasks = { 'T1': (80, 38), 'T2': (78, 37)}
#list_robots : The list of robots which contains the (x,y) coordinates of the robots // Type : dictionary, Example : list_robots = { 'R1': (10, 20), 'R2': (30, 40)}
#list_battery : The list of the battery levels of the robots // Type : dictionary, Example : list_battery = {'R1': 35,'R2': 40} ) (Percentage)
#list_allocation : The possible allocation of each task + the duration of each task by each robot (Who can do this task ? + How long can he do it ?)
# list_allocation (Type : dictionary, Example : list_allocation = list_allocation = {'T1': [('R10', 95), ('R3', 20)], 'T2': [('R9', 43)]) Explanation : T1 can be done by R10 in 95 time units and by R3 in 20 time units
#T_max : Maximum execution time (It is found in list_allocation) Example : list_allocation = {'T1': [('R10', 95), ('R3', 20)], 'T2': [('R9', 43)]) => T_max = 95
#d_max : Maximum distance between a robot and a task
def general_func(alpha, beta, gamma,list_tasks,list_battery,list_robots,list_allocation,T_max,d_max) :
  allocation = {} #allocation is the output that will contains the different allocations of tasks
  distance_totale = 0
  temps_totale=0
  consommation_battery = 0
  #Iteration on tasks (The tasks are ordered)
  for i in list_tasks.keys():
    #If the task can be done by a single robot (conflict = 0) => Direct allocation
    if len(list_allocation[i])==1 :
      allocation[i] = list_allocation[i][0][0]
      temps_totale += list_allocation[i][0][1]
      rob = list_robots[list_allocation[i][0][0]]
      tsk = list_tasks[i]
      distance_parcourue = math.sqrt( (rob[0] - tsk[0])**2 + (rob[1] - tsk[1])**2 )
      distance_totale += distance_parcourue
      list_robots[list_allocation[i][0][0]]  = list_tasks[i]
      list_battery[list_allocation[i][0][0]] =list_battery[list_allocation[i][0][0]] - 5
     #No : the task can be done by 2 or more robots (conflict # 0) => Game theory and equilibrium calculation
    else :
      L = list_allocation[i]
      # L is the list that contains the different robots
      Robot1 = list_robots[L[0][0]]
      Robot2 = list_robots[L[1][0]]
      t1 = L[0][1]
      t2 = L[1][1]
      task_position = list_tasks[i]
      b1 = list_battery[L[0][0]]
      b2 = list_battery[L[1][0]]
      n = len(L)
      A = L
      #Here we will devide the conflict 2 by 2
      while len(A)> 1 :
        H = [A[0],A[1]]
        R = best_robot_within_2_conflict(list_robots,list_battery,H,task_position,alpha,beta,gamma,T_max,d_max)
        if A[0][0] == R :
          A.pop(1)
        else :
          A.pop(0)
      for index in range(len(L)) :
        if L[index][0] == R :
          break
      allocation[i] = R
      temps_totale += L[index][1]
      rob = list_robots[R]
      tsk = list_tasks[i]
      distance_parcourue = math.sqrt( (rob[0] - tsk[0])**2 + (rob[1] - tsk[1])**2 )
      distance_totale += distance_parcourue
      list_robots[R]  = list_tasks[i]
      list_battery[R] -=5
  for i in allocation.values() :
    consommation_battery += list_battery[i]
  return (allocation,distance_totale,temps_totale,consommation_battery)
  #We return the list of allocations, the total distance that has been traveled by robots ,the total time execution of all the tasks and the sum of all battery levels after performing all the tasks