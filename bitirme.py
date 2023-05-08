import sys
import tkinter
import wave
import pyaudio
import tkinter.messagebox
import customtkinter
from tkcalendar import Calendar
from PIL import Image,ImageTk
import threading
import os
from datetime import datetime
import speech_recognition as sr
from transformers import pipeline
import numpy as np
from PIL import Image
from PIL import GifImagePlugin
import cv2
#from tensorflow.python.keras.engine import keras_tensor
from ActivityDetectionAlgorithm import Detection
from tkinter import messagebox as tmb
import multiprocessing



#google_key="112417540618206329954"
#google_mail = "kulak-ver@inbound-decker-385218.iam.gserviceaccount.com"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

recording_event = threading.Event()
activity_Detection_event = threading.Event()



class App(customtkinter.CTk):
    
    def __init__(self):
        
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', self.close_app)
        # configure window
        self.title("Kulak Ver")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Test", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.test_label = customtkinter.CTkLabel(self.sidebar_frame, text="Toplantı Özetleri", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.test_label.grid(row=1, column=0, padx=20, pady=(20, 10))
        #self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        #self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        #self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        #self.sidebar_button_2.grid(row=1, column=0, padx=20, pady=10)
        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame, width=250)
        self.textbox.grid(row=2, column=0, padx=(20, 0), pady=(10, 0), sticky="nsew")
        self.sidebar_button_create_avatar = customtkinter.CTkButton(self.sidebar_frame, text="Create Avatar", command=self.sidebar_button_event)
        self.sidebar_button_create_avatar.grid(row=3, column=0, pady=5)
        self.sidebar_button_edit_avatar = customtkinter.CTkButton(self.sidebar_frame, text="Edit Avatar", command=self.sidebar_button_event)
        self.sidebar_button_edit_avatar.grid(row=4,column=0, pady=10)
        self.sidebar_button_about = customtkinter.CTkButton(self.sidebar_frame, text="About", command=self.sidebar_button_event)
        self.sidebar_button_about.grid(row=5, column=0)
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame,text="")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.calendar = Calendar(self.sidebar_frame)
        self.calendar.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))

        # create main entry and button
        
        #self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        #self.picture1 = customtkinter.CTkImage(self.entry,Image.open(r"C:\Users\MonsterPC\Desktop\cv\1616751276754.jpg"))
        #self.photo_label = Label(image=ImageTk.PhotoImage(Image.fromarray(data)))
        #img = ImageTk.PhotoImage(Image.open(r"C:\Users\MonsterPC\Desktop\cv\1616751276754.jpg"))
        self.main_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.main_frame.grid(row=0, column=1, rowspan=5,columnspan=3, sticky="nsew")
        self.main_frame.grid_rowconfigure(5)
        self.main_frame.grid_columnconfigure(3)
        self.main_frame_label = customtkinter.CTkLabel(self.main_frame,text="")
        self.main_frame_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.main_frame_label2= customtkinter.CTkLabel(self.main_frame,text="")
        self.main_frame_label2.grid(row=2, column=0, padx=20, pady=(10, 0))
        img = customtkinter.CTkImage(light_image=Image.open(os.getcwd().replace("\\","/") + "/AvatarMaker.png"), size=(100, 100))
        self.picture_label=customtkinter.CTkLabel(self.main_frame,image=img,text="")
        self.picture_label.grid(row=3, column=1,padx=20, pady=(10, 10))
        self.picture_label2=customtkinter.CTkLabel(self.main_frame,image=img,text="")
        self.picture_label2.grid(row=3, column=2,padx=20, pady=(10, 10))
        self.picture_label3=customtkinter.CTkLabel(self.main_frame,image=img,text="")
        self.picture_label3.grid(row=3, column=3,padx=20, pady=(10, 10))
        self.main_frame_label3 = customtkinter.CTkLabel(self.main_frame,text="")
        self.main_frame_label3.grid(row=4, column=0, padx=20, pady=(10, 0))



        
        self.main_frame_button = customtkinter.CTkButton(self.main_frame, text="Dinle",command=button_callback)
        self.main_frame_button.grid(row=5, column=2)
        self.cam_button= customtkinter.CTkButton(self.main_frame,text="Kamera",command=kamera_callback)
        self.cam_button.grid(row=6,column=2)
       
       
        '''
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        '''
        # create textbox
        #self.textbox = customtkinter.CTkTextbox(self, width=250)
        #self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        '''
        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)
        
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)
        '''
        
        '''
        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")
        '''
        '''
        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 10), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_2.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        self.switch_1 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame, command=lambda: print("switch 1 toggle"))
        self.switch_1.grid(row=3, column=0, pady=10, padx=20, sticky="n")
        self.switch_2 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame)
        self.switch_2.grid(row=4, column=0, pady=(10, 20), padx=20, sticky="n")
        '''
        '''
        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="horizontal")
        self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")
        '''
        '''
        # set default values
        #self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.checkbox_2.configure(state="disabled")
        self.switch_2.configure(state="disabled")
        self.checkbox_1.select()
        self.switch_1.select()
        self.radio_button_3.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
