document.addEventListener("DOMContentLoaded", function() {
    const amountDisplay = document.getElementById("amount");
    const numButtons = document.querySelectorAll(".num-btn");
    const clearButton = document.getElementById("clear");

    let amount = "";

    numButtons.forEach(button => {
        button.addEventListener("click", function() {
            if (this.id === "clear") {
                amount = "";
            } else {
                amount += this.innerText;
            }
            amountDisplay.innerText = amount || "0";
        });
    });
});
