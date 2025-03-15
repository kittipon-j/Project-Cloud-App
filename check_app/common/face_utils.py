#--------------------------------------------------------
#import dependency
#--------------------------------------------------------
from deepface import DeepFace
import os.path

#--------------------------------------------------------
#define Constant Data
#--------------------------------------------------------
Models = [
    "VGG-Face", 
    "Facenet", 
    "Facenet512"
]
DEFAULT_model = Models[0]
   

DEFAULT_backends = [
    'yolov8',
    "fastmtcnn",
]
DEFAULT_backend = 'yolov8'

metrics = ["cosine", "euclidean", "euclidean_l2"]
DEFAULT_metrics = metrics[0]


#--------------------------------------------------------
#Embedd Function
#--------------------------------------------------------
def Embed_face(image, model = DEFAULT_model, backends = DEFAULT_backends ):


    for backend in backends:
        try:
            embedding_objs = DeepFace.represent( 
                img_path = image,
                model_name= model,
                detector_backend = backend
            )

            embeddings = [obj["embedding"] for obj in embedding_objs]
            
            return {"vector":embeddings,
                    "model" :model,
                    "face" :len(embeddings),
                    "detector": backend}
            
        except Exception as err :
            print(f"Embed Detector:{backend} failed with this err message:{err}") 

    return None


#--------------------------------------------------------
#Detect Function
#--------------------------------------------------------
def Detect_face(image, backends = DEFAULT_backends ):                    #case1 เช็คว่าหลังจากแตก vdo เป็นรูปแล้ว detect เจอหน้ากี่ %
                                                                    #case2 เช็คว่า 4 รูปเจอหน้าทั้งหมดมั้ย + มีคนเดียวรึป่าว
     for backend in backends:
        try:
            face_objs = DeepFace.extract_faces(
                img_path = image, 
                detector_backend = backend,
                align = True,
            )

            face_detected = [obj["face"] for obj in face_objs]
            
            return {"face": face_detected ,
                    "detector": backend}
            
        except Exception as err :
            print(f"Detector:{backend} failed with this err message:{err}") 

     return None
    

#--------------------------------------------------------
#Recognition function
#--------------------------------------------------------
def Find_face(image, database, model = DEFAULT_model, backend = DEFAULT_backend , metric = DEFAULT_metrics):
    try:
        # Ensure image is a valid path string
        if isinstance(image, list):
            raise ValueError("Image input must be a path string, not a list")
            
        if not os.path.exists(image):
            raise ValueError(f"Image path does not exist: {image}")

        # face recognition
        dfs = DeepFace.find(
            img_path = image,
            model_name = model,
            detector_backend = backend,
            db_path = database, 
            distance_metric = metric,
            threshold = 0.58
        )

        return dfs

    except Exception as err:
        print(f"Find Detector: {backend} failed with this err message: {err}")
        return None


# #--------------------------------------------------------
# #Recognition function2
# #--------------------------------------------------------
# def Find_face(image, database, model = DEFAULT_model, backend = DEFAULT_backend , metric = DEFAULT_metrics):

    
#     try:
#             #face recognition
#             dfs = DeepFace.find(
#                 img_path = image,
#                 model_name = model,
#                 detector_backend = backend,
#                 db_path = database, 
#                 distance_metric = metric
#             )

#             return dfs

#     except Exception as err :
#             print(f"Find Detector:{backend}with this err message:{err}")
     


         
if __name__ == "__main__":
    



    #--------------------------------------------------------
    #Test Detection
    #--------------------------------------------------------
    # image_detect = "image\\image9.jpg"
    # res = Detect(image_detect, backends = DEFAULT_backends )
    # print(len(res["face"]))


    #--------------------------------------------------------
    #Test Find
    #--------------------------------------------------------
    image1 = 'image\\image2.jpg'
    db = "image2"
    res = Find_face(image1, db )
    print(res)

    # img1_path = res[0]["identity"][0]
    # img2_path = res[0]["identity"][1]
    # import cv2 
    # import numpy as np 
    
    # # Read First Image 
    # img1 = cv2.imread(img1_path)
    # img1 = cv2.resize(img1, (780, 540), 
    #            interpolation = cv2.INTER_LINEAR)
    
    # # Read Second Image 
    # img2 = cv2.imread(img2_path) 
    # img2 = cv2.resize(img2, (780, 540), 
    #            interpolation = cv2.INTER_LINEAR)
    
    # # concatenate image Horizontally 
    # Hori = np.concatenate((img1, img2), axis=1) 
    
    # cv2.imshow('VERTICAL', Hori) 
    
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows() 


    #--------------------------------------------------------
    #Test Embedd 
    #--------------------------------------------------------
    # image1 = 'image\\image2.jpg'
    # embedded = Embed_face(image1)
    # a=[0]*4096
    # print(a)
    # print(len(embedded["vector"][0]))

    


    