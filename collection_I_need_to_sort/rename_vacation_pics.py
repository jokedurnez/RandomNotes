# in the current directory, there are 3 folders: for each camera one folder
# I will:
# 1) loop over those folders
# 2) loop over all pictres
# 3) extract the date the picture was taken
# 4) correct for a different timezone in each camera
# 5) give the file a logical date/time name: Guatemala_YYMMDD_HHMMSS_suffix.jpg
#    with suffix indicating the camera with which the picture was taken

#the different folders (camera's) have different time offsets
timechange = {
    "Guatemalala":-2,
    "Guatemalala_Anne":-1,
    "Guatemalala_Anne_onderwater":-3
    }

#we still want to have a suffix indicating who took the picture
suffix = {
    "Guatemalala":"JD",
    "Guatemalala_Anne":"AB",
    "Guatemalala_Anne_onderwater":"OW"
    }


for folder in timechange.keys():
    curdir = os.path.join(os.getcwd(),folder)
    for idx,file in enumerate(os.listdir(curdir)):
        # skipping over a few erroneous files
        if file in ["Guatemala_372.15",'.DS_Store','Icon\r']:
            continue
        # skipping over movies
        if ".MOV" in file:
            continue
        # current name (with path)
        filename = os.path.join(curdir,file)
        # extract time of creating
        filecreate = Image.open(filename)._getexif()[36867]
        filedate = datetime.datetime.strptime(filecreate,"%Y:%m:%d %H:%M:%S")
        # change date according to camera's timezone
        timedelta = datetime.timedelta(0,0,0,0,0,timechange[folder],0)
        newdate = filedate+timedelta
        # new name (with path)
        newname = datetime.datetime.strftime(newdate,"Guatemala_%y%m%d_%H%M%S")
        newname = os.path.join(curdir,newname+"_%s.jpg"%suffix[folder])
        # rename
        os.rename(filename,newname)
