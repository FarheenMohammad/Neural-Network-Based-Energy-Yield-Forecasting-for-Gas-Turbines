The demand for efficient and consistent production of energy has provided opportunities for the use of advanced data-centric technologies in power plants. Gas turbines, which are widely used to produce electricity, are exposed to fluctuating conditions depending on various environmental and operational factors. Precise forecasting of their energy production is essential to maintain proper performance, reduce operating costs, and promote sustainability.

In this work, we introduce a machine learning solution using Artificial Neural Networks (ANN) to forecast the net energy output of a gas turbine, based on critical input parameters such as:
->Ambient temperature
->Ambient pressure
->Relative humidity
->Exhaust vacuum

📌 Dataset
The investigation employs a publicly available dataset from the UCI Machine Learning Repository, containing over 36,000 real readings from a gas turbine commissioned in Turkey. Each observation comprises six input variables and a corresponding net electrical output value (PE).

🛠️ Methodology
1. The dataset was preprocessed through normalization.
2. Data was split into training and test subsets.
3. A feedforward neural network model was built using Keras and TensorFlow, consisting of:
   a. Multiple dense layers with ReLU activation
   b. A linear output layer for regression
4. Mean Squared Error (MSE) was used as the loss function.
5. Adam optimizer accelerated convergence.
6. Early stopping and dropout techniques were applied to avoid overfitting and improve generalization.

📈 Results
The model demonstrated:
1. Zero root mean squared error (RMSE) and the highest R² score on the test set.
2. Excellent ability to capture nonlinear associations between input variables and energy output.
3. A Predicted vs. Actual plot confirming model accuracy.

📌 Conclusion & Future Scope
This project validates the suitability of neural networks for modeling and forecasting energy yields from gas turbine systems. The results contribute to the growing field of smart energy management and open up possibilities for real-time predictive monitoring in power plants.
Future enhancements can include:
1. Experimenting with advanced architectures like LSTM for temporal modeling.
2. Developing an interactive dashboard interface for energy analysts and engineers.
