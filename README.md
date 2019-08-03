# coral-webcam-detection
Edge TPU real-time face detection and tracking on a Raspberry Pi with a Google Coral USB Accelerator and USB webcam

### Requirements:
1. Raspberry Pi 3 Model B+
2. Google Coral USB Accelerator
3. Arduino (optional: for GPIO output)

### References
I mostly followed the tutorial [here](https://www.pyimagesearch.com/2019/05/13/object-detection-and-image-classification-with-google-coral-usb-accelerator/) for the real-time face detection. I then modified the code to use the GPIO ports of the Raspberry Pi 3 Model B+ in order to send digital output signals to an Arduino Uno whenever a face moved to the edge of the webcam view. The Arduino used these signals to activate a stepper motor that rotates the webcam to follow the detected face.

References
1. https://www.pyimagesearch.com/2019/05/13/object-detection-and-image-classification-with-google-coral-usb-accelerator/
