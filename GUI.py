# import the necessary packages
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog as tkFileDialog
import cv2
import os
def Huffman(compressed_path, filename, image):
    cv2.imwrite(compressed_path, image, [17,2])

def RLE(compressed_path, filename, image):
    # cv2.imwrite(compressed_path, image, [17,3])
    cv2.imwrite(compressed_path, image)
def LZW(compressed_path, filename, image):
    cv2.imwrite(compressed_path, image, [cv2.IMWRITE_TIFF_COMPRESSION])
    
def select_and_compress(encoding_method):
    # grab a reference to the image panels
    global panelA, panelB
    # open a file chooser dialog and allow the user to select an input image
    path = tkFileDialog.askopenfilename()
    # ensure a file path was selected
    if len(path) > 0:
        filename = path.split('/')[-1]
        # load the image from disk
        image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        compress_folder = "/".join(path.split('/')[:-1]) + "/compress/"

        if (encoding_method=='Huffman'):
            compressed_path = compress_folder+'Huffman_'+filename
            Huffman(compressed_path, filename, image)
        elif (encoding_method=="RLE"):
            compressed_path = compress_folder+'RLE_'+filename
            RLE(compressed_path, filename, image)
        elif (encoding_method=="LZW"):
            compressed_path = compress_folder+'LZW_'+filename
            RLE(compressed_path, filename, image)
        # Get size of original image
        size = os.stat(path).st_size // 1024
        compressed = cv2.imread(compressed_path, cv2.IMREAD_UNCHANGED)

        # Get size of compressed image
        compressed_size = os.stat(compressed_path).st_size // 1024
        # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        compressed = cv2.cvtColor(compressed, cv2.COLOR_BGR2RGB)
        # Rescale image to be small enough to fit in GUI
        if (image.shape[1]>=700 or image.shape[0]>=700):
            image = cv2.resize(image, (500, int(image.shape[0]*(500/image.shape[1]))))
            compressed = cv2.resize(compressed, (500, int(compressed.shape[0]*(500/compressed.shape[1]))))
        # convert the images to PIL format
        image = Image.fromarray(image)
        compressed = Image.fromarray(compressed)
        # ...and then to ImageTk format
        image = ImageTk.PhotoImage(image)
        compressed = ImageTk.PhotoImage(compressed) 
        # if the panels are None, initialize them
        if panelA is None or panelB is None:
            # the first panel will store our original image
            panelA = Label(image=image)
            panelA.image = image

            panelA.grid(row=4, column=0)
            labelA = Label(text='Original Image')
            labelA.grid(row=3, column=0)

            # while the second panel will store the edge map
            panelB = Label(image=compressed)
            panelB.image = compressed
            # panelB.pack(side="right", padx=10, pady=20)
            panelB.grid(row=4, column=1)
            # Display size of image
            sizeB = Label(text=str(compressed_size) + " KB")
            sizeB.grid(row=5, column=1)
            labelB = Label(text='Compressed Image')
            labelB.grid(row=3, column=1)
        # otherwise, update the image panels
        else:
            # update the pannels
            panelA.configure(image=image)
            panelB.configure(image=compressed)
            panelA.image = image
            panelB.image = compressed
        sizeA = Label(text=str(size) + " KB")
        sizeA.grid(row=5, column=0)
        sizeB = Label(text=str(compressed_size) + " KB")
        sizeB.grid(row=5, column=1)

# Make compress folder if not exists
if not os.path.exists('./compress'):
    os.makedirs('./compress')

# initialize the window toolkit along with the two image panels
root = Tk()
root.title('Lossless Image Compressor')

panelA = None
panelB = None

# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn1 = Button(root, text="Huffman Encoding", command = lambda: select_and_compress('Huffman'))
btn2 = Button(root, text="RLE Encoding", command = lambda: select_and_compress('RLE'))
btn3 = Button(root, text="LZW", command = lambda: select_and_compress('LZW'))

btn1.grid(row=0, sticky='w')
btn2.grid(row=1, sticky='w')
btn3.grid(row=2, sticky='w')
# kick off the GUI
root.mainloop()