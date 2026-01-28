from ultralytics import YOLO

# Initialize model
model = YOLO("yoloe-26x-seg.pt")  # or select yoloe-26s/m-seg.pt for different sizes

# Set text prompt to detect person and bus. You only need to do this once after you load the model.
names = ["bus"]
model.set_classes(names, model.get_text_pe(names))

# Run detection on the given image
results = model.predict("E:\8th Sem\code Smart Traffic Management System for Urban Congestion\Smart-Traffic-Management-System-\yolo\image.jpg")

# Show results
results[0].show()