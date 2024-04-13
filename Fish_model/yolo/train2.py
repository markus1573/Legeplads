
import torch
import torch.backends
import torchvision.transforms as transforms
import torch.optim as optim
import torchvision.transforms.functional as FT
from torch.utils.data import DataLoader
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

# ## Hyperparameters

seed = 123
torch.manual_seed(seed)

# Hyperparameters etc. 
LEARNING_RATE = 2e-5
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 16 # 64 in original paper but I don't have that much vram, grad accum?
WEIGHT_DECAY = 0
EPOCHS = 1000
NUM_WORKERS = 0
PIN_MEMORY = True
LOAD_MODEL = False
LOAD_MODEL_FILE = "/Users/markus/Documents/Legeplads/Fish_model/yolo/overfit.pth.tar"

# ## Dataset & Dataloader

class Compose(object):
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, img, bboxes):
        for t in self.transforms:
            img, bboxes = t(img), bboxes

        return img, bboxes

transform = Compose([transforms.Resize((448, 448)), transforms.ToTensor(),])
def main():
    train_dataset = Fish_dataset(
        "/Users/markus/Documents/Legeplads/Fish_model/yolo/train_file.csv",
        transform=transform,
    )

    test_dataset = Fish_dataset(
        "/Users/markus/Documents/Legeplads/Fish_model/yolo/test_file.csv", transform=transform,
    )

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
        shuffle=True,
        drop_last=True,
    )

    # ## Model

    model1 = yolo_fish(split_size=7, num_boxes=2, num_classes=1).to(DEVICE)
    optimizer = optim.Adam(
        model1.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY
    )
    loss_fn = YoloLoss()

    if LOAD_MODEL:
        load_checkpoint(torch.load(LOAD_MODEL_FILE), model1, optimizer)

    # ## Train/Test loop

    train_loss_all = []
    test_loss_all = []
    for epoch in (range(EPOCHS)):
        print(f"Epoch: {epoch}/{EPOCHS}")
        # Train
        train_loss = train_step(model1,train_loader,loss_fn,optimizer,DEVICE)
        train_loss_all.append(train_loss)

        # # Test
        # test_loss = test_step(model1,test_loader,loss_fn,DEVICE)
        # test_loss_all.append(test_loss)

        pred_boxes, target_boxes = get_bboxes(train_loader, 
                                            model1, 
                                            iou_threshold=0.5, 
                                            threshold=0.4,device=DEVICE
            )

        mean_avg_prec = mean_average_precision(pred_boxes, 
                                            target_boxes, 
                                            iou_threshold=0.5, 
                                            box_format="midpoint"
            )
        print(f"Train mAP: {mean_avg_prec}")


        if mean_avg_prec > 0.999:
            checkpoint = {
                "state_dict": model1.state_dict(),
                "optimizer": optimizer.state_dict(),
            }
            save_checkpoint(checkpoint, filename=LOAD_MODEL_FILE)
            import sys
            sys.exit()

    # ## eval model

    # model1_stats = eval_model(model1,test_loader,loss_fn)

    # model1_stats

if __name__ == "__main__":
    main()



