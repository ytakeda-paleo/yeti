import glob, os, sys, datetime
from natsort import natsorted
from PIL import Image
from concurrent import futures
from time import time

# USAGE
# from imageprocess import ImageProcess as im

# inputdir = r"C:\Users\hogehoge\t e"
# data1 = im(inputdir)
# print(data1.filelist) # if you want to see the filelist
# print(data1.nfiles) # if you want to see the number of files

# outputdir = r"C:\Users\hogehoge\dst2"

# data1.ConvertMultiImages(outputdir, "png") # You can skip "png"
# data1.TrimMultiImages(500,600,700,800,50,60,outputdir, "jpg") # You can skip "jpg"

# data1 = im(inputdir, ["*.png","*.tif"]) # If various file types are in the directory, you can limit the file type(s) to input


Image.MAX_IMAGE_PIXELS = None

class ImageProcess:
    def __init__(self, inputdir, extensionlist=None):
        # the very initial argument to be set
        # example: inputdir = r"C:\Users\hogehoge\"
        #          data1 = ImageProcess(inputdir)
        self.inputdir = inputdir

        # another argument(non-mandatory)
        self.validextension = ["*.jpeg", "*.jpg", "*.tif", "*.tiff", "*.png", "*.bmp"]
        if extensionlist is not None:
                self.validextension = extensionlist
        # others
        self.outputext = "tif"
        self.multiprocessing = True
        self.filelist = []
        self.nfiles = "Input file is not initialized! Something is wrong."
        self.outputdir = "Outputdir is not initialized! Something is wrong."

        # create filelist
        for ext in self.validextension:
            self.filelist.extend(glob.glob(str(self.inputdir) + "/" + str(ext)))
            self.filelist = natsorted(self.filelist)
        self.nfiles = len(self.filelist)


    def CheckOutputDir(self,outputdir):
    # example:  data1.OutputDirCheck(outputfolderpath)
    # This is not necessary to process
        self.outputdir = outputdir
        if os.path.isdir(self.outputdir) is True:
            print("Output images will be saved in existing directory "+str(self.outputdir))
        else:
            os.mkdir(self.outputdir)
            print("New directory "+str(self.outputdir)+" created.")


    def ExportLog(self,log):
    # This is should not be executed by user
        logname = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        path_current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        if os.path.exists(str(path_current_dir) + r"\logs"):
            pass
        else:
            os.mkdir(str(path_current_dir) + r"\logs")
        logpath = str(path_current_dir) + r"\logs\imageprocess" + str(logname) + ".txt"
        with open(logpath, mode='a') as file:
            file.write(log)





    def ConvertMultiImages(self, outputdir, outputext=None, multiprocessing=True):
    # example: data1.ConvertMultiImages(outputdirectory, ".png")
        ImageProcess.CheckOutputDir(self,outputdir)
        log = []
        log = "ImageProcess.ConvertMultiImages(outputdir="+str(self.outputdir)+", outputext="+str(self.outputext)+", multiprocessing="+str(self.multiprocessing)+")"
        outputfilelist = []
        for i in range(self.nfiles):
            saveas = str(self.outputdir)+"\\"+str(os.path.splitext(os.path.basename(self.filelist[i]))[0])+"."+str(outputext)
            outputfilelist.append(saveas)
        self.multiprocessing = multiprocessing

        if self.multiprocessing is False:
            for i in range(self.nfiles):
                output = ImageProcess.ConvertImage(self.filelist[i], outputfilelist[i])
                log = log + "\n" + str(self.filelist[i]) + " >> " + str(outputfilelist[i])
        else:
            with futures.ThreadPoolExecutor() as executor:
                for i in range(self.nfiles):
                    future = executor.submit(ImageProcess.ConvertImage,
                    self.filelist[i], outputfilelist[i])
                    log = log + "\n" + str(self.filelist[i]) + " >> " + str(outputfilelist[i])

        ImageProcess.ExportLog(self,log)

    def ConvertImage(inputfilepath, outputfilepath):
        im = Image.open(inputfilepath)
        im.save(outputfilepath)




    def TrimMultiImages(self, x1, y1, x2, y2, z1, z2, outputdir, outputext=None, multiprocessing=True, validextension=None):
    # example: Data1.TrimMultiImages(500,600,700,800,50,60,outputdir, "jpg")
            ImageProcess.CheckOutputDir(self,outputdir)
            log = []
            log = "ImageProcessTrimMultiImages(x1="+str(x1)+", y1="+str(y1)+", x2="+str(x2)+", y2="+str(y2)+", z1="+str(z1)+", z2="+str(z2)+", outputdir="+str(self.outputdir)+", outputext="+str(self.outputext)+", multiprocessing="+str(self.multiprocessing)+")"
            self.multiprocessing = multiprocessing
            outputfilelist = []
            for i in range(z1,z2+1):
                saveas = str(self.outputdir)+"\\"+str(os.path.splitext(os.path.basename(self.filelist[i]))[0])+"."+str(outputext)
                outputfilelist.append(saveas)

            if self.multiprocessing is False:
                for i in range(len(outputfilelist)):
                    ImageProcess.TrimImage(self.filelist[i], x1, y1, x2, y2, outputfilelist[i])
                    log = log + "\n" + str(self.filelist[i]) + " >> " + str(outputfilelist[i])
            else:
                with futures.ThreadPoolExecutor() as executor:
                    for i in range(len(outputfilelist)):
                        future = executor.submit(ImageProcess.TrimImage,
                        self.filelist[i], x1, y1, x2, y2, outputfilelist[i])
                        log = log + "\n" + str(self.filelist[i]) + " >> " + str(outputfilelist[i])

            ImageProcess.ExportLog(self,log)

    def TrimImage(inputfilepath, x1, y1, x2, y2, outputfilepath):
    #左上の座標が(x, y) = (left, upper)、
    #右下の座標が(x, y) = (right, lower)に対応する。
    #切り出されるのはleft <= x < rightかつupper <= y < lowerの領域で、
    #x = right, y = lowerのピクセルは含まれない。
        im = Image.open(inputfilepath)
        im_crop = im.crop((x1, y1, x2, y2))
        save_filename = os.path.splitext(os.path.basename(inputfilepath))[0]
        im_crop.save(outputfilepath)





