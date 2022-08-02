import numpy as np
import pandas as pd
import matplotlib
import seaborn

def getData(n, th=60, min3=0.8, min2=0.7, min1=0.6):
    raw_df = pd.read_excel(n)


    smaller_df = raw_df.loc[:, :]





    def grade_to_mark(grade):
        grades = {
            "O": 10,
            "A+": 9,
            "A": 8,
            "B+": 7,
            "B": 6
        }
        if grade in grades:
            return grades[grade]
        return 0




    marks = []
    for i in smaller_df['END SEM GRADE']:
        marks.append(grade_to_mark(i) * 10 / 5)



    smaller_df.loc[:,'CO1 (20)'] = marks
    smaller_df.loc[:,'CO2 (20)'] = marks
    smaller_df.loc[:,'CO3 (20)'] = marks
    smaller_df.loc[:,'CO4 (20)'] = marks
    smaller_df.loc[:,'CO5 (20)'] = marks



    CO1_CAT = (smaller_df['CO1 (32)'] + smaller_df['Assgn(5)'])/37 * 100
    smaller_df.loc[:, 'CO1_CAT'] = CO1_CAT.round()
    CO2_CAT = (smaller_df['CO2 (18)'] + smaller_df['Assgn(5).1'] + smaller_df['CO2 (18).1'] + smaller_df['Assgn(5).2'])/46*100
    smaller_df.loc[:, 'CO2_CAT'] = CO2_CAT.round()
    CO3_CAT = (smaller_df['CO3 (32)'] + smaller_df['Assgn(5).3'])/37*100
    smaller_df.loc[:, 'CO3_CAT'] = CO3_CAT.round()
    CO4_CAT = (smaller_df['CO4 (25)'] + smaller_df['Assgn(5).4'])/30*100
    smaller_df.loc[:, 'CO4_CAT'] = CO4_CAT.round()
    CO5_CAT = (smaller_df['CO5 (25)'] + smaller_df['Assgn(5).5'])/30*100
    smaller_df.loc[:, 'CO5_CAT'] = CO5_CAT.round()


    smaller_df['CO1_ES'] = smaller_df['CO1 (20)'] * 100 / 20
    smaller_df['CO2_ES'] = smaller_df['CO1 (20)'] * 100 / 20
    smaller_df['CO3_ES'] = smaller_df['CO1 (20)'] * 100 / 20
    smaller_df['CO4_ES'] = smaller_df['CO1 (20)'] * 100 / 20
    smaller_df['CO5_ES'] = smaller_df['CO1 (20)'] * 100 / 20


    def print_CO_attainment(course_number, cat_marks, endsem_marks, cat_threshold, endsem_threshold):
        global courseOutcome_df
        cat_attainment = (cat_marks[cat_marks>cat_threshold].count()) / cat_marks.size
        endsem_attainment = endsem_marks[endsem_marks>endsem_threshold].count() / endsem_marks.size
        # print(course_number , "\t", cat_attainment.round(3), "\t", endsem_attainment.round(3))
        courseOutcome_df = courseOutcome_df.append({'Unit' : course_number, 'Cat_Attainment' : cat_attainment.round(3), 'ES_Attainment': endsem_attainment.round(3), 'Total_Attainment':((cat_attainment.round(3)+endsem_attainment.round(3))/2).round(3) }, ignore_index=True)
        if (courseOutcome_df.loc[course_number-1, 'Total_Attainment']>=min3):
            courseOutcome_df.loc[course_number-1, 'Attainment_Score']=3
        elif (courseOutcome_df.loc[course_number-1, 'Total_Attainment']>=min2):
            courseOutcome_df.loc[course_number-1, 'Attainment_Score']=2
        elif (courseOutcome_df.loc[course_number-1, 'Total_Attainment']>=min1):
            courseOutcome_df.loc[course_number-1, 'Attainment_Score']=1
        else:
            courseOutcome_df.loc[course_number-1, 'Attainment_Score']=0
        # print(courseOutcome_df.loc[0, 'Total_Attainment'])

    # print("course\tCat-Atmt ES-Atmt")
    global courseOutcome_df
    courseOutcome_df = pd.DataFrame(columns = ['Unit', 'Cat_Attainment', 'ES_Attainment'])
    print_CO_attainment(1, smaller_df['CO1_CAT'], smaller_df['CO1_ES'], th, th)
    print_CO_attainment(2, smaller_df['CO2_CAT'], smaller_df['CO2_ES'], th, th)
    print_CO_attainment(3, smaller_df['CO3_CAT'], smaller_df['CO3_ES'], th, th)
    print_CO_attainment(4, smaller_df['CO4_CAT'], smaller_df['CO4_ES'], th, th)
    print_CO_attainment(5, smaller_df['CO5_CAT'], smaller_df['CO5_ES'], th, th)

    return smaller_df.iloc[:,[0,19,20,21,22,23,24,25,26,27,28]], courseOutcome_df


courseOutcome_df = pd.DataFrame(columns = ['Unit', 'Cat_Attainment', 'ES_Attainment', 'Total_Attainment', 'Attainment_Score'])