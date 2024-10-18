import torch
import torch.nn as nn
import torch.optim as optim

# Define a simple neural network
class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(10, 50)
        self.fc2 = nn.Linear(50, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Create an instance of the network
model = SimpleNet()

# Define an optimizer (this is optional, but commonly saved in checkpoints)
optimizer = optim.SGD(model.parameters(), lr=0.001)

# Saving the model's state_dict (weights only) and the optimizer's state_dict
torch.save({
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'epoch': 10,  # You can track the training epoch
    'loss': 0.5,  # You can save the loss for logging purposes
}, 'model_checkpoint.pth')

print("Checkpoint saved successfully.")
