#!/usr/bin/python

import cv2, sys, getopt, json

def main(argv):
    inputfile = ''
    outputfile = ''
    action = 'box'
    try:
        opts, args = getopt.getopt(argv,"ha:i:o:",["action=","ifile=","ofile="])
    except getopt.GetoptError:
        print 'test.py [-a <action:box,cords>] -i <inputfile> [-o <outputfile>]'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'facedetect.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-a", "--action"):
            action = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    rects, img = detect(inputfile)

    if action == 'detect':
        print json.dumps(rects.tolist())
    else:
        print 'Detecting faces in:',inputfile
        print 'Boxing faces in:',outputfile
        box(rects, img, outputfile)

def detect(path):
    """ Detects faces and returns the x y locations and img resource
    """
    img = cv2.imread(path)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    return rects, img

def box(rects, img, outputfile):
    """ Draws boxes over the disovered detected area

    Note: mime types can change i.e. name can be png, jpg, different than the input file.
    GIF is not allowed
    """
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
    cv2.imwrite(outputfile, img)

if __name__ == "__main__":
    main(sys.argv[1:])