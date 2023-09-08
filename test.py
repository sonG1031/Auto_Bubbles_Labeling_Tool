from roboflow import Roboflow
rf = Roboflow(api_key="onmlowwu2Z6sNNupWM5Z")
project = rf.workspace().project("webtoon-bubble-detection")
model = project.version(8).model

# infer on a local image
print(type(model.predict("test2.PNG", confidence=40, overlap=30).json()))