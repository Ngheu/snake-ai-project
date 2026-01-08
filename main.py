import sys
from game import SnakeGame
from agent_logic import LogicAgent

try:
    from agent_cnn import train
except ImportError:
    train = None
    print("Warning: agent_cnn.py or train function not found.")

def main():
    print("--- SNAKE AI CONTROLLER ---")
    
    print("\nSelect Map:")
    print("1. Classic")
    print("2. Maze (Walls)")
    map_choice = input("Enter choice (1/2): ")
    
    map_name = "classic"
    if map_choice == "2":
        map_name = "maze"

    print("\nSelect Algorithm:")
    print("1. BFS")
    print("2. Greedy")
    print("3. Machine Learning (CNN)")
    
    algo_choice = input("Enter choice (1/2/3): ")

    if algo_choice == "3":
        if train:
            print(f"\nStarting Training on Map: {map_name}...")
            train(map_name) 
        else:
            print("Error: Machine Learning module not found.")
        return 

    algo_name = "bfs"
    if algo_choice == "2":
        algo_name = "greedy"

    game = SnakeGame(map_name=map_name)
    agent = LogicAgent(game)

    print(f"\nRunning Algorithm: {algo_name.upper()} on Map: {map_name.upper()}")
    print("Press window close button to exit.")

    while True:
        action = agent.get_action(algo_type=algo_name)
        reward, done, score = game.play_step(action)
        
        if done:
            game.reset()
            print(f"Game Over! Score: {score}. Restarting...")

if __name__ == '__main__':
    main()