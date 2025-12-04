import torch
import numpy as np
import cv2
import time 
import easyocr
import csv
from datetime import datetime, date
import re
import onnxruntime
import threading
import gc
from PIL import Image, ImageDraw, ImageFont
import os
class licensePlate:

    def __init__(self, onnx_file, ort_provider=['CUDAExecutionProvider', 'CPUExecutionProvider']):
        
        self.classes = ["license plate"]
        self.reader = easyocr.Reader(['th'] ,gpu=True)
        self.ort_session, self.input_names, self.output_names = self.load_model(onnx_file, ort_provider)
        self.show_result = ''
        self.real_result = ''
        self.list=[]
        self.check=1
        self.count=0


    def load_model(self, model_name, ort_provider):

        opt_session = onnxruntime.SessionOptions()
        opt_session.enable_mem_pattern = False
        opt_session.enable_cpu_mem_arena = False
        opt_session.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_DISABLE_ALL

        ort_session = onnxruntime.InferenceSession(model_name, providers=ort_provider)
        model_inputs = ort_session.get_inputs()
        model_output = ort_session.get_outputs()

        input_names = [model_inputs[i].name for i in range(len(model_inputs))]
        output_names = [model_output[i].name for i in range(len(model_output))]

        return ort_session, input_names, output_names

    def predict(self, input_tensor, conf_thresold=0.6):

        outputs = self.ort_session.run(self.output_names, {self.input_names[0]: input_tensor})[0]
        predictions = np.squeeze(outputs).T

        # Filter out object confidence scores below threshold
        scores = np.max(predictions[:, 4:], axis=1)
        predictions = predictions[scores > conf_thresold, :]
        scores = scores[scores > conf_thresold]  

        #class_ids = np.argmax(predictions[:, 4:], axis=1)

        # Get bounding boxes for each object
        boxes = predictions[:, :4]
        num_box = self.select_box(boxes)
        #rescale box
        input_shape = np.array([input_width, input_height, input_width, input_height])
        boxes = np.divide(boxes, input_shape, dtype=np.float32)
        boxes *= np.array([image_width, image_height, image_width, image_height])
        boxes = boxes.astype(np.int32)

        #indices = self.nms(boxes, scores, 0.3)

        return boxes, num_box

    def compute_iou(self, box, boxes):
        # Compute xmin, ymin, xmax, ymax for both boxes
        xmin = np.maximum(box[0], boxes[:, 0])
        ymin = np.maximum(box[1], boxes[:, 1])
        xmax = np.minimum(box[2], boxes[:, 2])
        ymax = np.minimum(box[3], boxes[:, 3])

        # Compute intersection area
        intersection_area = np.maximum(0, xmax - xmin) * np.maximum(0, ymax - ymin)

        # Compute union area
        box_area = (box[2] - box[0]) * (box[3] - box[1])
        boxes_area = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
        union_area = box_area + boxes_area - intersection_area

        # Compute IoU
        iou = intersection_area / union_area

        return iou
    
    def select_box(self, boxes):
        select_box = []
        
        if len(boxes)>0:
            size_box = [w*h for x,y,w,h in boxes ]
            select_box = [np.argmax(size_box)]

        return select_box

    def xywh2xyxy(self, x):
        # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
        y = np.copy(x)
        y[..., 0] = x[..., 0] - x[..., 2] / 2
        y[..., 1] = x[..., 1] - x[..., 3] / 2
        y[..., 2] = x[..., 0] + x[..., 2] / 2
        y[..., 3] = x[..., 1] + x[..., 3] / 2

        return y

    def preview(self, image, boxes, num_box):

        image_draw = image.copy()
        if len(boxes)> 0 :
            bbox = self.xywh2xyxy(boxes[num_box])[0]
            bbox = bbox.round().astype(np.int32).tolist() 
            color = (0,255,0)
            cv2.rectangle(image_draw, tuple(bbox[:2]), tuple(bbox[2:]), color, 2)
        
        return image_draw

    def preprocess(self, image, alpha = 2.0, beta = 90):
        # แปลงภาพสีเป็นภาพขาว-ดำ
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
          
        return gray

    def ocr(self, image, alpha = 2.0, beta = 90):
        adjusted = self.preprocess(image=image, alpha=alpha, beta=beta)
        return self.reader.readtext(adjusted, detail=0)
    
    def select_result(self, results):

        join_result= "".join(results)
        join_result = join_result.replace(" ", "")
        join_result = join_result.replace("า", "ว")
        pattern = re.compile("[^ก-ฮ\d]")
        join_result = pattern.sub("", join_result)

        prefix = join_result[:3]
        suffix = join_result[3:]
        #select only number in suffix
        suffix = re.sub(r'\D', '', suffix) 
        #check suffix that is less than 4 ?
        # check prefix that have a char ? and check prefix that have numeric < 2 ?
        if len(suffix) < 5 and sum(char.isalpha() for char in prefix) > 0 and sum(char.isalpha() for char in prefix) < 3 and sum(char.isdigit() for char in prefix) < 2 :
            result = prefix + suffix
            province = join_result[len(result):]
        else :
            result = ''
            province = ''

        if len(result) < 2 or len(result) > 8 :
            result = ''
            
        return result,province
    
    def test(self, img):
        
        result = self.ocr(image=img, alpha=3.0, beta=100)
        print('ori = ',result)
        result,province = self.select_result(result)
        if len(result) > 0:
            self.show_result = result
            print('true = ',result)
        self.real_result = result

    def pil2cv2(self,img,text,bbox):
        # Create a Pillow image object from the OpenCV image
        pillow_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # Create a Pillow draw object
        draw = ImageDraw.Draw(pillow_img)
        # Set the font type and size
        

        # Load Segoe UI font
        font_path = r"C:\Windows\Fonts\segoeui.ttf"  # or any other path where the font is installed
        font = ImageFont.truetype(font_path, size=16)
        #font = ImageFont.truetype('Arial Unicode.ttf', size=40)
        # Set the text position
        position = (bbox[0], bbox[1] - 2)
        # Set the text color
        font_color = (255, 0, 0)
        # Write the Thai text on the image
        draw.text(position, text, font=font, fill=font_color)
        # Convert the Pillow image back to OpenCV format
        img_with_text = cv2.cvtColor(np.array(pillow_img), cv2.COLOR_RGB2BGR)
        
        return img_with_text

    def save_to_csv(self, frame):
        if self.real_result != '' :
            self.list.append(self.real_result)
            print(self.list)
            if len(self.list) == 2 :
                if self.list[0] == self.list[1]:
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    today = date.today()
                    current_day = today.strftime("%d/%m/%Y")

                    pic_name = str(current_day) + '_' + str(current_time) + '.jpg'
                    pic_name = pic_name.replace('/','_')
                    pic_name = pic_name.replace(':','_')
                    cv2.imwrite('image_car/' + pic_name, frame)
                    data = [current_time, current_day, pic_name, self.real_result]
                    if os.path.isfile('ocr_results.csv'):
                        with open('ocr_results.csv', 'a', encoding="utf-8") as file:
                            writer = csv.writer(file)
                            writer.writerow(data)
                    else:
                        header = ['Time', 'Date', 'Image_name', 'License_Plate']
                        with open('ocr_results.csv', 'a', encoding="utf-8" ) as file:
                            writer = csv.writer(file)
                            writer.writerow(header)
                            writer.writerow(data)
                    self.check = 0
                    self.list = []
                else:
                    self.list = []
    
    def check_plate(self, input_tensor, frame):
        
        boxes, num_box = self.predict(input_tensor)
        image_preview = license_plate.preview(frame, boxes, num_box)
        cv2.putText(image_preview,'Complete!',(1600, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        cv2.putText(image_preview,'PLEASE TAKE A LICENSE PLATE OUT OF THE SCREEN ! ',(300, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 5)
        if len(boxes) == 0:
            self.count += 1
        if len(boxes) > 0:
            self.count = 0
        if self.count == 30:
            self.check = 1
            self.count = 0
            self.show_result = ''
            self.real_result = ''

        return image_preview
    
    def create_folder(self, folder_name):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print("Folder created successfully!")
        else:
            print("Folder already exists.")

license_plate = licensePlate(onnx_file="last.onnx")
vid = cv2.VideoCapture(0)
i = 0
license_plate.create_folder('image_car')

while True :
    i+=1
    start_time = time.time()
    ret, frame = vid.read()
    if ret == 1 :
        image_height, image_width = frame.shape[:2]
        Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        input_height, input_width = 640, 640
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(image_rgb, (input_width, input_height))

        # Scale input pixel value to 0 to 1
        input_image = resized / 255.0
        input_image = input_image.transpose(2,0,1)
        input_tensor = input_image[np.newaxis, :, :, :].astype(np.float32)
        if license_plate.check == 1:
            boxes, num_box= license_plate.predict(input_tensor)
            image_preview = license_plate.preview(frame, boxes, num_box)
            cv2.putText(image_preview,'Processing...',(1600, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
            text = ''
            if len(boxes) > 0 and i % 20 == 0:
                    
                    x1, y1, x2, y2 = license_plate.xywh2xyxy(boxes[num_box])[0]
                    image_ocr=image_preview[y1:y2, x1:x2]
                    thread = threading.Thread(target=license_plate.test,args=([image_ocr]))
                    thread.start()
                    license_plate.save_to_csv(frame)

            if len(boxes) > 0:
                bbox = license_plate.xywh2xyxy(boxes[num_box])[0]
                image_preview = license_plate.pil2cv2(image_preview, license_plate.show_result, bbox)

            
        if license_plate.check == 0 :
            image_preview = license_plate.check_plate(input_tensor, frame)
        end_time = time.time()
        fps = 1 / np.round(end_time - start_time, 2)

        cv2.putText(image_preview, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        
        cv2.imshow('License Plate',image_preview)
        
        if cv2.waitKey(1) == ord('q'):
            break
    
vid.release()
cv2.destroyAllWindows()