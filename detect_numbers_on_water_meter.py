import torch
from ultralytics import YOLO
import os
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

        result.show()  # display to screen
    if boxes!=None:
        numbers=sort_tensor_by_x1(boxes.data,boxes.cls)
        return numbers
    else:
        return "ErrorImage"
directory = 'testProva'

for image in os.listdir(directory):
    print(detect_numbers('testProva/'+image))


#image 1/1 C:\Users\simoc\PycharmProjects\Broccolandia\testProva\id_918_value_472_037_jpg.rf.b22118c14ec2a4e3c6f116b68a43c4fa.jpg: 256x320 3 0s, 1 2, 1 3, 1 4, 1 7, 67.2ms
#image 1/1 C:\Users\simoc\PycharmProjects\Broccolandia\testProva\id_832_value_276_214_jpg.rf.1a386606b7c22376d6ad6ad2ac467981.jpg: 256x320 2 0s, 1 1, 2 2s, 1 4, 1 6, 1 7, 104.9ms
#image 1/1 C:\Users\simoc\PycharmProjects\Broccolandia\testProva\id_831_value_98_827_jpg.rf.bd752c0d4b2927b791e5e39e60a42d94.jpg: 256x320 3 0s, 1 2, 1 7, 2 8s, 1 9, 67.5ms
#image 1/1 C:\Users\simoc\PycharmProjects\Broccolandia\testProva\id_828_value_173_877_jpg.rf.4be24a0ee66e55e7a988e1a3c111cf74.jpg: 256x320 2 0s, 1 1, 1 3, 3 7s, 1 8, 60.1ms
#image 1/1 C:\Users\simoc\PycharmProjects\Broccolandia\testProva\id_5_value_100_533_jpg.rf.631c7dd3b626b2798520343e7740996b.jpg: 256x320 4 0s, 1 1, 2 3s, 1 5, 46.0ms
#image 1/1 C:\Users\simoc\PycharmProjects\Broccolandia\testProva\id_438_value_293_369_jpg.rf.10551c933bde2e1d138aa44c4cf2bf46.jpg: 256x320 2 0s, 1 2, 2 3s, 1 6, 2 9s, 47.2ms
#image 1/1 C:\Users\simoc\PycharmProjects\Broccolandia\testProva\id_414_value_20_087_jpg.rf.5d6542abeb679e3abefff9322f397e05.jpg: 256x320 5 0s, 1 2, 1 7, 1 8, 47.3ms
