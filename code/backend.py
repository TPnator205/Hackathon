from openai import OpenAI
import fitz


def main(pdf_):
    pdf_file = fitz.open(pdf_)
    text_content = ""
    for page_ind in range(len(pdf_file)):
        page = pdf_file[page_ind]
        text_content += page.get_text("text")
    return text_content


def summary_gen(content, ai_magic: OpenAI):
    
    prompt = """
    You are an academic summarizer. Summarize the following lecture or notes clearly and accurately.
    Then provide 3-5 key insights or patterns from the content that would help a student understand the main ideas.
    
    Text: {""" + content + """}
    Return in this format:
    {
    "summary": "…",
    "key_insights": ["…", "…", "…"]
    }
    """
    
    response = ai_magic.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are the best academic summarizer, summarizing lecture notes."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content
    

def formula_gen(content, ai_magic: OpenAI):
    
    prompt = """
    Extract all mathematical formulas, equations, and symbols from the text below.
    For each formula, include:
    - The formula as written
    - A short explanation of what it represents
    - The context or topic it belongs to (if available)

    Text: {""" + content + """}

    Return as JSON:
    [
    {"formula": "...", "meaning": "...", "context": "..."}
    ]
    """
    response = ai_magic.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract all mathematical or symbolic formulas from the text and explain what each formula means"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content

    
def flashcards_gen(content, ai_magic: OpenAI):
     
    prompt = """
    You are an expert tutor. Create clear and concise flashcards from the following text. 
    Each flashcard should have:
    - A front (question or term)
    - A back (concise explanation or answer)

    Make them suitable for spaced repetition learning. Avoid redundancy.
    Text: { """ + content + """}
    Return as JSON in this format:
    [
        {"front": "...", "back": "..."},
        {"front": "...", "back": "..."}
    ]
    """
    
    response = ai_magic.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract all mathematical or symbolic formulas from the text and explain what each formula means"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content
    
def quiz_gen(content, ai_magic:OpenAI):

    prompt = """
    You are an intelligent quiz generator for university students. 
    Based on the text below, create a quiz that tests understanding, not rote memorization.

    Include:
    - 5 multiple-choice questions (each with 4 options and one correct answer)
    - 3 short-answer questions that require explanation or reasoning

    Keep questions challenging but fair. Avoid trick questions.  
    Make sure all content strictly comes from the provided text.

    Text: {""" + content + """}

    Return in JSON format exactly like this:
    {
    "multiple_choice": [
        {
        "question": "...",
        "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
        "correct_answer": "B"
        }
    ],
    "short_answer": [
        {
        "question": "...",
        "expected_answer": "..."
        }
    ]
    }
    """
    response = ai_magic.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an intelligent quiz generator for university students"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content



if __name__ == "__main__":
    client = OpenAI(api_key="sk-proj-fgiK2JJBytLimDDWj-TgKTenrTWq5lVc6wkkfoAtKcuAV2j52HEzFK" +
                    "JImKl09XS6c6Jtl8KxjQT3BlbkFJA46oPAdG3DCxwG-DXITmthCNciQXwI73o1-HiaAuqu0BT" +
                    "rWnZFXAuJHyRzMIZ3zL4SA5f1X1EA")
    
    filename = "sample_files/Dotproduct.pdf"
    content_main = main(filename)
    
    # print(summary_gen(main(filename), client))
    # print(formula_gen(content_main, client))
    print(formula_gen(content_main, client))
    print(quiz_gen(content_main, client))
    