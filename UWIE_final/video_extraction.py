import cv2
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument('-v','--vid',help='add video file to extract, absolute path only')
parser.add_argument('-od','--out_dir',help='target dir',action='store_true',default='')
parser.add_argument('-id','--in_dir',help='input dir')
parser.add_argument('-ex','--ex',help='extract frames',action='store_true')
parser.add_argument('-mk','--mk',help='mk video',action='store_true')
args = parser.parse_args()


def extract(out,vid):
    vidcap = cv2.VideoCapture(str(vid))
    success,image = vidcap.read()
    count = 0
    while success:
      cv2.imwrite(out+"\\%d.jpg" % count, image)     # save frame as JPEG file
      success,image = vidcap.read()
      print('Read a new frame: ', success,count)
      count += 1

def mk_video(in_dir):
    from PIL import Image
    os.chdir(str(in_dir))
    path = str(in_dir)
    mean_height = 0
    mean_width = 0
    num_of_images = len(os.listdir('.'))
    #print(num_of_images)
    list_img = []
    for file in os.listdir(in_dir):
        list_img.append(file)
        im = Image.open(os.path.join(path, file))
        width, height = im.size
        mean_width += width
        mean_height += height
    mean_width = int(mean_width / num_of_images)
    mean_height = int(mean_height / num_of_images)

    for file in range(0,num_of_images):
        file = in_dir+'\\'+str(file)+'.jpg'
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"):
    		# opening image using PIL Image
            im = Image.open(os.path.join(path, file))

    		# im.size includes the height and width of image
            width, height = im.size
    		#print(width, height)

    		# resizing
            imResize = im.resize((mean_width, mean_height), Image.ANTIALIAS)
            imResize.save( file, 'JPEG', quality = 95) # setting quality
    		# printing each resized image name
            print(im.filename.split('\\')[-1], " is resized")


    # Video Generating function
    def generate_video(in_dir,num_of_images):
        image_folder = in_dir # make sure to use your folder
        video_name = 'mygeneratedvideo.avi'
        #os.chdir(in_dir)
        images = []
        for img in range(0,num_of_images):
            img = in_dir+'\\'+str(img)+'.jpg'
            images.append(img)
        frame = cv2.imread(os.path.join(image_folder, images[0]))

        height, width, layers = frame.shape

        video = cv2.VideoWriter(video_name, 0, 24, (width, height))

        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))

    	# Deallocating memories taken for window creation
        cv2.destroyAllWindows()
        video.release() # releasing the video generated


    # Calling the generate_video function
    generate_video(in_dir,num_of_images)




if args.out_dir=='':
    args.out_dir = 'frames'
try:
    os.system('mkdir '+args.out_dir)
except:
    pass
print(args.out_dir,args.vid)
if args.ex and args.vid:
    extract(args.out_dir,args.vid)
if args.mk and args.in_dir:
    mk_video(args.in_dir)
