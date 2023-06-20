import gym
import torch
import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple
from classes.ll_agent import Agent

model_path = "lunar_lander/models/ll_model_2.pt"

Transition = namedtuple('Transition', ('state', 'action', 'reward', 'next_state', 'terminated'))

env = gym.make('LunarLander-v2')

agent = Agent(state_size=env.observation_space.shape[0], action_size=env.action_space.n)

print("TRAINING PHASE")

rewards = []  
errors = []

for i_episode in range(2000):
    state = env.reset()
    episode_reward = 0  
    for t in range(2000):
        
        action = agent.policy.select_action(torch.tensor(state, dtype=torch.float), agent.epsilon)
        
        next_state, reward, done, _ = env.step(action)
        
        agent.memory.store(Transition(state, action, reward, next_state, done))
        
        loss = agent.train()
        
        state = next_state
        
        episode_reward += reward 
        errors.append(loss)  
                
        if done:
            rewards.append(episode_reward)
            print(f"Episode: {i_episode} finished after {t+1} timesteps, Loss: {loss:.2f}, Reward: {episode_reward:.2f}, Average reward: {np.mean(rewards[-100:]):.2f}")
            break
        
        agent.decay_epsilon()

    if len(rewards) >= 100 and np.mean(rewards[-100:]) >= 200:
        print("Average reward of last 100 episodes is 200 or more. Training stops.")
        break


torch.save(agent.policy.state_dict(), model_path)

plt.figure(figsize=(12, 5))

plt.subplot(121)
plt.plot(rewards)
plt.title("Average Reward per Episode")
plt.xlabel("Episode")
plt.ylabel("Average Reward")
plt.xlim(0, 2*len(rewards))  

plt.subplot(122)
plt.plot(errors)
plt.title("Error per Episode")
plt.xlabel("Episode")
plt.ylabel("Error")
plt.xlim(0, 2*len(errors))

plt.show()

print("TESTING PHASE")

agent = Agent(state_size=env.observation_space.shape[0], action_size=env.action_space.n)
agent.policy.load_state_dict(torch.load(model_path))

while True:
    for i_episode in range(10): 
        state = env.reset()
        for t in range(1000):
            env.render()
            action = agent.policy.select_action(torch.tensor(state, dtype=torch.float), 0)
            state, reward, done, _ = env.step(action)
            if done:
                print(f"Episode: {i_episode} finished after {t+1} timesteps, with a reward of: {reward:.2f}")
                break

    user_input = input("Do you want to run the testing phase again? (yes/no): ")
    if user_input.lower() != "yes":
        break

env.close()
