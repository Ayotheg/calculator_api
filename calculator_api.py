<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welder Calculator</title>
  <style>
   .calculator {
  width: 220px;
  margin: 20px auto;
  padding: 10px;
  border: 2px solid #333;
  border-radius: 10px;
  background: #f9f9f9;
}

#display {
  width: 100%;
  height: 40px;
  margin-bottom: 10px;
  font-size: 20px;
  text-align: right;
  padding: 5px;
}

.buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 5px;
}

button {
  height: 50px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  border: none;
  background: #eee;
  border-radius: 5px;
}

button:hover {
  background: #ddd;
}

  </style>
</head>
<body>
 <div class="calculator">
  <input type="text" id="display" disabled />

  <div class="buttons">
    <button onclick="appendNumber(7)">7</button>
    <button onclick="appendNumber(8)">8</button>
    <button onclick="appendNumber(9)">9</button>
    <button onclick="setOperation('dividir')">÷</button>

    <button onclick="appendNumber(4)">4</button>
    <button onclick="appendNumber(5)">5</button>
    <button onclick="appendNumber(6)">6</button>
    <button onclick="setOperation('multiplicar')">×</button>

    <button onclick="appendNumber(1)">1</button>
    <button onclick="appendNumber(2)">2</button>
    <button onclick="appendNumber(3)">3</button>
    <button onclick="setOperation('restar')">-</button>

    <button onclick="appendNumber(0)">0</button>
    <button onclick="clearDisplay()">C</button>
    <button onclick="calculateResult()">=</button>
    <button onclick="setOperation('sumar')">+</button>
  </div>
</div>


  <script>
    let current = "";
let firstNum = null;
let operation = null;

const baseURL = "https://calculator-api-o5d2.onrender.com"; // ✅ API URL

function appendNumber(num) {
  current += num;
  document.getElementById("display").value = current;
}

function setOperation(op) {
  firstNum = current;
  current = "";
  operation = op;
}

async function calculateResult() {
  if (!firstNum || !operation || current === "") return;

  try {
    // Try API call
    const url = `${baseURL}/${operation}?num1=${firstNum}&num2=${current}`;
    const response = await fetch(url);
    if (!response.ok) throw new Error("API Error");

    const data = await response.json();

    if (data.resultado !== undefined) {
      document.getElementById("display").value = data.resultado;
      current = data.resultado;
    } else {
      throw new Error("Invalid API response");
    }
  } catch (err) {
    // ✅ Local fallback if API fails
    let result;
    const num1 = parseFloat(firstNum);
    const num2 = parseFloat(current);

    switch (operation) {
      case "sumar":
        result = num1 + num2;
        break;
      case "restar":
        result = num1 - num2;
        break;
      case "multiplicar":
        result = num1 * num2;
        break;
      case "dividir":
        result = num2 !== 0 ? num1 / num2 : "Err";
        break;
      default:
        result = "Err";
    }

    document.getElementById("display").value = result;
    current = result;
  }

  firstNum = null;
  operation = null;
}

function clearDisplay() {
  current = "";
  firstNum = null;
  operation = null;
  document.getElementById("display").value = "";
}

  </script>
</body>
</html>
