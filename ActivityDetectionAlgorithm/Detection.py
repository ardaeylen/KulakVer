import cv2
import numpy as np
from threading import Thread
import time
import pyscreenshot as ImageGrab
import pyvirtualcam
import os
_class = "wave"
image = ImageGrab.grab()
image = np.array(image.convert("RGB"))
    
labels = ['wave', 'okey', 'think', 'thumb_down', 'thumb_up', 'sleepy', 'clap', 'head_scratching', 'laugh']
CONFIDENCE_THRESHOLD = 0.2  # Confidence Threshold
NMS_THRESHOLD = 0.8  # Non-Max Suppression Threshold
network_conf_file = os.getcwd().replace('\\','/') + '/ActivityDetectionAlgorithm/yolov4-bitirme.cfg'
network_weights = os.getcwd().replace('\\','/') + '/ActivityDetectionAlgorithm/yolov4-bitirme_last.weights'
print(network_conf_file)
idx_to_labels = {
        0: labels[0],
        1: labels[1],
        2: labels[2],
        3: labels[3],
        4: labels[4],
        5: labels[5],
        6: labels[6],
        7: labels[7],
        8: labels[8],
    }



def camera_thread_function():

    while True:
        global image

        image = ImageGrab.grab(childprocess=False)
     
        # ----------------
def detection_function(model, net, output_label_dictionary, CONFIDENCE_THRESHOLD, NMS_THRESHOLD):

    while (True):
        global image

        try:
            #image = buffer.get()
            img_np = np.array(image)
            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

            frame_width = frame.shape[1]
            frame_height = frame.shape[0]

            img_blob= cv2.dnn.blobFromImage(frame, 1 / 255, (640, 640), swapRB=True)
            net.setInput(img_blob)
            classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)

            if(len(classes)):
                
                global _class
                for _class in classes:
                    if _class or _class == 0:
                        _class = output_label_dictionary[int(_class)]
                        print(_class)
            else:
                        
                print("Nothing has detected.")
            

        except:
            print("Exception Occured On Detection.")




# Concurrency test-----------------------
def DetectActivities():
    global image
    net = cv2.dnn.readNet(network_conf_file, network_weights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

    model = cv2.dnn.DetectionModel(net)

    model.setInputParams(size=(640,640), scale=1 / 255.0, swapRB=True)

    #camera_thread_function(model=model)

    camera_thread = Thread(target=camera_thread_function, args=())
    detection_thread = Thread(target=detection_function, args=(model, net, idx_to_labels
                                                                ,CONFIDENCE_THRESHOLD,
                                                                NMS_THRESHOLD))
    init_cam_thread = Thread(target = init_cam, args = ())
    camera_thread.start()
    detection_thread.start()
    init_cam_thread.start()

def stream_animation(virtualCam, frames):
	for i in range(0, len(frames)):
		frame=frames[i]
		
		virtualCam.send(frame)
		virtualCam.sleep_until_next_frame()
	
def default_animation(virtualCam, frame):
	
	frame[:] = virtualCam.frames_sent % 255 
	virtualCam.send(frame)
	virtualCam.sleep_until_next_frame()
			
def extract_frames(videoPath, camera_width, camera_height):

	frames = []
	videoCaptureObject = cv2.VideoCapture(videoPath)
	

	ret = True
	while ret:
		ret, frame = videoCaptureObject.read()
		if ret:
			frames.append(frame)
			print("x")
	# Convert frames into desired sizes.
	frames = [cv2.resize(frame, (camera_width, camera_height), cv2.INTER_AREA) for frame in frames]
	return frames


def display_avatars(da_width, da_height, da_fps):
    with pyvirtualcam.Camera(width=da_width,height=da_height, fps=da_fps, device='/dev/video4') as cam:
        global _class
        default_animation_frames = extract_frames("sample", cam.width, cam.height)
        laugh_frames = extract_frames("sample2", cam.width, cam.height)
        print(f'Using virtual camera: {cam.device}')
        frame = np.zeros((cam.height, cam.width, 3), np.uint8)  # RGB
        i=0
        while True:
            # Take input from action recognition
            # parse input
            if (i%100 == 0):
                if _class == "wave":
                    stream_animation(cam, default_animation_frames)
                    
                else:
                    stream_animation(cam, laugh_frames)
                    
                
            default_animation(cam, frame)
            
            i=i+1

def init_cam():
    os.popen("sudo -S %s"%("sudo modprobe -r v4l2loopback && sudo modprobe v4l2loopback devices=1 video_nr=4 card_label=\"Virtual\" exclusive_caps=1 max_buffers=2"), 'w').write('1')
    #os.system("sudo modprobe -r v4l2loopback && sudo modprobe v4l2loopback devices=1 video_nr=4 card_label=\"Virtual\" exclusive_caps=1 max_buffers=2")
    display_avatars(1200, 700, 10)
