import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os, glob, sys
from animation import Animation
from PIL import Image
from natsort import natsorted

format = [".jpeg", ".jpg", ".tif", ".tiff", ".png"]
Image.MAX_IMAGE_PIXELS = None



##### フォルダ入力 #####
def open_dir():
    iDir = os.path.abspath(os.path.dirname(__file__))
    #input_dir = filedialog.askdirectory(initialdir = iDir)
    input_dir = filedialog.askopenfilename(initialdir = iDir)
    if len(input_dir) > 0:
        input_dir=os.path.dirname(input_dir)
        filelist = os.listdir(input_dir)
        if not any([os.path.splitext(file)[1].lower() in format for file in filelist]):
            warnwindow = messagebox.showwarning("warning", "No image found!")
            anime_open_button["state"] = "disable"
            preview_button["state"] = "disable"
        else:
            input_box.configure(state = "normal")
            input_box.delete(0, tk.END)
            input_box.insert(0, input_dir)
            input_box.configure(state = "readonly")
            anime_open_button["state"] = "normal"
            preview_button["state"] = "normal"
            x, y, z = show_data_info(input_dir)

            original_X.set(x)
            original_Y.set(y)
            original_Z.set(z)
            resize_abs_X.set(x)
            resize_abs_Y.set(y)
            resize_abs_Z.set(z)
            resize_rel_X.set(1.00)
            resize_rel_Y.set(1.00)
            resize_rel_Z.set(1.00)
            chain["state"] = "normal"


    else:
        input_box.configure(state = "normal")
        input_box.delete(0, tk.END)
        input_box.insert(0, input_dir)
        input_box.configure(state = "readonly")
        anime_open_button["state"] = "disable"
        preview_button["state"] = "disable"
        initial_data_info.set("")
        original_X.set("")
        original_Y.set("")
        original_Z.set("")
        chain["state"] = "disable"


def show_data_info(path):
    validextension = ("*.jpeg", "*.jpg", "*.tif", "*.tiff", "*.png", "*.bmp")
    filelist = []
    for ext in validextension:
            filelist.extend(glob.glob(str(path) + "/" + str(ext)))
    filelist = natsorted(filelist)
    filelist[0]
    im = Image.open(filelist[0])
    width, height = im.size
    nfiles = len(filelist)
    data_info_text = "1st Image: " + str(width) + "x" + str(height) + ", " + str(im.mode) + ", " + str(im.format) + ", " + str(nfiles) + " images"
    initial_data_info.set(data_info_text)

    return width, height, nfiles



