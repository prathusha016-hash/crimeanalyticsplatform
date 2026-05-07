function predict() {
    let crime = document.getElementById("crime").value;
    let age = document.getElementById("age").value;
    let weapon = document.getElementById("weapon").value;

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            crime: crime,
            age: age,
            weapon: weapon
        })
    })
    .then(res => res.json())
    .then(data => {
        let resultBox = document.getElementById("result");

        resultBox.innerText = data.result;

        if(data.result.includes("High Risk")) {
            resultBox.style.color = "red";
        }
        else if(data.result.includes("Sensitive")) {
            resultBox.style.color = "orange";
        }
        else {
             resultBox.style.color = "lightgreen";
        }
    });
}