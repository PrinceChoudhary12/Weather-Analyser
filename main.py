from data_loader import load_weather_data
from data_cleaner import clean_weather_data
from data_visualizer import create_matplotlib_dashboard

def main():
    file_path = "data/data.csv"
    df = load_weather_data(file_path)
    cleaned = clean_weather_data(df)
    cleaned.to_csv("data/cleaned_data.csv", index=False)
    create_matplotlib_dashboard(cleaned, show=True)

if __name__ == "__main__":
    main()
