# Equities Trading Strategy Using Sentiment Analysis

This project demonstrates the development of an algorithmic trading strategy by integrating sentiment analysis of Reddit posts from the WallStreetBets subreddit with traditional market indicators. Using advanced NLP models, the project aims to enhance trading decisions by combining sentiment predictions with financial metrics.

## Key Features
- **Sentiment Analysis:** Utilizes transformer-based models like BERT, GPT-2, and GPT-Neo to classify sentiments as Positive, Neutral, or Negative.
- **Trading Strategy:** Implements a trend-following strategy using sentiment predictions and market indicators such as OHLC, RSI, and moving averages.
- **Performance Evaluation:** Achieved an 8.87% return over 18 months of back-testing, showcasing the integration of sentiment-driven insights with traditional trading metrics.

## Project Structure
- `data/`: Contains cleaned Reddit posts and financial data.
- `scripts/`: Python scripts for data preprocessing, model training, and back-testing.
- `results/`: Performance metrics, plots, and back-testing outcomes.
- `documentation/`: Includes the project documentation and detailed reports.

## Technologies Used
- **Python**: For data preprocessing, modeling, and trading strategy implementation.
- **Hugging Face Transformers**: For implementing NLP models.
- **YFinance API**: For retrieving historical financial data.
- **Backtrader**: For simulating and back-testing trading strategies.

## Setup Instructions
1. Open terminal and navigate to the folder where you want to save the repo using the command:
   ```bash
   cd <dir path>
   ```
2. Clone the repository:
   ```bash
   git clone <link to repo>
   ```
3. Open the cloned repository folder in a local code editor (e.g., VSCode).
4. Run the data preprocessing steps in the following sequence:
   - `dpp_eda.py`
   - `absa_dpp.py`
   Make sure to replace the paths to load the `reddit_wsb.csv` data in the files (the CSV file is in the `data/` folder after cloning). Update paths to save the final preprocessed files as needed.
5. Execute the sentiment analysis scripts:
   - `bert.py`
   - `gpt2.py`
   - `gpt_neo.py`
6. Run the trading strategy simulation:
   ```bash
   python scripts/trading_strategy.py
   ```
   This generates the P&L charts and total return metrics.

## Results

The results section highlights the performance of the sentiment classification models and the trading strategy. GPT-Neo achieved the highest accuracy (88%) among the models tested, as demonstrated in the learning curves and performance metrics. The trading strategy simulation, depicted in the P&L chart, showed consistent portfolio growth, with a total return of 8.87% over 18 months, validating the integration of sentiment analysis with technical indicators for effective decision-making.

## Documentation and Resources
- **Project Documentation:** [View Documentation](./documentation/project_report.pdf)
- **Video Presentation:** [Watch Video](./documentation/Presentation_Video.mp4)


## Contributing
Contributions are welcome! Feel free to fork the repository, open an issue, or submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## References
- Chen, Y., Li, X., & Zhang, Z. (2022). Aspect-based Sentiment Analysis in Financial News. In Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing (EMNLP).
- Kumar, R., & Shankar, A. (2021). Sentiment Analysis on Reddit’s WallStreetBets. Stanford CS229 Machine Learning Final Projects.
- Liu, J., Zhao, R., & Xu, Y. (2019). Multimodal Aspect-based Sentiment Analysis: Integrating Text and Image Data. In Proceedings of the 2019 Conference on Computer Vision and Pattern Recognition (CVPR).
- Zhang, L., Wang, Y., & Liu, H. (2020). Deep Q-Networks for Stock Trading with Composite Sentiment Scores. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL).

