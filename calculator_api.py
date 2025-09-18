from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import re
import math
from typing import Union

app = FastAPI(title="Calculator API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ayotheg.github.io/calculator.html",
        "*"  # Remove this in production, add your specific domains
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

def clean_number_input(value: str) -> float:
    """Clean and validate number input"""
    try:
        # Convert to string first
        clean_value = str(value).strip()
        
        # Remove any HTML/CSS contamination
        clean_value = re.sub(r'<[^>]+>', '', clean_value)  # Remove HTML tags
        clean_value = re.sub(r'[a-zA-Z-]+:\s*[^;]+[;]?', '', clean_value)  # Remove CSS properties
        clean_value = re.sub(r'width:\s*\d+px[;]?', '', clean_value)  # Specific fix for width CSS
        clean_value = re.sub(r'[a-zA-Z]+', '', clean_value)  # Remove any remaining letters
        
        # Remove extra spaces and special characters except numbers, decimal, minus
        clean_value = re.sub(r'[^\d.-]', '', clean_value)
        
        # Handle multiple decimal points
        parts = clean_value.split('.')
        if len(parts) > 2:
            clean_value = parts[0] + '.' + ''.join(parts[1:])
        
        # Handle multiple minus signs
        if clean_value.count('-') > 1:
            if clean_value.startswith('-'):
                clean_value = '-' + clean_value.replace('-', '')
            else:
                clean_value = clean_value.replace('-', '')
        
        # Validate the cleaned value
        if not clean_value or clean_value in ['-', '.', '-.']:
            raise ValueError("Invalid number format")
        
        # Convert to float
        result = float(clean_value)
        
        # Check for infinity or NaN
        if math.isinf(result) or math.isnan(result):
            raise ValueError("Invalid number: infinity or NaN")
            
        return result
        
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid number format: '{value}'. Error: {str(e)}"
        )

@app.get("/")
def home():
    return {
        "message": "✅ Calculator API is running!",
        "endpoints": {
            "sumar": "/sumar?num1=5&num2=3",
            "restar": "/restar?num1=10&num2=4", 
            "multiplicar": "/multiplicar?num1=6&num2=7",
            "dividir": "/dividir?num1=15&num2=3"
        }
    }

@app.get("/test")
def test():
    return {"status": "working", "message": "API is healthy"}

@app.get("/sumar")
def sumar(num1: str = Query(...), num2: str = Query(...)):
    """Add two numbers"""
    try:
        n1 = clean_number_input(num1)
        n2 = clean_number_input(num2)
        result = n1 + n2
        
        return {
            "operation": "addition",
            "num1": n1,
            "num2": n2,
            "resultado": result,
            "expression": f"{n1} + {n2} = {result}"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/restar")  
def restar(num1: str = Query(...), num2: str = Query(...)):
    """Subtract two numbers"""
    try:
        n1 = clean_number_input(num1)
        n2 = clean_number_input(num2)
        result = n1 - n2
        
        return {
            "operation": "subtraction", 
            "num1": n1,
            "num2": n2,
            "resultado": result,
            "expression": f"{n1} - {n2} = {result}"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/multiplicar")
def multiplicar(num1: str = Query(...), num2: str = Query(...)):
    """Multiply two numbers"""
    try:
        n1 = clean_number_input(num1)
        n2 = clean_number_input(num2)
        result = n1 * n2
        
        return {
            "operation": "multiplication",
            "num1": n1, 
            "num2": n2,
            "resultado": result,
            "expression": f"{n1} × {n2} = {result}"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dividir")
def dividir(num1: str = Query(...), num2: str = Query(...)):
    """Divide two numbers"""
    try:
        n1 = clean_number_input(num1)
        n2 = clean_number_input(num2)
        
        if n2 == 0:
            raise HTTPException(
                status_code=400, 
                detail="Division by zero is not allowed"
            )
        
        result = n1 / n2
        
        return {
            "operation": "division",
            "num1": n1,
            "num2": n2, 
            "resultado": result,
            "expression": f"{n1} ÷ {n2} = {result}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Advanced calculator endpoint
@app.get("/calculate")
def calculate(expression: str = Query(...)):
    """Evaluate a mathematical expression safely"""
    try:
        # Clean the expression
        expr = str(expression).strip()
        
        # Remove CSS/HTML contamination
        expr = re.sub(r'<[^>]+>', '', expr)
        expr = re.sub(r'[a-zA-Z-]+:\s*[^;]+[;]?', '', expr)
        expr = re.sub(r'width:\s*\d+px[;]?', '', expr)
        
        # Replace symbols
        expr = expr.replace('×', '*').replace('÷', '/')
        expr = expr.replace('x', '*').replace('X', '*')
        
        # Validate characters
        if not re.match(r'^[0-9+\-*/().\s]+$', expr):
            raise ValueError("Expression contains invalid characters")
        
        # Evaluate safely
        allowed_names = {"__builtins__": {}}
        result = eval(expr, allowed_names, {})
        
        if math.isinf(result):
            result = "Infinity"
        elif math.isnan(result):
            result = "Error"
        
        return {
            "expression": expression,
            "cleaned_expression": expr,
            "resultado": result
        }
        
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Division by zero")
    except (SyntaxError, ValueError) as e:
        raise HTTPException(status_code=400, detail=f"Invalid expression: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

# Health check
@app.get("/health")
def health():
    return {"status": "healthy", "api": "calculator"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
