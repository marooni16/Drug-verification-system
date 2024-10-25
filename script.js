document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("verification-form");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission

        const batchNumber = document.getElementById("batch_number").value;
        const drugId = document.getElementById("drug_id").value;
        const nafdacNumber = document.getElementById("nafdac_number").value;

        // Validate inputs
        if (batchNumber.trim() === "" || drugId.trim() === "" || nafdacNumber.trim() === "") {
            displayError("Please enter valid details for all fields and try again.");
            return;
        }

        // Create a data object to send to the server
        const data = {
            batch_number: batchNumber,
            drug_id: drugId,
            nafdac_number: nafdacNumber
        };

        // Send data to Flask backend using fetch
        fetch("/verify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json()) // Parse the JSON response
        .then(result => {
            const resultDiv = document.getElementById("result");

            if (result.status === "Invalid") {
                displayError(`${result.message} Please enter valid details and <button id="retry-btn">Try Again</button>.`);
                setupRetryButton(); // Set up the retry button to reset the form
            } else {
                resultDiv.innerHTML = `<h2>Verification Result</h2>
                                       <p>Status: ${result.status}</p>
                                       <p>Message: ${result.message}</p>`;
            }
        })
        .catch(error => {
            displayError("An error occurred. Please try again.");
            setupRetryButton(); // Set up the retry button to reset the form
        });
    });

    // Function to display an error message
    function displayError(message) {
        const resultDiv = document.getElementById("result");
        resultDiv.innerHTML = `<p class="error-message">${message}</p>`;
    }

    // Function to set up the "Try Again" button
    function setupRetryButton() {
        const retryBtn = document.getElementById("retry-btn");
        if (retryBtn) {
            retryBtn.addEventListener("click", function () {
                resetForm();
            });
        }
    }

    // Function to reset the form after an error
    function resetForm() {
        document.getElementById("batch_number").value = "";
        document.getElementById("drug_id").value = "";
        document.getElementById("nafdac_number").value = "";
        document.getElementById("result").innerHTML = ""; // Clear the result/error message
    }
});
