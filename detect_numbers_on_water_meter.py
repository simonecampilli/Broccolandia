import torch
from ultralytics import YOLO
def sort_tensor_by_x1(data, cls):
    # Ordina il tensor in base alla colonna 0 (che rappresenta x1)
    sorted_data, indices = torch.sort(data[:, 0], dim=0)

    # Applica lo stesso ordinamento al tensor cls
    sorted_cls = cls[indices]

    return sorted_cls
def detect_numbers(img):
    model = YOLO('best.pt')
    image_path = img

    result_obj_det = model(image_path)

    boxes = None
    for result in result_obj_det:
        boxes = result.boxes  # Boxes object for bounding box outputs

        #result.show()  # display to screen
    if boxes!=None:
        numbers=sort_tensor_by_x1(boxes.data,boxes.cls)
        return numbers
    else:
        return "ErrorImage"
print(detect_numbers('images/id_1017_value_151_374_jpg.rf.7f391250fd08a5749ec4651849c7d512.jpg'))