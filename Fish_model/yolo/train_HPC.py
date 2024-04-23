import torch
import torch.backends
import torchvision.transforms as transforms
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torch.optim.lr_scheduler import StepLR
from dataset import Fish_dataset
from Model import yolo_fish
from Loss import YoloLoss
from utils import (
    non_max_suppression,
    mean_average_precision,
    intersection_over_union,
    cellboxes_to_boxes,
    get_bboxes,
    plot_image,
    save_checkpoint,
    load_checkpoint,
    train_step,
    test_step,
    eval_model,
)
import os

if os.name == 'nt':  # For Windows
    if os.getcwd().split("\\")[-1] != "Legeplads":
        os.chdir('../..')
else:  # For Unix and Linux
    if os.getcwd().split('/')[-1] != 'Legeplads':
        os.chdir('../..')


# Hyperparameters etc. 
LEARNING_RATE = 1e-6
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 32 # 64 in original paper but I don't have that much vram, grad accum?
WEIGHT_DECAY = 0.0005
MOMENTUM = 0.9
EPOCHS = 1000
NUM_WORKERS = 0
PIN_MEMORY = True
LOAD_MODEL = False
LOAD_MODEL_FILE = "../overfit.pth.tar"
LOAD_PRE_TRAIN_MODEL = False
LOAD_PRE_TRAIN_MODEL_FILE = "../pre_train.pth.tar"

#########################################################################
# Set seed for reproducibility
seed = 123
torch.manual_seed(seed)
#########################################################################
# Load Data
transform = transforms.Compose([transforms.Resize((448, 448)), transforms.ToTensor(),])

fish_data = Fish_dataset("Fish_model/yolo/train_file.csv",
    transform=transform,)

train_dataset, test_dataset = random_split(fish_data,[0.9,0.1],generator=torch.Generator().manual_seed(seed))

train_loader = DataLoader(
    dataset=train_dataset,
    batch_size=BATCH_SIZE,
    num_workers=NUM_WORKERS,
    pin_memory=PIN_MEMORY,
    shuffle=True,
    drop_last=True,
)

test_loader = DataLoader(
    dataset=test_dataset,
    batch_size=BATCH_SIZE,
    num_workers=NUM_WORKERS,
    pin_memory=PIN_MEMORY,
    shuffle=False,
    drop_last=False,
)
#########################################################################
# Model
model1 = yolo_fish(split_size=7, num_boxes=2, num_classes=1).to(DEVICE)
# optimizer = optim.SGD(model1.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY,momentum=MOMENTUM)
optimizer = optim.Adam(model1.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
scheduler = StepLR(optimizer, step_size = 100, gamma = 0.5)
loss_fn = YoloLoss()
#########################################################################
# Load Model
if LOAD_MODEL:
    checkpoint = torch.load(LOAD_MODEL_FILE, map_location=torch.device(DEVICE))
    load_checkpoint(checkpoint, model1, optimizer)
elif LOAD_PRE_TRAIN_MODEL:
    checkpoint = torch.load(LOAD_PRE_TRAIN_MODEL_FILE, map_location=torch.device(DEVICE))
    load_checkpoint(checkpoint, model1, optimizer)

# ## Train/Test loop
seed = 123
torch.manual_seed(seed)
train_loss_all = []
test_loss_all = []
for epoch in (range(EPOCHS)):
    print(f"Epoch: {epoch}")
    # Train
    train_loss = train_step(model1,train_loader,loss_fn,optimizer,DEVICE)
    train_loss_all.append(train_loss)
    if epoch != 0 and epoch % 200 == 0:
        save_checkpoint(model=model1, optimizer=optimizer,scheduler=scheduler, filename=LOAD_MODEL_FILE)
    scheduler.step()
save_checkpoint(model=model1, optimizer=optimizer,scheduler=scheduler, filename=LOAD_MODEL_FILE)
