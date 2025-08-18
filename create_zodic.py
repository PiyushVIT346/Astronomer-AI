import pandas as pd

# Define the zodiac sign data as a list of dictionaries
zodiac_rows = [
    {"Date begin": "Mar 21", "Date End": "Apr 19", "Zodiac": "Aries"},
    {"Date begin": "Apr 20", "Date End": "May 20", "Zodiac": "Taurus"},
    {"Date begin": "May 21", "Date End": "Jun 20", "Zodiac": "Gemini"},
    {"Date begin": "Jun 21", "Date End": "Jul 22", "Zodiac": "Cancer"},
    {"Date begin": "Jul 23", "Date End": "Aug 22", "Zodiac": "Leo"},
    {"Date begin": "Aug 23", "Date End": "Sep 22", "Zodiac": "Virgo"},
    {"Date begin": "Sep 23", "Date End": "Oct 22", "Zodiac": "Libra"},
    {"Date begin": "Oct 23", "Date End": "Nov 21", "Zodiac": "Scorpio"},
    {"Date begin": "Nov 22", "Date End": "Dec 21", "Zodiac": "Sagittarius"},
    {"Date begin": "Dec 22", "Date End": "Jan 19", "Zodiac": "Capricorn"},
    {"Date begin": "Jan 20", "Date End": "Feb 18", "Zodiac": "Aquarius"},
    {"Date begin": "Feb 19", "Date End": "Mar 20", "Zodiac": "Pisces"},
]

# Create DataFrame
df = pd.DataFrame(zodiac_rows)

# Save to CSV
df.to_csv("zodiac_horoscope.csv", index=False)

print("Created zodiac_horoscope.csv")
