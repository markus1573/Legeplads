
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch.optim as optim
import torch.nn.functional as F

# Set device
if torch.cuda.is_available():
    device = torch.device('cuda')
elif torch.backends.mps.is_built():
    device = torch.device('mps')
else:
    device = torch.device('cpu')

print(f"Device: {device}")

# # linear regression model

start = -5
stop = 10
step = 0.1
N = int((stop-start)/step)

weigth = 1.8
bias = 27

X = torch.arange(start,stop,step,device=device).unsqueeze(dim=1)

Y = weigth * X + bias

split = int(N*0.8)

X_train = X[:split]
Y_train = Y[:split]

X_test = X[split:]
Y_test = Y[split:]


class LinearRegressionModelNew(nn.Module):
    def __init__(self,input_features, output_features):
        super().__init__()
        self.linear_layer = nn.Linear(input_features,output_features,device=device)
    
    def forward(self,X):
        return self.linear_layer(X)

learning_rate = 0.01
n_epochs = 1000
in_features = 1 # Antal weigts
out_features = 1 # Samme som antal weigts, da vi vil have et output pr. input
model1 = LinearRegressionModelNew(in_features,out_features)
optimizer = optim.SGD(model1.parameters(),lr=learning_rate)
loss_fn = nn.MSELoss()


# Tracking the model
epoch_count = []
loss_values = []
test_loss_values = []

# Training the model
for epoch in range(n_epochs):
    model1.train()
    #Calculate predictions
    Y_predicted = model1(X_train)
    #Calculate loss
    loss = loss_fn(Y_predicted,Y_train)
    #backprobagate
    loss.backward()
    #take step
    optimizer.step()
    #reset gradients
    optimizer.zero_grad()

    # Testing the model
    with torch.inference_mode():
        model1.eval()
        Y_pred1 = model1(X_test)
        test_loss = loss_fn(Y_pred1,Y_test)

    # print the loss
    if (epoch+1) % 100 == 0:
        print(f"Epoch {epoch+1}, loss is {loss.item()} | Test loss is {test_loss.item()}")

    # Store the loss value for plotting
    epoch_count.append(epoch+1)
    loss_values.append(loss.item())
    test_loss_values.append(test_loss.item())

# save model and tracking data
save_path = "model1.pt"
torch.save(model1.state_dict(),save_path)

train_stats = {
    "epoch_count":epoch_count,
    "loss_values":loss_values,
    "test_loss_values":test_loss_values
}

df = pd.DataFrame(train_stats)

with open("train_stats.csv","w") as file:
    df.to_csv(file)