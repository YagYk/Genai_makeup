# End-To-End-Gemini-Project
# Beauty Advisor AI Application

An intelligent beauty advisor application powered by Google's Gemini AI that provides personalized makeup and accessory recommendations based on uploaded images and user preferences.

## Features

- **Image Analysis**: Upload photos to receive personalized beauty recommendations
- **Interactive Chat**: Engage in conversations about makeup and facial features
- **User Authentication**: Secure login system for personalized experience
- **Real-time Responses**: Instant AI-powered recommendations using Gemini Pro
- **Facial Feature Detection**: Advanced facial analysis using MediaPipe
- **Session Management**: Maintains chat history during user sessions

## Installation

1. Clone the repository:
git clone https://github.com/YagYk/Genai_makeup.git
cd Genai_makeup

2. Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install required packages:
pip install -r requirements.txt

4. Create a `.env` file in the root directory and add your Google API key:
GOOGLE_API_KEY=your_api_key_here

## Usage

1. Start the application:
streamlit run vision.py

2. Open your browser and navigate to the provided local URL (typically http://localhost:8501)

3. Create an account or log in to access the beauty advisor

4. Upload an image and describe your desired look to receive personalized recommendations

5. Use the chat interface to ask specific questions about makeup and styling

## Project Structure

- `vision.py`: Main application file with image processing and AI recommendation logic
- `login.py`: User authentication and account management
- `facial_beauty_advisor.py`: Facial feature detection and analysis
- `requirements.txt`: List of Python dependencies
- `.env`: Configuration file for API keys (not included in repository)

## Technologies Used

- Streamlit: Web interface
- Google Generative AI (Gemini Pro): AI model for recommendations
- MediaPipe: Facial feature detection
- SQLite: User data storage
- Python-dotenv: Environment variable management

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contact

Yagyansh - [GitHub Profile](https://github.com/YagYk)

Project Link: [https://github.com/YagYk/Genai_makeup](https://github.com/YagYk/Genai_makeup)
