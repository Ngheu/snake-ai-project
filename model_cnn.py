import torch
import torch.nn as nn
import torch.nn.functional as F
import os
from config import GRID_W, GRID_H

class ConvQNet(nn.Module):
    def __init__(self, output_size):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        
        self.feature_size = 32 * GRID_H * GRID_W 
        
        self.linear1 = nn.Linear(self.feature_size, 256)
        self.linear2 = nn.Linear(256, output_size)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = x.view(-1, self.feature_size) 
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model_cnn.pth'):
        folder = './model'
        if not os.path.exists(folder): os.makedirs(folder)
        path = os.path.join(folder, file_name)
        torch.save(self.state_dict(), path)