##### アニメーションGUI #####
def generate_animation():
    input_dir = input_box.get()
    width, height, nfiles = show_data_info(input_dir)
    filelist = os.listdir(input_dir)
    # 入力フォルダ内に画像が存在しない場合
    if not any([os.path.splitext(file)[1].lower() in format for file in filelist]):
        warnwindow = messagebox.showwarning("warning", "No image found!")
        input_box.delete(0, tk.END)
        anime_open_button["state"] = "disable"
        preview_button["state"] = "disable"
    # 入力フォルダ内に画像が存在する場合，アニメーション作成ウインドウの立ち上げ
    else:
        # アニメーション作成ウインドウ
        ######################animewindow = tk.Toplevel(root)
        animewindow = tk.Toplevel()
        animewindow.title("animation")
        animewindow.grab_set()
        animewindow.focus_set()
        animewindow.geometry("+500+500")

        # 入力順（ファイル名or日時順）
        sort_area = tk.Label(animewindow, text = "sort: ")
        sort_area.grid(row = 0, column = 0, sticky = tk.W, rowspan = 2 )
        sort_radio_value = tk.IntVar(value = 1)
        sort_radio_value1 = ttk.Radiobutton(animewindow, text = "filename", variable = sort_radio_value, value = 1)
        sort_radio_value1.grid(row = 0, column = 1, sticky = tk.W)
        sort_radio_value1 = ttk.Radiobutton(animewindow, text = "timestamp", variable = sort_radio_value, value = 2)
        sort_radio_value1.grid(row = 1, column = 1, sticky = tk.W)

        # fps(speed)
        fps_area = tk.Label(animewindow, text = "speed(fps): ")
        fps_area.grid(row = 2, column = 0, sticky = tk.W)
        fps_spinbox = tk.StringVar()
        fps_spinbox.set(15)
        fps_sp = ttk.Spinbox(animewindow, textvariable= fps_spinbox, from_=1, to=50, width=5)
        fps_sp.grid(row = 2, column = 1, columnspan = 2, sticky = tk.W)

        # size
        size_area = tk.Label(animewindow, text = "size: ")
        size_area.grid(row = 3, column = 0, sticky = tk.W)
        size_input_frame = tk.Frame(animewindow)
        size_input_frame.grid(row = 3, column = 1, columnspan = 3, sticky = tk.W + tk.E )
        size_input_box_X = tk.Entry(size_input_frame, width = 5)# , validate= "key")#, validatecommand=(check_generate_animation,"%P"))
        size_input_box_X.grid(row = 0, column = 0, sticky = tk.W)
        size_text = tk.Label(size_input_frame, text = "x")
        size_text.grid(row = 0, column = 1, sticky = tk.W)
        size_input_box_Y = tk.Entry(size_input_frame, width = 5) #, validate= "key")#, validatecommand=(check_generate_animation,"%P"))
        size_input_box_Y.grid(row = 0, column = 2, sticky = tk.W)
        def animationsize_setoriginal():
            size_input_box_X.delete(0, tk.END)
            size_input_box_X.insert(tk.END, width)
            size_input_box_Y.delete(0, tk.END)
            size_input_box_Y.insert(tk.END, height)
        def animationsize_set4K():
            size_input_box_X.delete(0, tk.END)
            size_input_box_X.insert(tk.END, "4344")
            size_input_box_Y.delete(0, tk.END)
            size_input_box_Y.insert(tk.END, "2896")
        size_shortcut_button_setoriginal = tk.Button(size_input_frame, text = "original", command = animationsize_setoriginal)
        size_shortcut_button_setoriginal.grid(row = 0, column = 3)
        size_shortcut_button_set4K = tk.Button(size_input_frame, text = "4344x2896", command = animationsize_set4K)
        size_shortcut_button_set4K.grid(row = 0, column = 4)

        # ナンバリング
        numbering_area = tk.Label(animewindow, text = "numbering: ")
        numbering_area.grid(row = 4, column = 0, sticky = tk.W)
        numbering_frame = tk.Frame(animewindow)
        numbering_frame.grid(row = 4, column = 1, columnspan = 3, sticky = tk.W + tk.E )
        numbering_input_box = tk.Entry(numbering_frame, width = 20)
        numbering_input_box.grid(row = 0, column = 0, sticky = tk.W)
        if nfiles >= 9999:
            digits = "_00001"
        else:
            digits = "_0001"
        numbering_area2 = tk.Label(numbering_frame, text = str(digits))
        numbering_area2.grid(row = 0, column = 1, sticky = tk.W)
        # 実行ボタン
        def start_generate_animation():
            try:
                size_x = int(size_input_box_X.get())
            except ValueError:
                warnwindow = messagebox.showwarning("warning", "Size should be integer more than 0!", parent=animewindow)
            else:
                try:
                    size_y = int(size_input_box_Y.get())
                except ValueError:
                    warnwindow = messagebox.showwarning("warning", "Size should be integer more than 0!", parent=animewindow)
                else:
                    if (size_x > 0) and (size_y > 0):
                        typ = [("Movie", "*.mov")]
                        save_animation_path = filedialog.asksaveasfilename(filetypes = typ, defaultextension = "mov", parent=animewindow)
                        if save_animation_path == "":
                            pass
                        else:
                            #print(save_animation_path)
                            execute = Animation()
                            execute.inputdir = input_dir
                            if sort_radio_value.get() == 1:
                                execute.timesort = False
                            else:
                                execute.timesort = True
                            execute.fps = 15
                            execute.size_X = size_x
                            execute.size_Y = size_y
                            execute.numbering = numbering_input_box.get()
                            execute.output = save_animation_path
                            if os.path.exists(execute.output) is True:
                                os.remove(execute.output)

                            execute.Generate_Animation()
                    else:
                        warnwindow = messagebox.showwarning("warning", "Size should be integer more than 0!", parent=animewindow)

        start_animation_button = tk.Button(animewindow, text = "generate", command = start_generate_animation)
        #start_animation_button = tk.Button(animewindow, text = "generate", command = execute)
        start_animation_button.grid(row = 5, column = 0, columnspan = 4, sticky = tk.W + tk.E, padx = 5, pady = 10)
        animewindow.mainloop()

