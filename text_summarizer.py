from transformers import pipeline

def summarize_text(text):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    print("Original Text: ", text)
    print("Summary: ", summary[0]['summary_text'])
    return summary[0]['summary_text']

if __name__ == "__main__":
    sample_text = ("Your long text goes here. "
                   "Ensure the text is long enough for the summarizer to work effectively.")
    summary = summarize_text(sample_text)
