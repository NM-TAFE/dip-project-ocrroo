import cv2
import pytesseract
import json
from tqdm import tqdm
from fuzzywuzzy import fuzz

# Specify the Tesseract executable path if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\bishi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def frame_difference(frame1, frame2, threshold_value):
    """
    Extracts text from a given frame using Tesseract OCR.

    Parameters:
    frame (np.array): The frame to extract text from.
    tesseract_cmd (str): The path to the Tesseract executable.

    Returns:
    str: The extracted text.
    """
    diff = cv2.absdiff(frame1, frame2)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, binary_diff = cv2.threshold(gray_diff, threshold_value, 255, cv2.THRESH_BINARY)
    return cv2.sumElems(binary_diff)[0]


def extract_text(frame):
    """
    Extracts text from a given frame using Tesseract OCR.

    Parameters:
    frame (np.array): The frame to extract text from.

    Returns:
    str: The extracted text.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text.strip()


def find_segments(video_path, frame_diff_threshold, threshold_value):
    """ 
    Find segments in a video where the frame difference exceeds a threshold.
    
    Parameters:
    video_path (str): The path to the video file.
    frame_diff_threshold (int): The frame difference threshold.
    threshold_value (int): The threshold value for binary thresholding.

    Returns:
    list: A list of segments.
    """
    video = cv2.VideoCapture(video_path)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_skip = int(fps / 2)  # Process two frames per second
    segments = []

    last_frame = None
    segment_start = 0

    # Use tqdm to create a progress bar
    for frame_num in tqdm(range(0, frame_count, frame_skip), desc="Processing video frames"):
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = video.read()
        if not ret:
            break

        if last_frame is not None:
            diff = frame_difference(last_frame, frame, threshold_value)
            if diff > frame_diff_threshold:
                # Segment ends here
                segments.append({
                    "start_frame": segment_start,
                    "end_frame": frame_num - frame_skip,
                    "start_time": segment_start / fps,
                    "end_time": (frame_num - frame_skip) / fps,
                    "text_present": False,
                    "extracted_text": ""
                })
                segment_start = frame_num

        last_frame = frame

    # Handle last segment
    segments.append({
        "start_frame": segment_start,
        "end_frame": frame_count - 1,
        "start_time": segment_start / fps,
        "end_time": (frame_count - 1) / fps,
        "text_present": False,
        "extracted_text": ""
    })

    video.release()

    return segments


def extract_text_from_segments(video_path, segments):
    """ 
    Extract text from the frames at the start of each segment in a video.
     
    Parameters:
    video_path (str): The path to the video file.
    segments (list): A list of segments.

    Returns:
    list: The list of segments with the extracted text.
     
     """
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_skip = int(fps / 2)  # Process two frames per second

    for segment in segments:
        video.set(cv2.CAP_PROP_POS_FRAMES, segment["start_frame"])
        ret, frame = video.read()
        if not ret:
            continue

        extracted_text = extract_text(frame)
        text_present = len(extracted_text) > 0

        segment["text_present"] = text_present
        segment["extracted_text"] = extracted_text if text_present else ""

    video.release()

    return segments


def save_segments_to_json(segments, output_path):
    """
    Do final segmentation then save a list of segments to a JSON file.

    Parameters:
    segments (list): A list of segments.
    output_path (str): The path to the output JSON file.
    """
    i = 0
    # Combine segments that are close to each other
    while i < len(segments) - 1:
        current_segment = segments[i]
        next_segment = segments[i + 1]
        if current_segment["text_present"] and next_segment["text_present"]:
            # Check if CURRENT segment's text is in the NEXT segment
            ratio_full = fuzz.ratio(current_segment["extracted_text"], next_segment["extracted_text"])
            ratio_within = fuzz.ratio(next_segment["extracted_text"], current_segment["extracted_text"])  # Check reverse containment
            is_within = current_segment["extracted_text"] in next_segment["extracted_text"]

            if ratio_full >= 70 or ratio_within >= 80 or is_within: # Adjust thresholds if needed (decrease for more leniance)
                # Combine segments 
                current_segment["end_frame"] = next_segment["end_frame"]
                current_segment["end_time"] = next_segment["end_time"]
                current_segment["extracted_text"] = next_segment["extracted_text"]  # Take the complete text
                del segments[i + 1]
            else:
                i += 1
        else:
            i += 1

    with open(output_path, 'w') as f:
        json.dump(segments, f, indent=4)

# Example usage
video_path = "C:/Users/bishi/OneDrive/Desktop/test2 - 1716891852652.mp4"
output_json_path = 'text_segments3.json'
difference_threshold = 100  # Increase for less sensitivity in text detection
frame_diff_threshold = 2000  # Increase for less sensitivity in frame differencing
threshold_value = 100  # Increasing makes it less sensitive to frame differences

segments = find_segments(video_path, frame_diff_threshold, threshold_value)
extract_text_from_segments(video_path, segments)
save_segments_to_json(segments, output_json_path)

print(f"Text segments have been saved to {output_json_path}")