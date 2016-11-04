import sqlite3

netid = "sanilk2.result"
social_db = "./data/social.db"
matrix_db = "./data/matrix.db"
university_db = "./data/university.db"
query_1 = """select name from student where grade = 9 order by name;"""

query_2 = """select grade, count(id) as count from student group by grade order by grade;"""

query_3 = """select name, grade from student where student.id IN (select id1 from friend group by id1 having count(id2) > 2) order by name, grade;"""

query_4 = """select s1.name, s1.grade from student s, student s1, likes l where l.id2 = s1.id and l.id1 = s.id and s.grade > s1.grade order by s1.name, s1.grade;"""

query_5 = """select name, grade from student where student.id IN (select f.id1 from friend f, likes l where f.id1 = l.id1 and f.id2 = l.id2) UNION select name, grade from student where student.id NOT IN (select id1 from likes) order by name, grade;"""

query_6 = """select l.id1 as ID1, s.name as name1, l.id2 as ID2, s1.name as name2 from student s, student s1, likes l where s.id = l.id1 and s1.id = l.id2 and s.id <> s1.id and l.id2 NOT IN (select f.id2 from friend f where l.id1 = f.id1) order by l.id1, l.id2;"""

query_7 = """select first.id1 as ID1, s.name as name1, first.id2 as ID2, s1.name as name2, f.id2 as ID3, s2.name as name3 from (select l.id1, l.id2 from Likes l  where l.id2 NOT IN (select f1.id2 from friend f1 where f1.id1=l.id1)) as first, friend f, student s, student s1, student s2 where first.id1=f.id1  and f.id2 IN (select f2.id2 from friend f2 where first.id2=f2.id1) and first.id1=s.id and first.id2=s1.id and f.id2=s2.id order by first.id1, first.id2, f.id2;"""

#University DB. Since there are only 10 queries in all, I thought it would be better to start this from 8.
query_8 = """select tenured, avg(class_score) from Fact_Course_Evaluation f, Dim_Professor p where p.id= f.professor_id group by tenured;"""

query_9 = """select year, area, avg(class_score) as avg_score from Fact_Course_Evaluation f, Dim_type d, Dim_term t where d.id= f.type_id and f.term_id=t.id group by d.area, t.year order by t.year, d.area;"""

#Matrix.DB
query_10 = """select A.row_num as row_num, B.col_num as col_num, sum(A.value * B.value) as value from A, B where A.col_num = B.row_num group by A.row_num, B.col_num order by A.row_num, B.col_num;"""

################################################################################

def get_query_list():
    """
    Form a query list for all the queries above
    """
    query_list = []
    for index in range(1, 11):
        eval("query_list.append(query_" + str(index) + ")")
    # end for
    return query_list
    pass

def output_result(index, result):
    """
    Output the result of query to facilitate autograding.
    Caution!! Do not change this method
    """
    with open(netid, 'a') as fout:
        fout.write("<"+str(index)+">\n")
    with open(netid, 'a') as fout:
        for item in result:
            fout.write(str(item))
            fout.write('\n')
        #end for
    #end with
    with open(netid, 'a') as fout:
        fout.write("</"+str(index) + ">\n")
    pass

def run():
    ## get all the query list
    query_list = get_query_list()

    ## problem 1
    conn = sqlite3.connect(social_db)
    cur = conn.cursor()
    for index in range(0, 7):
        cur.execute(query_list[index])
        result = cur.fetchall()
        tag = "q" + str(index+1)
        output_result(tag, result)
    #end for

	##Problem 2
	conn = sqlite3.connect(university_db)
    cur = conn.cursor()
    for index in range(7, 9):
        cur.execute(query_list[index])
        result = cur.fetchall()
        tag = "q" + str(index+1)
        output_result(tag, result)


    ##problem 3
	conn = sqlite3.connect(matrix_db)
    cur = conn.cursor()
    for index in range(9, 10):
        cur.execute(query_list[index])
        result = cur.fetchall()
        tag = "q" + str(index+1)
        output_result(tag, result)

    #end run()


if __name__ == '__main__':
    run()
