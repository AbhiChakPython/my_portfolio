document.addEventListener("DOMContentLoaded", function () {
    // Check if Typed.js is loaded before initializing
    if (typeof Typed !== "function") {
        console.error("Typed.js failed to load.");
    } else {
        console.log("Typed.js loaded successfully.");

        // Typed.js Options
        var options = {
            typeSpeed: 250, // Slow typing speed in milliseconds
            backSpeed: 150, // Slow backspacing speed
            loop: true,
            cursorChar: '|',
            startDelay: 500,
            backDelay: 1000, // Add a slight pause before typing again
            showCursor: true,
            smartBackspace: true
        };

        // Initialize Typed.js for multiple elements
        new Typed('#navigate', { ...options, strings: ['navigate$'] });
        new Typed('#ascii-art', { ...options, strings: ['ascii-art$'] });
        new Typed('#about_me', { ...options, strings: ['about_me$'] });
        new Typed('#skills', { ...options, strings: ['skills$'] });
        new Typed('#projects', { ...options, strings: ['projects$'] });
        new Typed('#contact', { ...options, strings: ['contact$'] });
    }

    // CLI Command Handling
    document.getElementById('command_line').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            const command = this.value.trim().toLowerCase(); // Get and normalize the input
            const outputDiv = document.getElementById('output'); // Terminal output area

            switch (command) {
                case 'about_me':
                    outputDiv.innerHTML = "Navigating to About Me Section...";
                    document.querySelector('.about-me-section').scrollIntoView({ behavior: 'smooth' });
                    break;

                case 'skills':
                    outputDiv.innerHTML = "Exploring Skills Section...";
                    document.querySelector('.skills-section').scrollIntoView({ behavior: 'smooth' });
                    break;

                case 'personal_projects':
                    outputDiv.innerHTML = "Heading to Personal Projects Section...";
                    document.querySelector('.personal-projects-section').scrollIntoView({ behavior: 'smooth' });
                    break;

                case 'contact_me':
                    outputDiv.innerHTML = "Connecting with Contact Me Section...";
                    document.querySelector('.contact-me-section').scrollIntoView({ behavior: 'smooth' });
                    break;

                case 'email_me':
                    outputDiv.innerHTML = "Opening Email Client...";
                    window.location.href = "mailto:abhijit@example.com";
                    break;

                case 'github':
                    outputDiv.innerHTML = "Redirecting to GitHub Profile...";
                    window.open("https://www.github.com/abhijit", "_blank");
                    break;

                case 'linkedin':
                    outputDiv.innerHTML = "Redirecting to LinkedIn Profile...";
                    window.open("https://www.linkedin.com/in/abhijit", "_blank");
                    break;

                case 'help':
                    outputDiv.innerHTML = `
                    Available commands:
                    - about_me: Navigate to About Me Section
                    - skills: Explore Skills Section
                    - personal_projects: Head to Personal Projects Section
                    - contact_me: Connect with Contact Me Section
                    - email_me: Open Email Client
                    - github: Redirect to GitHub Profile
                    - linkedin: Redirect to LinkedIn Profile
                    `;
                    break;

                default:
                    // Error message for unrecognized commands
                    outputDiv.innerHTML = `Error: "${command}" is not a valid command. Type 'help' for a list of available commands.`;
            }

            this.value = ''; // Clear the input field
        }
    });
});