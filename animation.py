import glob, os, subprocess, sys
from natsort import natsorted
from PIL import Image
import time
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import signal

Image.MAX_IMAGE_PIXELS = None

class Animation:
    def __init__(self):
        self.inputdir = ""
        self.fps = 0
        self.size_X = ""
        self.size_Y = ""
        self.numbering = ""
        self.output = ""
        self.filelist = []
        self.validextension = ("*.jpeg", "*.jpg", "*.tif", "*.tiff", "*.png", "*.bmp")
        self.timesort = False
        self.font = "C\\\:/Windows/Fonts/times.ttf"

    def Filelist_Animation(self):
        self.filelist = []
        for ext in self.validextension:
            self.filelist.extend(glob.glob(str(self.inputdir) + "/" + str(ext)))
        if self.timesort == False:
            self.filelist = natsorted(self.filelist)
        elif self.timesort == True:
            self.filelist.sort(key=os.path.getctime)
        initial_image = self.filelist[0]
        nfiles = len(self.filelist)
        logname = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        path_current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        if os.path.exists(str(path_current_dir) + r"\logs"):
            pass
        else:
            os.mkdir(str(path_current_dir) + r"\logs")
        ssmtemp = str(path_current_dir) + r"\logs\animation" + str(logname) + ".txt"

        if os.path.isfile(ssmtemp): # delete previous ssmstemp.txt
            os.remove(ssmtemp)
        ssmtemplist = []
        for i in range(len(self.filelist)):
            self.filelist[i] = (self.filelist[i]).replace("/", os.sep)
            ssmtemplist.append("file " + "'" + str(self.filelist[i]) + "'")
        with open(ssmtemp, mode='w') as file:
            file.write('\n'.join(ssmtemplist))
        return(ssmtemp, initial_image, nfiles)

    def Caption_Animation(self, imagepath, nfiles):
        im = Image.open(imagepath)
        width, height = im.size
        NMB_XPOS = round(width * 0.005755)
        NMB_YPOS = round(height * 0.974102)
        NMB_SIZE = round(width * 0.01151)
        zeros = len(str(nfiles))
        if zeros <= 4:
            zeros = 4
        numberingcaption = " -vf \"drawtext=fontfile=" + str(self.font) + ": text=\'" + str(self.numbering) +"_"+ "%{eif\:n+1\:d\:" + str(zeros)+ "}\': r=25: x=" + str(NMB_XPOS) + ": y=" + str(NMB_YPOS) + ": fontsize=" + str(NMB_SIZE) + ": fontcolor=white: box=1: boxcolor=0x00000099\""
        return(numberingcaption)

    def Generate_Animation(self):
        """
        def subprocess_args(include_stdout=True):
            # The following is true only on Windows.
            if hasattr(subprocess, 'STARTUPINFO'):
                info = subprocess.STARTUPINFO()
                info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                env = os.environ
            else:
                info = None
                env = None

            if include_stdout:
                return {'stdout': subprocess.PIPE,
                        'stdin': subprocess.PIPE,
                        'stderr': subprocess.PIPE,
                        'startupinfo': info,
                        'env': env }
            else:
                return {'stdin': subprocess.PIPE,
                        'stderr': subprocess.PIPE,
                        'startupinfo': info,
                        'env': env}
        """
        ssmtemp, initial_image, nfiles = Animation.Filelist_Animation(self)
        ffmpeg_concat_path = "\"" + str(ssmtemp) + "\""
        ffmpeg_concat_path = (ffmpeg_concat_path).replace("/", os.sep)
        if len(str(self.numbering)) > 0:
            caption = Animation.Caption_Animation(self, initial_image, nfiles)
        else:
            caption = ""
        command = 'ffmpeg -f concat -r 15 -safe 0 '\
        + ' -i '  + str(ffmpeg_concat_path) + ' -r ' + str(self.fps)\
        + ' -s ' + str(self.size_X) + 'x' + str(self.size_Y)\
        + ' -an -pix_fmt yuv420p -vcodec mjpeg -b:v 600000000000000'\
        + str(caption)\
        + ' "' + str(self.output) + '"'

        with open(ssmtemp, mode='a') as file:
                file.write('\n'+"#"+str(command))



        ####ffmpegのログをコマンドプロンプト上に出力する場合は以下を使う．
        #p =subprocess.Popen("start "+str(command), **subprocess_args(True), shell=True)

        progress = tk.Toplevel()
        progress.geometry("750x350+500+500")
        progress.title("processing...")
        progress.grab_set()
        progress.focus_set()
        text = tk.Label(progress, text = "Now generating animation!")
        text.pack(side = tk.TOP,anchor = tk.W)
        text2 = tk.Label(progress, text = "Please wait...")
        text2.pack(side = tk.TOP,anchor = tk.W)
        bar = ttk.Progressbar(progress,mode='indeterminate')
        bar.pack(side = tk.TOP, fill = tk.X)
        cancel_button = tk.Button(progress, text = "cancel")
        cancel_button.pack(side = tk.TOP,anchor = tk.W)
        data_info = tk.StringVar()
        info = tk.Text(progress)
        info.bind("<Key>", lambda e: ctrlEvent(e))
        scrollbar = tk.Scrollbar(progress, orient=tk.VERTICAL, command=info.yview)
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        info["yscrollcommand"] = scrollbar.set
        info.pack(side = tk.TOP, anchor = tk.W, fill = tk.BOTH)

        bar.start()

        def ctrlEvent(event):
            if(event.state & 2**2 == 4 and event.keysym=='c' ):
                return
            else:
                return "break"



        def progre():

            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True,universal_newlines=True)#, preexec_fn=os.setsid)

            def cancel_animation():
                os.kill(p.pid, signal.CTRL_C_EVENT)
                cancel_button.configure(state = "disabled")
                for line in p.stdout:
                    try:
                        info.insert(tk.END, line)
                        info.see("end")
                    except KeyboardInterrupt:
                        pass
                progress.protocol("WM_DELETE_WINDOW", "")
                outputlog = info.get("1.0", "end")
                with open(ssmtemp, mode='a') as file:
                    file.write('\n'+ '\n'+ "JOB CANCELLED"+'\n')

            cancel_button.configure(command = cancel_animation)

            def click_close_to_cancel():
                if messagebox.askokcancel("Close window", "Animation will not be saved. Are you sure?", parent=progress):
                    cancel_animation()
                    progress.protocol("WM_DELETE_WINDOW", "")
                    outputlog = info.get("1.0", "end")
                    progress.update()
                    progress.destroy()

            progress.protocol("WM_DELETE_WINDOW", click_close_to_cancel)

            for line in p.stdout:
                #####data_info.set(line)
                info.insert(tk.END, line)
                info.see("end")

            try:
                #print("before")
                outs, errs = p.communicate()
                #print("after")
            except subprocess.TimeoutExpired:
                pass
            else:
                p.terminate()
                #print('done')
                if cancel_button['state'] == "disabled":
                    text["text"] = "Abort!"
                    text2["text"] = "Cancel button pushed. No animation file saved."
                else:
                    text["text"] = "Done!"
                    text2["text"] = "Animation saved as: " + str(self.output)
                    cancel_button.configure(state = "disabled")
                bar.stop()
                progress.protocol("WM_DELETE_WINDOW", "")
                outputlog = info.get("1.0", "end")
                with open(ssmtemp, mode='a') as file:
                    file.write('\n'+ outputlog+'\n')




        th1 = threading.Thread(target=progre)
        th1.start()
