# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A demo to classify Raspberry Pi camera stream."""

import argparse
import io
import time

from edgetpu.classification.engine import ClassificationEngine
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
args = parser.parse_args()

labels = dataset_utils.ReadLabelFile(args.label)
model = ClassificationEngine(args.model)


vs = VideoStream(src=0).start()
time.sleep(2)
while True:
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
  results = model.ClassifyWithImage(frame, top_k=1)
  end = time.time()

  # ensure at least one result was found
  if len(results) > 0:
    # draw the predicted class label, probability, and inference
    # time on the output frame
    (classID, score) = results[0]
    text = "{}: {:.2f}% ({:.4f} sec)".format(labels[classID], score * 100, end - start)
    cv2.putText(orig, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # show the output frame and wait for a key press
    cv2.imshow("Frame", orig)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
      break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
