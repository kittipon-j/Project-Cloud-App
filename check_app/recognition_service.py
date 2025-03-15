from common.face_utils import Find_face
from common.db_utils import DB_manager
import datetime
import os
from flask import Flask, jsonify, request,render_template
from flask_cors import CORS

#--------------------------------------------------------
#define Constant Data
#--------------------------------------------------------
DB_NAME = "Coe_Access_control"
DB_USER = "postgres"
DB_PASS = "147258"
DB_HOST = "db" #"localhost"
DB_PORT = "5432"

image_extensions = {'.jpg', '.jpeg', '.png'}  
#--------------------------------------------------------
# กำหนด folder
#--------------------------------------------------------
# กำหนดพาธสำหรับเก็บรูปภาพชั่วคราว
PROJECT_ROOT =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("1root = ",PROJECT_ROOT)
STORAGE_DIR = os.path.join(PROJECT_ROOT, 'data')
print("data= ",STORAGE_DIR)
FACE_IMAGE_DIR = os.path.join(STORAGE_DIR, 'temporary')
print("image= ",FACE_IMAGE_DIR)

# สร้างโฟลเดอร์หลักถ้ายังไม่มี
for directory in [STORAGE_DIR, FACE_IMAGE_DIR]:
    os.makedirs(directory, exist_ok=True)

#--------------------------------------------------------
#define app
#--------------------------------------------------------
app = Flask(__name__)
CORS(app)

#--------------------------------------------------------
#define core function
#--------------------------------------------------------
def recognition(img,db):

    try:  

        rows = db.fetch_user()
        for row in rows:
                
                image_path = row[4]
                num_db = 4
                # num_db = len([
                #     entry for entry in os.listdir(image_path)
                #     if os.path.isfile(os.path.join(image_path, entry)) and
                #     os.path.splitext(entry)[1].lower() in image_extensions
                #     ])

                find_res = Find_face(image = img, 
                                      database= image_path  
                                     )
                
                print(find_res)
                print(len(find_res[0]))
                print(num_db)
                print(row[1])

                if len(find_res[0]) > num_db: #threshold   
                    return {"user_id": row[0] ,
                            "name" : row[1],
                            "lastname" : row[2]}
            

    except Exception as err :
            print(f"recognition failed with this err message:{err}") 
            return None

    return "unknown"


#--------------------------------------------------------
#check face end point
#--------------------------------------------------------
@app.route('/face_check', methods=['POST'])
def face_check():
     
    try:
    
        file = request.files['file'] 
        image_path = os.path.join(FACE_IMAGE_DIR, file.filename)
        file.save(image_path)

        time = datetime.datetime.now()
        print("------------------------TIME1----------------------" ,time)
        db = DB_manager(
            DB_NAME, 
            DB_USER, 
            DB_PASS, 
            DB_HOST, 
            DB_PORT )
        
        check_res = recognition(img = image_path,db = db)
        os.remove(image_path)

        time2 = datetime.datetime.now()
        print("------------------------TIME2 ========" ,time2-time)
        if check_res == None:
            return jsonify({"success": False,  "case":"ไม่พบใบหน้าในรูปภาพ" }),400

        elif check_res == "unknown":
            return jsonify({"success": False,  "case":"ไม่พบใบหน้าในฐานข้อมูล"}),200

        else:
            #data = {"user_id":check_res["user_id"]  ,"name":check_res["name"] ,"lastname":check_res["lastaname"]  ,"upd_date":date ,  "room":4101,  "time_stamp":time} #Need Room mother fucker 
            data = {"user_id":check_res["user_id"]  , "room":4101,  "time_stamp":time}  
            db.insert_Log(data = data, table ="user_log")  
            return  jsonify({"success": True,  "name":check_res["name"] +" "+ check_res["lastname"]   ,"user_id":check_res["user_id"] }),200
        
    except Exception as err :
            return  jsonify({"success": False,  "case": err  }),500
    
#--------------------------------------------------------
#Home
#--------------------------------------------------------
@app.route('/')
def main():
    return render_template("Index.html")   


#--------------------------------------------------------
#Run the app
#--------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)











