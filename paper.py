import os
from dotenv import load_dotenv
from fastapi import HTTPException
from google import genai
from gcse_boards_config import exam_boards_gcse

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY environment variable is not set. "
        "Please add it to your .env file or export GEMINI_API_KEY in your environment."
    )

client = genai.Client(api_key=api_key)


class Paper:
    def __init__(self, subject: str, tier: str, year: int, board: str, file):
        self.subject = subject
        self.tier = tier
        self.year = year
        self.board = board
        self.file = file

    def grade(self):
        error = False
        message = None
        if self.board.lower() in exam_boards_gcse.keys():
            if self.subject.lower() in exam_boards_gcse[self.board.lower()]:
                if self.year <= 2026 or self.year >= 2000:
                    save_path = f"saved {self.file.filename}"
                    with open(save_path, "wb") as buffer:
                        buffer.write(self.file.file.read())
                    uploaded_file = client.files.upload(file=save_path)
                    prompt = f"""
                                Grade this {self.board} {self.subject} ({self.tier} tier) in {self.year} exam paper.
                                use the mark scheme for that paper. 
                                Give Total Marks, Estimated Grade, and Feedback.
                                Please use plain text only. Do not use Markdown formatting. do not include \n at all, only a short summary is needed
                                100 words max with the marks, percentage and estimated grade
                                """

                    response = client.models.generate_content(
                        model="gemini-3.6-flash", contents=[uploaded_file, prompt]
                    )

                    return {"message": "Grading Complete!", "feedback": response.text}
                else:
                    error = True
                    message = "year must be an integer between 2000 and 2026"
            else:
                error = True
                message = f"subject must be one of these {list(exam_boards_gcse[self.board.lower()])}"
        else:
            error = True
            message = f"board must be one of these {list(exam_boards_gcse.keys())}"

        if error:
            raise HTTPException(status_code=400, detail=message)
        else:
            return {"error": error, "message": message}