#       self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("CTkOptionmenu")
        self.combobox_1.set("CTkComboBox")
        self.slider_1.configure(command=self.progressbar_2.set)
        self.slider_2.configure(command=self.progressbar_3.set)
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()
        '''
        #summaries = os.
        #self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        self.textbox.insert("0.0",str(os.listdir()))
        '''
        self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        self.seg_button_1.set("Value 2")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    '''

    def sidebar_button_event(self):
        print("sidebar_button click")
    def change_appearance_mode_event(self, new_appearance_mode: str): 
        customtkinter.set_appearance_mode(new_appearance_mode)

    def close_app(self):
        if tmb.askokcancel("Close", "Are you sure...?"):
            self.destroy()
            #process = multiprocessing.current_process()
            #process.kill()
            #activity_Detection_event.clear()
            #recording_event.clear()
            #t2.join()
            #t1.join()
            os._exit(os.EX_OK)

def init_file(FORMATIN, audio):
    wf = wave.open("/home/berk/Desktop/test.wav", "wb")
    # set the channels
    wf.setnchannels(1)
    # set the sample format
    wf.setsampwidth(audio.get_sample_size(FORMATIN))
    # set the sample rate
    wf.setframerate(44100)
    # write the frames as bytes
    return wf

def init_stream():
    '''
    FORMATIN = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    audio = pyaudio.PyAudio()


    info = audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    print("Devices ----------------------------------------------------------------------------")
   
    for i in range(audio.get_device_count()):
        print (audio.get_device_info_by_index(i))
    
    index = 0
    print(audio.get_device_info_by_index(index).get('maxOutputChannels'))
    # start Recording
    streamIn = audio.open(format=FORMATIN, channels=int(audio.get_device_info_by_index(index).get('maxOutputChannels')),
                            rate=int(audio.get_device_info_by_index(index).get('defaultSampleRate')), input=True,
                            input_device_index = index,
                            frames_per_buffer=CHUNK)


    return CHUNK, FORMATIN, audio, streamIn
    '''
    FORMATIN = pyaudio.paInt16
    CHANNELS = 2
    RATE = 24000
    CHUNK = 1024
    audio = pyaudio.PyAudio()

    #info = audio.get_host_api_info_by_index(0)
    #numdevices = info.get('deviceCount')
    #for i in range(0, numdevices):
    #        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
    #            if(audio.get_device_info_by_host_api_device_index(0, i).get('name')=='sof-hda-dsp'):
    #                index = audio.get_device_info_by_host_api_device_index(0, i).get('index')
                    #print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
                    #print(index)
    # start Recording
    index = 0
    audio.get_default_host_api_info()
    streamIn = audio.open(format=FORMATIN, channels=CHANNELS,
                          rate=RATE, input=True, output=False, output_device_index=index,
                          frames_per_buffer=CHUNK)
    return CHUNK, FORMATIN, audio, streamIn
    
def summarize(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length = 250, min_length = 30, do_sample=False)
    return summary

def save_text_and_summary(text):
    time = datetime.now()
    current_time = time.strftime("%H:%M:%S")
    # open text file
    #org_file_name='original_'+current_time+'.txt'
    text_file = open(str(os.getcwd())+'\\text.txt', "a")
    print(str(os.getcwd()))
    # write string to file
    text_file.write(text)

    # close file
    text_file.close()
    # open summary file
    #sum_file_name = 'summary_'+current_time+'.txt_'
    sumary_file = open(str(os.getcwd())+'\\ozet.txt',"a")
    # Summarize text
    summary_text = summarize(text)
    #Save summarized text
    for summary_part in summary_text:
        sumary_file.write(str(summary_part['summary_text']))
        sumary_file.write("\n")

    #Close summary file
    sumary_file.close()   

 # Speech Recognition Object
    #bucket_name = 'bucket_test'
    #source_file_name = filepath + audio_file_name
    #destination_blob_name = audio_file_name
    


def convert_to_text():
    
    recognizer = sr.Recognizer()
    # Reading the recorded .wav file (audio file)
    data = sr.AudioFile('/home/berk/Desktop/test.wav')
    chunk_duration = 60
    text_data = ""
    text_data_list = []
    with data as source:
        audio_length = source.DURATION
        print("Audio Length: " + str(audio_length))
        audio_length = int(audio_length)
        miss_part=audio_length % 60
        partition = audio_length/60
        #audio_length = int(audio_length+mis_parts)
        for chunk_start in range(0, int(partition)):
            print(str(chunk_start*60)+"->"+str(chunk_start*60+chunk_duration))
            audio = recognizer.record(source,offset=chunk_start*60, duration=chunk_duration)
            json = recognizer.recognize_google(audio, language='en-IN', show_all=True)
            print("-----------print ama for-----------")
            if (len(json)):
                save_text_and_summary(json['alternative'][0].get('transcript'))
                #text_data_list.append(json['alternative'][0].get('transcript'))
                #print("-------for içindeki if")
                text_data = text_data + json['alternative'][0].get('transcript')
                #print(text_data)
                
        audio=recognizer.record(source,offset=audio_length-miss_part,duration=int(miss_part))
        json = recognizer.recognize_google(audio, language='en-IN', show_all=True)
        if (len(json)):
                text_data_list.append(json['alternative'][0].get('transcript'))
                text_data = text_data + json['alternative'][0].get('transcript')
                print(json)
        #print(text_data_list)
    #return json['alternative'][0].get('transcript')
    
    return text_data
    '''
    audio_file= open("test.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript.text)
    return transcript.text
    '''
    

def record():
    CHUNK, FORMATIN, audio, streamIn = init_stream()

    print("recording...")

    wf = init_file(FORMATIN, audio)
    data = b''
    while recording_event.is_set():
        data = streamIn.read(CHUNK)
        wf.writeframes(data)

    close_recording(audio, streamIn, wf)
    ret_val = convert_to_text()
    #print(json)
    #save_text_and_summary(ret_val)
    sys.exit()

def close_recording(audio, streamIn, wf):
    # close & terminate the stream and audio
    streamIn.stop_stream()
    streamIn.close()
    audio.terminate()
    # close the file
    wf.close()





#-----------------kamera---------------------




#--------------------kamera----------------

def button_callback():
    if not recording_event.is_set():
        recording_event.set()
        #main_frame_button._text="Durdur"
        t1 = threading.Thread(target=record, args=())

        t1.start()
    else:
        recording_event.clear()
        

def kamera_callback():
    if not activity_Detection_event.is_set():
        activity_Detection_event.set()
        Detection.detection_event.set()
        t2 = threading.Thread(target=Detection.DetectActivities,args=())
        t2.start()
    else:
        activity_Detection_event.clear()
        Detection.detection_event.clear()
        

    
if __name__ == "__main__":
    app = App()
    app.mainloop()