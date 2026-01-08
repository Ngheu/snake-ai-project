import torch
import random
import numpy as np
import os
from collections import deque
from game import SnakeGame
from model_cnn import ConvQNet
from helper import plot
import torch.optim as optim
import torch.nn as nn
from config import *

class CNNAgent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MEMORY_SIZE)
        self.model = ConvQNet(output_size=3)
        self.optimizer = optim.Adam(self.model.parameters(), lr=LR)
        self.criterion = nn.MSELoss()
        self.load_model()

    def load_model(self):
        folder_path = './model'
        file_path = os.path.join(folder_path, 'model_cnn.pth')
        if os.path.exists(file_path):
            print("--> Loaded existing model_cnn.pth")
            try:
                saved_state = torch.load(file_path)
                self.model.load_state_dict(saved_state)
                self.model.eval() 
                self.n_games = 100 
            except Exception as e:
                print(f"Error loading model: {e}")
        else:
            print("--> No existing model. Training from scratch.")

    def get_state(self, game):
        grid = game.get_grid_state()
        return np.expand_dims(grid, axis=0)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(np.array(state), dtype=torch.float)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 3:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        pred = self.model(state)
        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))
            target[idx][torch.argmax(action[idx]).item()] = Q_new
    
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.train_step(states, actions, rewards, next_states, dones)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state_t = torch.tensor(state, dtype=torch.float).unsqueeze(0)
            prediction = self.model(state_t)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

def train(map_name='classic'):
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = CNNAgent()
    
    game = SnakeGame(map_name=map_name)
    
    print(f"Starting CNN Training on map: {map_name}...")
    
    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        
        agent.train_step(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            if score > record:
                record = score
                agent.model.save()
                print(f"--> New Record! Model Saved.")

            print(f'Game {agent.n_games} Score {score} Record {record}')
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)