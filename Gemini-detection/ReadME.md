Whole Project Summary

Goal: Real-time AI waste detection using webcam + Gemini AI.

Webcam Feed: Captured using OpenCV (cv2.VideoCapture) + flipped + resized for smooth display.

AI Classification:
Frame saved as temporary image.
Gemini AI receives image + prompt → returns JSON (waste info).
Parsed safely, displayed on video.

Threading: AI calls run in background → video never freezes.

Overlay: Title + AI result text on live video.

Delay Control: Limit AI calls every 15 sec → prevent API quota overuse.

Error Handling: Handles AI/API exceptions gracefully.

Output: Smooth, real-time, mirror-view webcam feed with waste classification text overlayed.

✅ Extra Notes:

Categories are flexible → AI can detect new types.

No square boxes → clean minimal display.

Safe threading + global variable lock ensures stable real-time performance.