# メインウインドウの作成
root = tk.Tk()
root.title("YETI (YET another ImageJ)")
root.resizable(width=False, height=False)
root.geometry("+500+500")
icon_path = os.path.dirname(os.path.abspath(sys.argv[0])) + r'\icon.ico'
root.iconbitmap(default=icon_path)

##### ラベルフレーム（フォルダ入力）#####
input_frame = ttk.Labelframe(root, text = "Input folder", padding = 10)
input_frame.pack(side = tk.TOP, anchor = tk.W)
# フォルダパス表示欄
input_box = tk.Entry(input_frame, width = 50, state='readonly')
input_box.pack(side = tk.TOP, anchor = tk.W, fill = tk.X)
# フォルダを開くボタン
input_open_button = tk.Button(input_frame, text = "Open", command = open_dir)
input_open_button.pack(side = tk.TOP, anchor = tk.E, fill = tk.NONE, expand = 0)
# 画像情報表示枠
original_X = tk.IntVar()
original_Y = tk.IntVar()
original_Z = tk.IntVar()
original_X.set("")
original_Y.set("")
original_Z.set("")
initial_data_info = tk.StringVar()
initial_data = tk.Label(input_frame, textvariable = initial_data_info)
initial_data.pack(side = tk.TOP, anchor = tk.W)
# 画像表示ボタン
preview_button = tk.Button(input_frame, text = "Preview", state = "disable") #, command = run_func)
preview_button.pack(side = tk.TOP, fill = tk.X)
# アニメーション機能開始ボタン
anime_open_button = tk.Button(input_frame, text = "Generate animation", command = generate_animation, state = "disable")
anime_open_button.pack(side = tk.TOP, fill = tk.X)

##### 処理GUI #####
process_frame =ttk.Notebook(root)
process_frame.pack(side = tk.TOP, anchor = tk.W, fill = tk.X, padx = 5)
# タブの作成
resize_frame = tk.Frame(process_frame)
trim_frame = tk.Frame(process_frame)
reslice_frame = tk.Frame(process_frame)
convert_frame = tk.Frame(process_frame)
bits_frame = tk.Frame(process_frame)
# タブを追加
process_frame.add(resize_frame, text="resize")
process_frame.add(trim_frame, text="trim")
process_frame.add(reslice_frame, text="reslice")
process_frame.add(convert_frame, text="convert")
process_frame.add(bits_frame, text="bits")

# 各タブ（処理）のGUI
original_text = tk.StringVar()
# resize オリジナルデータ
resize_original_frame = ttk.LabelFrame(resize_frame, text = "original (pixel)")#, padding = 10)
resize_original_frame.pack(side = tk.TOP, anchor = tk.W)
original = tk.Entry(resize_original_frame, width = 5, state='readonly', textvariable=original_X)
original.pack(side = tk.LEFT, anchor = tk.CENTER, fill = tk.X, expand = 1)
x = tk.Label(resize_original_frame, text = "x")
x.pack(side = tk.LEFT,anchor = tk.W)
original = tk.Entry(resize_original_frame, width = 5, state='readonly', textvariable=original_Y)
original.pack(side = tk.LEFT, anchor = tk.CENTER, fill = tk.X, expand = 1)
x = tk.Label(resize_original_frame, text = "x")
x.pack(side = tk.LEFT,anchor = tk.W)
original = tk.Entry(resize_original_frame, width = 5, state='readonly', textvariable=original_Z)
original.pack(side = tk.LEFT, anchor = tk.CENTER, fill = tk.X, expand = 1)
# resize 入力値
def resize_param():
    try:
        resize_abs_X.set(round(resize_rel_X.get() * original_X.get()))
    except:
        messagebox.showerror("Value error", "Relative value should be double")
    try:
        resize_abs_Y.set(round(resize_rel_Y.get() * original_Y.get()))
    except:
        messagebox.showerror("Value error", "Relative value should be double")
    try:
        resize_abs_Z.set(round(resize_rel_Z.get() * original_Z.get()))
    except:
        messagebox.showerror("Value error", "Relative value should be double")

