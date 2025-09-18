from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend (your website) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ayotheg.github.io/welderskit/calculator.html"],   # Change "*" to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "✅ Calculator API is running!"}

@app.get("/sumar")
def sumar(num1: float, num2: float):
    return {"resultado": num1 + num2}

@app.get("/restar")
def restar(num1: float, num2: float):
    return {"resultado": num1 - num2}

@app.get("/multiplicar")
def multiplicar(num1: float, num2: float):
    return {"resultado": num1 * num2}

@app.get("/dividir")
def dividir(num1: float, num2: float):
    if num2 == 0:
        return {"error": "Division by zero not allowed"}
    return {"resultado": num1 / num2}
