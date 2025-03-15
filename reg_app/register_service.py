from flask import Flask, request, jsonify
import cv2
import os
import datetime
from flask_cors import CORS

from common.face_utils import Find_face
from common.db_utils import DB_manager

#--------------------------------------------------------
#define Constant Data
#--------------------------------------------------------
DB_NAME = "Coe_Access_control"
DB_USER = "postgres"
DB_PASS = "147258"
DB_HOST = "db"
DB_PORT = "5432"

#--------------------------------------------------------
#define app
#--------------------------------------------------------
app = Flask(__name__)
CORS(app)

#--------------------------------------------------------
#define core function
#--------------------------------------------------------
def embed_vdo(db):

    try:
        img = [0]*4096

        find_res = Find_face(img ,database= db)
    
        return True
   
    except Exception as err :
            print(f"recognition failed with this err message:{err}") 
            return False

    

#--------------------------------------------------------
# กำหนด folder
#--------------------------------------------------------

# กำหนดพาธสำหรับเก็บรูปภาพ
# ย้ายที่เก็บรูปภาพไปยังโฟลเดอร์ data ที่อยู่นอก src ไปอีก 1 โฟลเดอร์
PROJECT_ROOT =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("1root = ",PROJECT_ROOT)
STORAGE_DIR = os.path.join(PROJECT_ROOT, 'data')
print("data= ",STORAGE_DIR)
FACE_IMAGE_DIR = os.path.join(STORAGE_DIR, 'face-images')
print("image= ",FACE_IMAGE_DIR)

# สร้างโฟลเดอร์หลักถ้ายังไม่มี
for directory in [STORAGE_DIR, FACE_IMAGE_DIR]:
    os.makedirs(directory, exist_ok=True)


#--------------------------------------------------------
# กำหนด folder
#--------------------------------------------------------
@app.route('/api/process-video', methods=['POST'])
def process_video():
    try:
        if 'video' not in request.files:
            return jsonify({'success': False, 'message': 'ไม่พบไฟล์วิดีโอ'}), 400

        video_file = request.files['video']
        user_id = request.form.get('user_id')
        name = request.form.get('name')
        lastname = request.form.get('lastname')


        if not (video_file or not user_id) or (not name or not lastname):
            return jsonify({'success': False, 'message': 'ข้อมูลไม่ครบถ้วน'}), 400

        # สร้างโฟลเดอร์สำหรับเก็บรูปของนักศึกษา
        student_folder = os.path.join(FACE_IMAGE_DIR, user_id)
        os.makedirs(student_folder, exist_ok=True)

        # บันทึกวิดีโอชั่วคราว
        temp_video_path = os.path.join(student_folder, 'temp_video.mp4')
        video_file.save(temp_video_path)

        # อ่านวิดีโอและแยกเฟรม
        cap = cv2.VideoCapture(temp_video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_count = 0
        saved_frames = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # บันทึกเฟรมทุกๆ 2 วินาที
            if frame_count % fps//2 == 0:
                # เปลี่ยนชื่อไฟล์เป็นรหัสผู้ใช้งานตามด้วยลำดับ
                frame_path = os.path.join(student_folder, f'{user_id}_{saved_frames:03d}.jpg')
                cv2.imwrite(frame_path, frame)
                saved_frames += 1

            frame_count += 1

        cap.release()

        # ลบไฟล์วิดีโอชั่วคราว
        os.remove(temp_video_path)

        # student_folder
        if(embed_vdo(student_folder)):

            db = DB_manager(
            DB_NAME, 
            DB_USER, 
            DB_PASS, 
            DB_HOST, 
            DB_PORT )
            date = datetime.datetime.today().strftime('%Y-%m-%d')
            data = {"user_id":user_id  ,  "name":name,  "lastname":lastname,   "upd_date":date,   "image_path": student_folder}
            db.insert_user(data =data)

        else:
            return jsonify({
            'success': False,
            'message': 'เกิดข้อผิดพลาด:ไม่สามารถแปลงวิดีโอเป็นเวกเตอร์ได้ '
        }), 500

        
        return jsonify({
            'success': True,
            'message': 'ประมวลผลวิดีโอสำเร็จ',
            'framesCount': saved_frames,
            'studentFolder': student_folder
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'เกิดข้อผิดพลาด: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)