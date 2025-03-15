import psycopg2 

#--------------------------------------------------------
#integrate psycopg2.connect with DB_manager Class
#--------------------------------------------------------
def DB_connect(db_obj):
    
    conn = psycopg2.connect(database=db_obj.db_name,
                                user=db_obj.db_user,
                                password=db_obj.db_pass,
                                host=db_obj.db_host,
                                port=db_obj.db_port)
    return conn
        
    
    
#--------------------------------------------------------
#Database operation with oop
#--------------------------------------------------------
class DB_manager:
    def __init__(self, DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT):
        self.db_name = DB_NAME
        self.db_user = DB_USER
        self.db_pass = DB_PASS
        self.db_host = DB_HOST
        self.db_port = DB_PORT


    #--------------------------------------------------------
    #insert log data to database
    #--------------------------------------------------------
    def insert_Log(self,data,table): #data = {"user_id"  ,  "room",  "time_stamp"}  |  {"plate",  "time_stamp"}
        conn = DB_connect(self)
        cur = conn.cursor()
        if table == "car_log":
             plate = data["plate"]
             time_stamp = data["time_stamp"]
        
             cur.execute(f"""
                INSERT INTO "Access_Control".{table}(plate, time_stamp)
                    VALUES ('{plate}', '{time_stamp}');
            """)
             
        else:
            user_id = data["user_id"]
            time_stamp = data["time_stamp"]
            room = data["room"]

            cur.execute(f"""
                INSERT INTO "Access_Control".{table}(user_id, time_stamp, room)
                    VALUES ('{user_id}', '{time_stamp}', {room});
            """)
        conn.commit()
        cur.close()
        conn.close()


    #--------------------------------------------------------
    #insert user data to database
    #--------------------------------------------------------
    def insert_user(self,data):#data = {"user_id"  ,  "name",  "lastname",   "upd_date",   "image_path"}
        conn = DB_connect(self)
        cur = conn.cursor()

        user_id = data["user_id"]
        name = data["name"]
        lastname = data["lastname"]
        upd_date = data["upd_date"]
        image_path = data["image_path"]
        
        cur.execute(f"""
            INSERT INTO  "Access_Control".user_info(user_id, name, lastname,upd_date, image_path )
                VALUES ('{user_id}', '{name}', '{lastname}','{upd_date}', '{image_path}');
            """)
             
        conn.commit()
        cur.close()
        conn.close()
            
    #--------------------------------------------------------
    #select all users data
    #--------------------------------------------------------
    def fetch_user(self):
        conn = DB_connect(self)
        cur = conn.cursor()
        cur.execute('SELECT * FROM "Access_Control".user_info') #Add Professor
        rows = cur.fetchall()
             
        conn.commit()
        cur.close()
        conn.close()

        return rows
    

# #--------------------------------------------------------
# Test
# #--------------------------------------------------------
if __name__ == "__main__":
   
    #define Constant Data
    #--------------------------------------------------------
    import datetime
    DB_NAME = "Coe_Access_control"
    DB_USER = "postgres"
    DB_PASS = "147258"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    

    db = DB_manager(DB_NAME, 
        DB_USER, 
        DB_PASS, 
        DB_HOST, 
        DB_PORT )
    
    #data = {"user_id"  ,  "room",  "time_stamp"}  |  {"plate",  "time_stamp"}
    time = datetime.datetime.now()
    st_log = {"user_id":"643040531-5"  ,  "room":4101,  "time_stamp": time}
    pf_log = {"user_id":"1"  ,  "room":4101,  "time_stamp": time}
    car_log = {"plate": "ท้อ 100",  "time_stamp": time}

    #data = {"user_id"  ,  "name",  "lastname",  "upd_date",   "image_path"}
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    path = 'C:\\Users\\User\\Desktop\\learning_mother_father_resurrected\\year4.2\\Cloud\\Project\\image'
    st = {"user_id":"643040531-5"  ,  "name": "punnawit",  "lastname" :"yuttagla",  "upd_date":date,   "image_path":path}
    pf = {"user_id":"1"  ,  "name": "Ck",  "lastname": "Boa",  "upd_date":date,   "image_path":path}
    

    #test db connect
    #--------------------------------------------------------
    try:
        conn = DB_connect(db)
        conn.close()
    except Exception as err :
        print(f"db connect failed with this err message:{err}")
    

    # #test select
    # #--------------------------------------------------------
    # try:
    #     rows = db.fetch_user()
    #     print(rows[0][4])

    # except Exception as err :
    #     print(f"select failed with this err message:{err}")


    #test insert user
    #--------------------------------------------------------
    try:
        
        db.insert_user(data= st)
        print("student")

        db.insert_user(data= pf)
        print("professor")

    except Exception as err :
        print(f"insert user failed with this err message:{err}")



#     #test insert log
#     #--------------------------------------------------------
#     try:
        
#         db.insert_Log(data = st_log,table= 'student_log')
#         print("student log")

#         db.insert_Log(data= pf_log,table = 'professor_log')
#         print("professo log")

#         db.insert_Log(data= car_log,table = 'car_log')
#         print("car log")

#     except Exception as err :
#         print(f"insert log failed with this err message:{err}")



