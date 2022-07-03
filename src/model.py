import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import os
import shutil
import numpy as np

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()

        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

    def save(self, score, optimiser):
        file_name = f'{score}.pth'
        model_folder_path = '../models'

        state = {
            'state_dict': self.state_dict(),
            'optimiser': optimiser.state_dict()
        }

        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        try:
            models = os.listdir(model_folder_path)
            models = [int(x[:-4]) for x in models]

            if score >= max(models):
                shutil.rmtree(model_folder_path)
                os.makedirs(model_folder_path)
                file_name = os.path.join(model_folder_path, file_name)
                torch.save(state, file_name)
        except:
            file_name = os.path.join(model_folder_path, file_name)
            torch.save(state, file_name)


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimiser = optim.Adam(model.parameters(), lr=lr)

        # load model if it is saved
        model_file_path = '../models'
        models = os.listdir(model_file_path)
        if models:
            self.optimiser.load_state_dict(torch.load(
                os.path.join(model_file_path, models[0]), map_location=device)['optimiser'])

        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, game_over):
        state = torch.tensor(np.array(state), dtype=torch.float)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float)
        action = torch.tensor(np.array(action), dtype=torch.float)
        reward = torch.tensor(np.array(reward), dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            game_over = (game_over, )

        state = state.to(device)
        next_state = next_state.to(device)
        pred = self.model(state)

        target = pred.clone()
        for i in range(len(game_over)):
            Q_new = reward[i]
            if not game_over[i]:
                Q_new = reward[i] + self.gamma * \
                    torch.max(self.model(next_state[i]))
            target[i][torch.argmax(action).item()] = Q_new

        target = target.to(device)

        self.optimiser.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimiser.step()
