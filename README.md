

# Instagram Fake Profile Detection


This project is designed to detect fake profiles on Instagram by analyzing various profile attributes. It uses the `instaloader` library to scrape profile data and assigns a fraud score based on predefined criteria. The results are stored in an SQLite database for further analysis.

## Introduction

With the rise of social media platforms, fake profiles have become a significant concern. This project focuses on detecting fake profiles on Instagram using profile data like follower count, post count, and engagement metrics. By analyzing these features, the tool assigns a fraud score to determine whether a profile is likely fake or genuine.

## Features

- **Profile Scraping**: Automatically scrapes Instagram profiles using `instaloader`.
- **Fraud Score Calculation**: Assigns a fraud score based on factors such as:
  - Missing profile picture
  - Low post count
  - Low follower count
  - High following count
  - Follower-following imbalance
- **Profile Categorization**: Classifies profiles based on their fraud score.
- **Database Storage**: Stores the results of profile analysis in an SQLite database for easy access and future analysis.

## Technologies Used

- **Programming Language**: Python
- **Framework**: Flask
- **Libraries**:
  - `instaloader` for scraping Instagram profiles
  - `sqlite3` for database management

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NaveenShaji742/instagramfakeprofiledetection.git
   ```
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the Flask application:
   ```bash
   python app.py
   ```

## Usage

1. Access the web interface provided by Flask after starting the application.
2. Enter the Instagram username of the profile you want to analyze.
3. The tool will scrape the profile data and calculate a fraud score.
4. The result, including profile data and fraud score, will be stored in the database.

## Dataset

No predefined dataset is required as the data is scraped from live Instagram profiles using `instaloader`.

## Model

This project uses a heuristic scoring model based on profile characteristics rather than a traditional machine learning model. The following criteria are used:
- Missing profile picture adds 30 points to the fraud score.
- Less than 5 posts adds 20 points.
- Fewer than 100 followers adds 20 points.
- Following more than 1000 accounts adds 30 points.
- Having fewer followers than following adds 30 points.

## Results

The project assigns a fraud score to each profile. A higher fraud score indicates a higher likelihood of the profile being fake. Profiles are categorized based on their score:
- 80 or higher: Likely Fake
- Below 80: Likely Genuine

## Future Enhancements

- **Real-time Detection**: Introduce real-time monitoring for fake profiles.
- **Machine Learning**: Implement machine learning algorithms to improve fraud score accuracy.
- **Additional Features**: Add NLP for analyzing profile bio descriptions and image analysis for more accurate detection.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue for suggestions or bug reports.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

