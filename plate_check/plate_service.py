from common.db_utils import DB_manager
import datetime
import os
from flask import Flask, jsonify, request,render_template
from flask_cors import CORS
import cv2
from ultralytics import YOLO

#--------------------------------------------------------
#define Constant Data
#--------------------------------------------------------
DB_NAME = "Coe_Access_control"
DB_USER = "postgres"
DB_PASS = "147258"
DB_HOST = "db" #"localhost"
DB_PORT = "5432"

text_dict = {
 'A01': 'ก',
 'A02': 'ข',
 'A03': 'ฃ',
 'A04': 'ค',
 'A05': 'ฅ',
 'A06': 'ฆ',
 'A07': 'ง',
 'A08': 'จ',
 'A09': 'ฉ',
 'A10': 'ช',
 'A11': 'ซ',
 'A12': 'ฌ',
 'A13': 'ญ',
 'A14': 'ฎ',
 'A15': 'ฏ',
 'A16': 'ฐ',
 'A17': 'ฑ',
 'A18': 'ฒ',
 'A19': 'ณ',
 'A20': 'ด',
 'A21': 'ต',
 'A22': 'ถ',
 'A23': 'ท',
 'A24': 'ธ',
 'A25': 'น',
 'A26': 'บ',
 'A27': 'ป',
 'A28': 'ผ',
 'A29': 'ฝ',
 'A30': 'พ',
 'A31': 'ฟ',
 'A32': 'ภ',
 'A33': 'ม',
 'A34': 'ย',
 'A35': 'ร',
 'A36': 'ล',
 'A37': 'ว',
 'A38': 'ศ',
 'A39': 'ษ',
 'A40': 'ส',
 'A41': 'ห',
 'A42': 'ฬ',
 'A43': 'อ',
 'A44': 'ฮ',
 '0': '0',
 '1': '1',
 '2': '2',
 '3': '3',
 '4': '4',
 '5': '5',
 '6': '6',
 '7': '7',
 '8': '8',
 '9': '9'}



province_dict = {'CMI': 'เชียงใหม่',
 'NMA': 'นครราชสีมา',
 'KRI': 'กาญจนบุรี',
 'UBN': 'อุบลราชธานี',
 'TAK': 'ตาก',
 'SNI': 'สุราษฎร์ธานี',
 'CPM': 'ชัยภูมิ',
 'MSN': 'แม่ฮ่องสอน',
 'PNB': 'เพชรบูรณ์',
 'LPG': 'ลำปาง',
 'UDN': 'อุดรธานี',
 'CRI': 'เชียงราย',
 'NAN': 'น่าน',
 'LEI': 'เลย',
 'KKN': 'ขอนแก่น',
 'PLK': 'พิษณุโลก',
 'BRM': 'บุรีรัมย์',
 'NST': 'นครศรีธรรมราช',
 'SNK': 'สกลนคร',
 'NSN': 'นครสวรรค์',
 'SSK': 'ศรีสะเกษ',
 'KPT': 'กำแพงเพชร',
 'RET': 'ร้อยเอ็ด',
 'SRN': 'สุรินทร์',
 'UTT': 'อุตรดิตถ์',
 'SKA': 'สงขลา',
 'SKW': 'สระแก้ว',
 'KSN': 'กาฬสินธุ์',
 'UTI': 'อุทัยธานี',
 'STI': 'สุโขทัย',
 'PRE': 'แพร่',
 'PKN': 'ประจวบคีรีขันธ์',
 'CTI': 'จันทบุรี',
 'PYO': 'พะเยา',
 'PBI': 'เพชรบุรี',
 'LRI': 'ลพบุรี',
 'CPN': 'ชุมพร',
 'NPM': 'นครพนม',
 'SPB': 'สุพรรณบุรี',
 'MKM': 'มหาสารคาม',
 'CCO': 'ฉะเชิงเทรา',
 'RBR': 'สมุทรสงคราม',
 'TRG': 'ตรัง',
 'PRI': 'ปราจีนบุรี',
 'KBI': 'กระบี่',
 'PCT': 'พิจิตร',
 'YLA': 'ยะลา',
 'LPN': 'ลำพูน',
 'NWT': 'นราธิวาส',
 'CBI': 'ชลบุรี',
 'MDH': 'มุกดาหาร',
 'BKN': 'บึงกาฬ',
 'PNA': 'พังงา',
 'YST': 'ยโสธร',
 'NBP': 'หนองบัวลำภู',
 'SRI': 'สระบุรี',
 'RYG': 'ระยอง',
 'PLG': 'พัทลุง',
 'RNG': 'ระนอง',
 'ACR': 'อำนาจเจริญ',
 'NKI': 'หนองคาย',
 'TRT': 'ตราด',
 'AYA': 'พระนครศรีอยุธยา',
 'STN': 'สตูล',
 'CNT': 'ชัยนาท',
 'NPT': 'นครปฐม',
 'NYK': 'นครนายก',
 'PTN': 'ปัตตานี',
 'BKK': 'กรุงเทพมหานคร',
 'PTE': 'ปทุมธานี',
 'SPK': 'สมุทรปราการ',
 'ATG': 'อ่างทอง',
 'SKN': 'สมุทรสาคร',
 'NBI': 'นนทบุรี',
 'TKT': 'สิงห์บุรี',
 'SKM': 'ภูเก็ต' }

