import cv2
import mediapipe as mp
import glob, os
import json
import logging
import uuid
from . import utils


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def infer(key):
    try:
        url = utils.get_s3_presigned_url(key)
        cap = cv2.VideoCapture(url)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width  = int(cap.get(3))   # float `width`
        height = int(cap.get(4))  # float `height`
        name = str(uuid.uuid4()) + '.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        out = cv2.VideoWriter(name, fourcc, fps, (width, height))
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    break
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = pose.process(image)
                # Draw the pose annotation on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                out.write(image)
        cap.release()
        out.release()
        key = 'skeleton/' + name
        utils.upload_file(name, key)
        for f in glob.glob("./*.mp4"):
            os.remove(f)
        code = 200
        body = {"key": key}

    except Exception as e:
        code = 403
        body = {"msg": 'infer failed'}
        print(e)
        logging.error(e)
        return "Error"
    return {
        'statusCode': code,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,HEAD,OPTIONS,POST,PUT",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept, Authorization",
        },
        'body': json.dumps(body)
    }