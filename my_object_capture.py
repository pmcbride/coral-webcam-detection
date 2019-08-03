import argparse
import io
import time
import RPi.GPIO as IO
from edgetpu.detection.engine import DetectionEngine
from edgetpu.utils import dataset_utils
from imutils.video import VideoStream
from PIL import Image
import numpy as np
import imutils
import cv2


parser = argparse.ArgumentParser()
parser.add_argument(
    '--model', help='File path of Tflite model.', required=True)
parser.add_argument('--label', help='File path of label file.', required=True)
parser.add_argument('--confidence', help='Minimum probability to filter weak detections.', type=float, default=0.3)
args = parser.parse_args()

labels = dataset_utils.ReadLabelFile(args.label)
model = DetectionEngine(args.model)

IO.cleanup()
IO.setmode(IO.BOARD)
IO.setup(40, IO.OUT)
IO.setup(38, IO.OUT)

with VideoStream(src=0).start() as vs:
#vs = VideoStream(src=0).start()
  time.sleep(2)

  # Loop over the frames from the video stream
  while True:
    found_person = False

    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 500 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    orig = frame.copy()

    # prepare the frame for classification by converting (1) it from
    # BGR to RGB channel ordering and then (2) from a NumPy array to
    # PIL image format
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)

    # make predictions on the input frame
    start = time.time()
    results = model.DetectWithImage(frame, threshold=args.confidence, keep_aspect_ratio=True, relative_coord=False)
    end = time.time()

    # ensure at least one result was found
    for r in results:
      # extract the bounding box and box and predicted class label
      box = r.bounding_box.flatten().astype("int")
      (startX, startY, endX, endY) = box
      label = labels[r.label_id]
      if label=="person":
        found_person = True

      # draw the bounding box and label on the image
      cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)
      y = startY - 15 if startY - 15 > 15 else startY + 15
      text = "{}: {:.2f}%".format(label, r.score * 100)
      cv2.putText(orig, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # show the output frame and wait for a key press
    cv2.imshow("Frame", orig)
    key = cv2.waitKey(1) & 0xFF

    if found_person==True:
      IO.output(40, 1)
      IO.output(38, 0)
    else:
      IO.output(40, 0)
      IO.output(38, 1)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
      break

  # do a bit of cleanup
  cv2.destroyAllWindows()
  vs.stop()
  IO.cleanup()
