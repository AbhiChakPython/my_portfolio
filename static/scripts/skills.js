document.addEventListener("DOMContentLoaded", function () {
    const progressBars = [
        { name: "Python", level: "90%" },
        { name: "Django", level: "85%" },
        { name: "JavaScript", level: "75%" },
        { name: "PostgreSQL", level: "80%" }
    ];

    const progressContainer = document.querySelector(".progress-bars");

    progressBars.forEach(skill => {
        const bar = document.createElement("div");
        bar.classList.add("progress-bar-container");
        bar.innerHTML = `
            <p>${skill.name}</p>
            <div class="progress-container">
                <div class="progress-bar" style="width: ${skill.level};"></div>
            </div>
        `;
        progressContainer.appendChild(bar);
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const circles = document.querySelectorAll(".circular-progress");

    circles.forEach(circle => {
        let progress = parseInt(circle.getAttribute("data-progress"), 10);
        let degrees = (progress / 100) * 360;

        circle.style.background = `conic-gradient(#33ff33 ${degrees}deg, #222 ${degrees}deg)`;
        circle.querySelector(".progress-value").innerText = `${progress}%`;
    });
});


