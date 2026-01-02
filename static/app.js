document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const fileInput = document.getElementById("trends");

    form.addEventListener("submit", function (e) {
        if (!fileInput.files.length) {
            e.preventDefault();
            alert("Please select a Google Trends CSV file first.");
            return;
        }

        const file = fileInput.files[0];
        const ext = file.name.split(".").pop().toLowerCase();

        if (ext !== "csv") {
            e.preventDefault();
            alert("Only CSV files are allowed.");
            fileInput.value = "";
            return;
        }

        // Optional: show loading state
        const btn = form.querySelector(".btn");
        btn.innerText = "Processing...";
        btn.disabled = true;
    });

});