resize_abs_X = tk.IntVar()
resize_abs_Y = tk.IntVar()
resize_abs_Z = tk.IntVar()
resize_rel_X = tk.DoubleVar()
resize_rel_Y = tk.DoubleVar()
resize_rel_Z = tk.DoubleVar()
resize_abs_X.set("")
resize_abs_Y.set("")
resize_abs_Z.set("")
resize_rel_X.set("")
resize_rel_Y.set("")
resize_rel_Z.set("")
resize_input_frame = ttk.LabelFrame(resize_frame, text = "resize to")
resize_input_frame.pack(side = tk.LEFT, anchor = tk.W)
data_info = tk.StringVar()
resize_pixel_frame = ttk.Frame(resize_input_frame)
resize_pixel_frame.pack(side = tk.LEFT)
resize_text = tk.Label(resize_pixel_frame, text = "pixel")
resize_text.pack(side = tk.TOP,anchor = tk.W)
resize_pixel = tk.Entry(resize_pixel_frame, width = 5, textvariable=resize_abs_X)
resize_pixel.pack(side = tk.LEFT,anchor = tk.W)
resize_pixel = tk.Label(resize_pixel_frame, text = "x")
resize_pixel.pack(side = tk.LEFT,anchor = tk.W)
resize_pixel = tk.Entry(resize_pixel_frame, width = 5, textvariable=resize_abs_Y)
resize_pixel.pack(side = tk.LEFT,anchor = tk.W)
resize_pixel = tk.Label(resize_pixel_frame, text = "x")
resize_pixel.pack(side = tk.LEFT,anchor = tk.W)
resize_pixel = tk.Entry(resize_pixel_frame, width = 5, textvariable=resize_abs_Z)
resize_pixel.pack(side = tk.LEFT,anchor = tk.W)

resize_chain_frame = ttk.Frame(resize_input_frame)
resize_chain_frame.pack(side = tk.LEFT)
chain = tk.Button(resize_chain_frame, text = "<--", command = resize_param)
chain["state"] = "disable"
chain.pack(side = tk.LEFT)

resize_percent_frame = ttk.Frame(resize_input_frame)
resize_percent_frame.pack(side = tk.LEFT)
resize_text = tk.Label(resize_percent_frame, text = "relative(0-1)")
resize_text.pack(side = tk.TOP,anchor = tk.W)
resize_percent = tk.Entry(resize_percent_frame, width = 5, textvariable=resize_rel_X)
resize_percent.pack(side = tk.LEFT,anchor = tk.W)
resize_percent = tk.Label(resize_percent_frame, text = "x")
resize_percent.pack(side = tk.LEFT,anchor = tk.W)
resize_percent = tk.Entry(resize_percent_frame, width = 5, textvariable=resize_rel_Y)
resize_percent.pack(side = tk.LEFT,anchor = tk.W)
resize_percent = tk.Label(resize_percent_frame, text = "x")
resize_percent.pack(side = tk.LEFT,anchor = tk.W)
resize_percent = tk.Entry(resize_percent_frame, width = 5, textvariable=resize_rel_Z)
resize_percent.pack(side = tk.LEFT,anchor = tk.W)


# ウインドウ状態の維持
root.mainloop()

