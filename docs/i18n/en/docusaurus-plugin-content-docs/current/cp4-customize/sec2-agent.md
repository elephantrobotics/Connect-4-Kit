---
sidebar_position: 2
---

# Optimization of the Game Model

The official gaming model is based on a DQN[^2] network trained with PyTorch[^1] and exported in the ONNX[^3] format for usage.

However, you can also train your own gaming model using any framework you prefer. The model file must be exported in the ONNX format.

The model takes a matrix-shaped chessboard state as input and outputs decision values for 6 positions. The position with the highest decision value will be selected as the next chess move for the robotic arm.

[^1]: PyTorch is an open-source machine learning framework primarily used for building deep neural network models. It provides a rich set of tools and libraries for various machine learning tasks, including computer vision, natural language processing, image and speech recognition, etc. PyTorch adopts a dynamic graph computation approach, making model construction and debugging more flexible and intuitive.

[^2]: DQN is a reinforcement learning algorithm, which stands for Deep Q-Network. It combines deep neural networks and Q-learning algorithm to solve reinforcement learning problems. DQN has made significant breakthroughs in the field of reinforcement learning, particularly in tasks with high-dimensional state spaces, such as gameplay in games.

[^3]: ONNX (Open Neural Network Exchange) is an open-source cross-platform machine learning model interchange format. It allows users to seamlessly migrate models between different deep learning frameworks. ONNX can export deep learning models as independent files, enabling the deployment and execution of models on different frameworks (such as PyTorch, TensorFlow, etc.) or hardware platforms, thereby improving model portability and flexibility.
