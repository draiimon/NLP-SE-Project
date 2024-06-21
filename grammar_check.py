import language_tool_python

def check_grammar(text):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    corrected_text = tool.correct(text)
    print("Original Text: ", text)
    print("Corrected Text: ", corrected_text)
    return corrected_text

if __name__ == "__main__":
    sample_text = "This is an example sentence with a error."
    corrected_text = check_grammar(sample_text)