#--------------------------------------------------------
# กำหนด folder
#--------------------------------------------------------
# กำหนดพาธสำหรับเก็บรูปภาพชั่วคราว
PROJECT_ROOT =os.path.dirname(os.path.abspath(__file__))
print("root = ",PROJECT_ROOT)
PLATE_IMAGE_DIR = os.path.join(PROJECT_ROOT, 'data')
print("data= ",PLATE_IMAGE_DIR)
MODEL_DIR = os.path.join(PROJECT_ROOT, 'model')
print("model= ",PLATE_IMAGE_DIR)

# สร้างโฟลเดอร์หลักถ้ายังไม่มี
for directory in [ PLATE_IMAGE_DIR]:
    os.makedirs(directory, exist_ok=True)


detect_threshold = 0.5
extract_threshold = 0.1

detector_path = os.path.join(MODEL_DIR, 'detect_yolov11n.pt')
license_plate_detector = YOLO (detector_path)

extract_path = os.path.join(MODEL_DIR, 'extract_yolov11m.pt')
text_extractor = YOLO (extract_path)

print(detector_path)
print(extract_path)
#--------------------------------------------------------
#define app
#--------------------------------------------------------
app = Flask(__name__)
CORS(app)

#--------------------------------------------------------
#define core function
#--------------------------------------------------------

#Function to detect and crop plate image
def Plate_Detector(img):
    try:
        results = license_plate_detector(img, conf=detect_threshold)

        img = cv2.imread(img)
        for i, det in enumerate(results[0].boxes.xyxy):
            # Extract bounding box coordinates
            x1, y1, x2, y2 = map(int, det[:4])

            # Crop the image using the bounding box
            crop_img = img[y1:y2, x1:x2]

            # Define the path to save the cropped image
            crop_path = f'cropped_image_{i}.jpg'
            crop_path = os.path.join(PLATE_IMAGE_DIR, crop_path)

            # Save the cropped image
            cv2.imwrite(crop_path, crop_img)
            print(f'Cropped image saved to {crop_path}')

            return crop_path
            

    except Exception as err :
            print(f"detectc failed with this err message:{err}") 

            return None
    

#Function to do OCR
def Text_Extractor(img):

    try:   
        # Run detection on the image
        results = text_extractor(img, conf=extract_threshold)

        data = {}
        # Sort by confidence before looping
        sorted_results = sorted(results[0].boxes.data, key=lambda x: x[4])

        # Print predicted classes and their confidence
        for result in sorted_results:
            class_id = int(result[5])  # Class index
            confidence = result[4]  # Confidence score
            class_name = text_extractor.names[class_id]  # Get the class name
            data[int(result[0])] = class_name
            print(f"Predicted Class: {class_name}, Confidence: {confidence:.2f}")


        myKeys = list(data.keys())
        myKeys.sort()

        # Sorted Dictionary
        sd = [data[i] for i in myKeys]

        plates = []
        pro =  " ไม่เจอจังหวัดครับ"
        
        for i in sd :
            if i in province_dict.keys():
                pro = " " + province_dict[i]
            else:
                plates.append(text_dict[i])

        plates.append(pro)


        tabeun = ""
        for i in plates:
            tabeun += i
        
        print("ทะเบียน: ", tabeun)

        return tabeun

    except Exception as err :
            print(f"extract failed with this err message:{err}") 
            return None




#--------------------------------------------------------
#check face end point
#--------------------------------------------------------
@app.route('/plate_check', methods=['POST'])
def plate_check():
     
    try:
    
        file = request.files['file'] 
        image_path = os.path.join(PLATE_IMAGE_DIR, file.filename)
        file.save(image_path)

        time = datetime.datetime.now()
        db = DB_manager(
            DB_NAME, 
            DB_USER, 
            DB_PASS, 
            DB_HOST, 
            DB_PORT )
        
        crop_path = Plate_Detector(image_path)

        if crop_path == None :
            return jsonify({"success": False,  "case":"error อะไรสักอย่างครับ" }),400
        
        res = Text_Extractor(crop_path)

        if res == None:
            return jsonify({"success": False,  "case":"error อะไรสักอย่างครับ" }),400
        
        os.remove(image_path)
        os.remove(crop_path)
       

        data = {"plate":res,  "time_stamp":time}  
        db.insert_Log(data = data, table ="car_log")  
        return  jsonify({"success": True,  "plate":res}),200
        
    except Exception as err :
            return  jsonify({"success": False,  "case": err  }),500
    
#--------------------------------------------------------
#Home
#--------------------------------------------------------


#--------------------------------------------------------
#Run the app
#--------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)











