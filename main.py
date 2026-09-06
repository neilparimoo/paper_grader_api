from fastapi import FastAPI, UploadFile, File, Form
from paper import Paper

app = FastAPI()


@app.post("/grade-paper")
def grade_paper(
    file: UploadFile = File(...),
    board: str = Form(default="aqa"),
    subject: str = Form(default="maths"),
    tier: str | None = Form(default="Higher"),
    year: int = Form(default=2025),
):
    paper = Paper(subject, tier, year, board, file)
    result = paper.grade()
    return result