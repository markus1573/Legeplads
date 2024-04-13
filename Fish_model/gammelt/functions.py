import torch
import torch.backends
from torchmetrics import Accuracy, ConfusionMatrix
from tqdm.auto import tqdm


device = torch.device("mps" if torch.backends.mps.is_built() else "cpu")


def train_step(model,train_loader,loss_fn,optimizer,device=device):
    train_loss = 0
    model.train()
    for batch,(X_train,y_train) in enumerate(train_loader):
        X_train = X_train.to(device)
        y_train = y_train.to(device)
        y_logits = model(X_train).squeeze()
        loss = loss_fn(y_logits,y_train)
        train_loss += loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    train_loss /= len(train_loader)

    # Print out what is happening
    print(f"Train loss: {train_loss:.4f}")
    return train_loss



def test_step(model,test_loader,loss_fn,device=device):
    test_loss = 0
    model.eval()
    with torch.inference_mode():
        for X_test, y_test in test_loader:
            X_test = X_test.to(device)
            y_test = y_test.to(device)
            # forward pass
            test_pred = model(X_test).squeeze()
            # calculate loss accumulating
            test_loss += loss_fn(test_pred,y_test)
        
        # calculate the average loss per batch
        test_loss /= len(test_loader)
        # test_loss_all.append(test_loss.item())
        
        # Print out what is happening
        print(f"Test loss: {test_loss:.4f}")
        return test_loss
    

def eval_model(model, test_loader, loss_fn,
               show_confusion_matrix=True, show_accuracy=True):
    y_preds_total = []
    y_total = []
    with torch.inference_mode():
        for X, y in tqdm(test_loader):
            y_preds = torch.sigmoid(model.to("cpu")(X)).round().squeeze()
            y_preds_total.extend(y_preds.numpy())
            y_total.extend(y.to("cpu").numpy())
    y_preds_total = torch.tensor(y_preds_total)
    y_total = torch.tensor(y_total)
    loss = loss_fn.to("cpu")(y_preds_total,y_total)
    print(f"Loss: {loss:.4f}")
    acc = None
    if show_accuracy:
        acc = Accuracy(task="binary")(y_preds_total,y_total)
        print(f"Accuracy: {acc:.4f}")
    c_matrix = None
    if show_confusion_matrix:
        comfmat = ConfusionMatrix(task="binary",num_classes=2)
        c_matrix = comfmat(y_preds_total,y_total)
        print(f"Confusion matrix: \n{c_matrix}")
    return y_preds_total, y_total, {"Model Name":model.__class__.__name__,"loss":loss.item(),"accuracy":acc.item(),"confusion_matrix":c_matrix}