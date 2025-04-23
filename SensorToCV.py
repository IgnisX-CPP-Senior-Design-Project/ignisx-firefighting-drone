# The purpose of this script is to read the input sensor data from the flight controller 
# as it relates to and aligns with the computer vision models 

# online python script template 

from dronekit import connect 
from ultralytics import YOLO 
import cv2 
import time 


# === CONNECT TO PIXHAWK === 

print("Connecting to Pixhawk...") 

vehicle = connect('/dev/ttyAMA0', wait_ready=True, baud=57600)  # Adjust for your port 
 
#  /dev/ttyAMA0 is the serial port of the RPi used to talk to external hardware I.e. pixhawk  
# where data flows from the pixhawk to the Pi 
# Baud rate is the communication speed over the serial connection 
# 57600 (standard telemetry 1 port) 
# 115200 (faster, used in some USB configs) 

# == Check Telemtry and connection == 
print(vehicle.location.global_frame)

print(vehicle.airspeed)
  
  
# === LOAD YOLOv8 MODEL === 

model = YOLO("yolov8n.pt")  # or yolov8n.onnx if using ONNX inference 

  
# === SET UP CAMERA === 

cap = cv2.VideoCapture(0)  # Change index if needed 


# === MAIN LOOP === 

try: 

    while True: 

        # === READ SENSOR DATA FROM PIXHAWK === 

        altitude = vehicle.location.global_relative_frame.alt 

        gps = vehicle.location.global_frame 

        heading = vehicle.heading 

        airspeed = vehicle.airspeed 

  
        print(f"Altitude: {altitude:.2f}m | GPS: {gps.lat:.6f}, {gps.lon:.6f} | Heading: {heading}") 

  
        # === CAPTURE FRAME FROM CAMERA === 

        ret, frame = cap.read() 

        if not ret: 

            print("Failed to grab frame") 

            continue 

# ret stands for “return value” (a boolean). tells you whether the camera successfully grabbed a # frame. I.e. true or false  


        # === RUN YOLOv8 DETECTION === 

        results = model(frame) 
        annotated_frame = results[0].plot() 

        # === ADD SENSOR OVERLAY === 

        cv2.putText(annotated_frame, f"Alt: {altitude:.1f}m", (10, 25), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2) 

        cv2.putText(annotated_frame, f"GPS: {gps.lat:.4f}, {gps.lon:.4f}", (10, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2) 


        # === SHOW FRAME === 

        cv2.imshow("Drone Vision", annotated_frame) 

        if cv2.waitKey(1) & 0xFF == ord('q'): 

            break 

  
except KeyboardInterrupt: 

    print("Shutting down...") 

  
finally: 

    cap.release() 
    cv2.destroyAllWindows() 
    vehicle.close() 