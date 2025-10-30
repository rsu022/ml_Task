import cv2
import google.generativeai as genai
import threading
import tempfile
import json
import time

# Configure Gemini AI
API_KEY = ""  # Replace with your API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-001")

# Global variables
result_text = "Analyzing..."  # Text to display
lock = threading.Lock()  # Thread safety
delay = 5  # Seconds between AI calls
last_capture_time = 0  #tracks last capture time

# Function to analyze frame
def analyze_frame(frame):
    """
    Send frame to Gemini AI for waste classification.
    """
    global result_text
    try:
        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        cv2.imwrite(temp_file.name, frame)

        prompt = """
        You are an expert in waste material detection.
        Analyze the given image and respond in JSON:
        {
            "is_waste": true/false,
            "category": "Plastic/Paper/Food/Metal/Glass/Textiles/E-waste/Wood/Others",
            "decomposable": "Yes/No",
            "explanation": "Short reason"
        }
        Notes: Categories listed are examples. Detect new types if present.
        """

        response = model.generate_content(
            [prompt, {"mime_type": "image/jpeg", "data": open(temp_file.name, "rb").read()}]
        )

        try:
            output_json = json.loads(response.text)
            text = f"Waste: {output_json['is_waste']}, Category: {output_json['category']}, Decomposable: {output_json['decomposable']}"
        except:
            text = response.text

        with lock:
            result_text = text

    except Exception as e:
        with lock:
            result_text = f"Error: {e}"

# Open webcam

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access webcam.")
    exit()

print("🎥 Press 'q' to quit.")

#  Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture video frame.")
        break

    frame = cv2.flip(frame, 1)  # Mirror for user perspective
    frame = cv2.resize(frame, (640, 480))  # Smooth display

    # Run AI analysis in background thread
    current_time = time.time()
    if current_time - last_capture_time > delay:
        last_capture_time = current_time
        threading.Thread(target=analyze_frame, args=(frame.copy(),), daemon=True).start()

    # Overlay AI result text only (no boxes)
    cv2.putText(frame, "Gemini Waste Detector", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    with lock:
        y0 = 70
        for i, line in enumerate(result_text.split("\n")):
            y = y0 + i*30
            cv2.putText(frame, line, (10, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Show video
    cv2.imshow("Live Waste Classification", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
