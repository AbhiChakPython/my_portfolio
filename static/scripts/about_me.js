document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("toggleMode");
    const body = document.body;

    // Check if Dark Mode was previously enabled (using localStorage)
    if (localStorage.getItem("darkMode") === "enabled") {
        body.classList.add("dark-mode");
        toggleButton.innerHTML = "☀️ Light Mode";
    }

    // Toggle Dark Mode on button click
    toggleButton.addEventListener("click", function () {
        body.classList.toggle("dark-mode");

        if (body.classList.contains("dark-mode")) {
            localStorage.setItem("darkMode", "enabled");
            toggleButton.innerHTML = "☀️ Light Mode";
        } else {
            localStorage.setItem("darkMode", "disabled");
            toggleButton.innerHTML = "🌙 Dark Mode";
        }
    });
});
