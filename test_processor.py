from text_processor import clean_text

sample_text = """
    Rounak Kumar


    Python     Java       SQL


    Education
    B.Tech   Computer Science
"""

cleaned = clean_text(sample_text)

print(cleaned)