#!/usr/bin/env python3

# Robot Vision Inference Script
import cv2
import numpy as np
import time
from ultralytics import YOLO
import argparse

def main():
    parser = argparse.ArgumentParser(description='Run object detection on a USB camera feed.')
    parser.add_argument('--model', type=str, default='yolov8n.pt', 
                        help='Path to the YOLOv8 model weights')
    parser.add_argument('--conf', type=float, default=0.25, 
                        help='Confidence threshold for detections')
    parser.add_argument('--camera', type=int, default=0, 
                        help='Camera index (usually 0 for built-in, 1 for USB)')
    args = parser.parse_args()
    
    # Load the model
    try:
        model = YOLO(args.model)
        print(f"Loaded model from {args.model}")
    except Exception as e:
        print(f"Error loading model: {e}")
        return
    
    # Open the camera
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print(f"Error: Could not open camera at index {args.camera}")
        print("Try a different camera index using the --camera argument")
        return
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("Camera opened successfully. Press 'q' to exit.")
    
    # Variables for FPS calculation
    fps = 0
    frame_count = 0
    start_time = time.time()
    
    while True:
        # Read a frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break
            
        # Increment frame counter
        frame_count += 1
        
        # Perform inference
        results = model(frame, conf=args.conf)
        
        # Process results
        annotated_frame = results[0].plot()
        
        # Calculate FPS
        elapsed_time = time.time() - start_time
        if elapsed_time >= 1.0:
            fps = frame_count / elapsed_time
            frame_count = 0
            start_time = time.time()
            
        cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display results
        cv2.imshow('Industrial Robot Vision', annotated_frame)
        
        # Check for exit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
