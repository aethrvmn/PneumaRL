import random
import torch

from numpy.random import default_rng

#from rl.brain import PPONet
from rl.brain import ActorNetwork, CriticNetwork, PPOMemory
class Agent:
    def __init__(self, n_actions, input_dims, gamma = 0.99, alpha = 0.0003, policy_clip = 0.2, batch_size = 64, N=2048, n_epochs = 10, gae_lambda = 0.95):
    
        self.gamma = gamma
        self.policy_clip = policy_clip
        self.n_epochs = n_epochs
        self.gae_lambda = gae_lambda
        
        print("Preparing Actor model...")
        self.actor = ActorNetwork(input_dims, n_actions, alpha)
        print(f"Actor network activated using {self.actor.device}")
        print("\nPreparing Critic model...")
        self.critic = CriticNetwork(input_dims, alpha)
        print(f"Critic network activated using {self.critic.device}")
        self.memory = PPOMemory(batch_size)
        
    def remember(self, state, action, probs, vals, reward, done):
        self.memory.store_memory(state, action, probs, vals, reward, done)
        
    def save_models(self):
        print('... saving models ...')
        self.actor.save_checkpoint()
        self.critic.save_chaeckpoint()
        print('... done ...')
        
    def load_models(self):
        print('... loadng models ...')
        self.actor.load_checkpoint()
        self.critic.load_chaeckpoint() 
        print('.. done ...')
    
    def choose_action(self, observation):
        state = T.tensor([observation], dtype = T.float).to(self.actor.device)
        
        dist = self.actor(state)
        value = self.critic(state)
        action = dist.sample()
        
        probs = T.squeeze(dist.log_prob(action)).item()
        action = T.squeeze(action).item()
        value = T.squeeze(value).item()
        
        return action, probs, value
        
    def learn(self):
        for _ in range(self.n_epochs):
            state_arr, action_arr, old_probs_arr, vals_arr, reward_arr, done_arr, batches = self.memory.generate_batches()
            
            values = vals_arr
            advantage = np.zeros(len(reward_arr), dtype = np.float32)
            
            for t in range(len(reward_arr)-1):
                discount = 1
                a_t = 0
                for k in range(t, len(reward_arr)-1):
                    a_t += discount*(reward_arr[k] + self.gamma*values[k+1]*(1-int(dones_arr[k])) - values[k])
                    discount *= self.gamma * self.gae_lambda
                advantage[t] = a_t
            advantage = T.tensor(Advantage).to(self.actor.device)
            
            values = T.tensor(values).to(self.actor.device)
            for batch in batches:
                states = T.tensor(state_arr[batch], dtype = T.float).to(self.actor.device)
                old_probs = T.tensor(old_probs_arr[batch]).to(self.actor.device)
                actions = T.tensor(action_arr[batch]).to(self.actor.device)
                
                dist = self.actor(states)
                critic_value = self.critic(states)
                
                critic_value = T.squeeze(critic_value)
                
                new_probs = dist.log_prob(actions)
                prob_ratio = new_probs.exp() / old_probs.exp()
                weighted_probs = advantage[batch] * prob_ratio
                weighted_clipped_probs = T.clamp(prob_ratio, 1-self.policy_clip, 1+self.policy_clip)*advantage[batch]
                actor_loss = -T.min(weighted_probs, weighted_clipped_probs).mean()
                
                returns = advantage[batch] + values[batch]
                critic_loss = (returns - critic_value)**2
                critic_loss = critic_loss.mean()
                
                total_loss = actor_loss + 0.5*critic_loss
                
                self.actor.optimizer.zero_grad()
                self.critic.optimizer.zero_grad()
                total_loss.backward()
                self.actor.optimizer.step()
                self.critic.optimizer.step()
                
        self.memory.clear_memory()
                
        
  #  def __init__(self, actions, inputs, player_info, reward, save_dir, checkpoint = None):
 #       self.inputs = inputs
#
 #       self.input_dim = len(inputs) + len(player_info)
#
#        self.output_dim = len(actions)
        
       # self.reward = reward
      #  
     #   if torch.cuda.is_available():
    #        self.device = "cuda"
   #     elif torch.backends.mps.is_available():
  #          self.device = "mps"
 #       else:
#            self.device="cpu"
            
       # self.net = PPONet(self.input_dim, self.output_dim)
      #  self.net = self.net.to(device=self.device)
     #   
    #    self.rng = default_rng()
   #     
  #      
 #       ## DEFINING PARAMETERS
#        pass
                
                
        #print(f"Model ready, using {self.device}")
       # if checkpoint:
      #      print(f"chkpt at {checkpoint}")
     #       self.load(checkpoint)
    #    else:
   #         print('No chkpt passed')
  #          
 #   def act(self, distance_direction_to_player):
#       print(distance_direction_to_player)
