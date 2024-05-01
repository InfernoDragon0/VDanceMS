from ultralytics import YOLO
from roboflow import Roboflow


if __name__ == '__main__':
    rf = Roboflow(api_key="apikey")

    project = rf.workspace("ms-xprmw").project("vdance")
    version = project.version(6)
    dataset = version.download("yolov8")
    # Load a model
    model = YOLO('yolov8m.pt')  # load a pretrained model (recommended for training)

    # Use the model
    results = model.train(data=f'{dataset.location}/data.yaml', epochs=20)  # train the model
    results = model.export(format='onnx')  # export the model to ONNX format
