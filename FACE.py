import face_recognition
import cv2
import numpy as np
import os
import time
import pickle
# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.


"""获取文件列表"""
def getRawFileList(path):
    files, names= [],[]
    for f in os.listdir(path):
        if  f.endswith(".jpg") :      # 返回指定的文件夹包含的文件或文件夹的名字的列表
            files.append(os.path.join(path, f))     # 把目录和文件名合成一个路径
            names.append(f)
    return files, names
data_dir = "D:/face/jpg"
files,names = getRawFileList(data_dir)
known_face_encodings,known_face_names=[],[]
pickData={}
start_time = time.time()
pickDataPath = "pickData.dat"
if not os.path.exists(pickDataPath):
    for file in names:
        image = face_recognition.load_image_file(file)
        face_encoding = face_recognition.face_encodings(image, num_jitters=5)[0]
        known_face_encodings.append(face_encoding)
        face_name = file.replace('.jpg','')
        known_face_names.append(face_name)
        pickData[face_name] = face_encoding
    #持久化
    fw=open(pickDataPath,"wb")
    pickle.dump(pickData,fw)    
    fw.close()
else:
    fr=open(pickDataPath,"rb")
    pickData=pickle.loads(fr.read())
    for key,value in pickData.items():
        known_face_names.append(key)        
        known_face_encodings.append(value)
    fr.close()

end_time = time.time()  # 记录程序结束运行时间

print('Took %f second' % (end_time - start_time))

# Get a reference to webcam #0 (the default one)
#rtsp://[admin]:[admin123]@[10.15.6.23]:554/h264/ch1/sub/av_stream
#rtsp://[admin]:[admin123]@[10.15.6.23]:554/h264/ch1/main/av_stream
# video_capture = cv2.VideoCapture('rtsp://admin:admin123@10.15.12.67:554/h264/ch1/main/av_stream')
video_capture = cv2.VideoCapture(0)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    try:
        small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)
    except Exception:
        continue    

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time-----节省时间？
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.45)
            name = u"Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            if name != u"Unknown":
                name = name + " {:8.2f}".format(face_distances.min())    
                print(name)                      
            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 1
        right *= 1
        bottom *= 1
        left *= 1

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

1 editted on web  @2019-08-08 16:00
2 editted on web  @2019-08-08 16:09    
