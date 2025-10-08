// Create a container for the canvas to hold the particles background
const canvasContainer = document.createElement("div");
canvasContainer.style.position = "absolute";
canvasContainer.style.top = 0;
canvasContainer.style.left = 0;
canvasContainer.style.width = "100%";
canvasContainer.style.height = "100%";
canvasContainer.style.zIndex = "-1"; // Ensures the background stays behind all content
document.body.prepend(canvasContainer); // Adds the container at the very start of <body>

// Create the canvas for the animation
const canvas = document.createElement("canvas");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
canvasContainer.appendChild(canvas);

const ctx = canvas.getContext("2d");

// Array to store particle properties
const particles = [];
const colors = ["#00ffcc", "#ff33cc", "#66ff66"]; // Neon-themed particle colors

// Function to create particles with random properties
function createParticles() {
  for (let i = 0; i < 100; i++) {
    particles.push({
      x: Math.random() * canvas.width, // Random x-coordinate
      y: Math.random() * canvas.height, // Random y-coordinate
      radius: Math.random() * 3 + 1, // Random particle size (1-3px)
      color: colors[Math.floor(Math.random() * colors.length)], // Random color
      dx: Math.random() * 2 - 1, // Random horizontal speed
      dy: Math.random() * 2 - 1 // Random vertical speed
    });
  }
}

// Function to draw and animate particles
function drawParticles() {
  ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas for each frame
  particles.forEach(particle => {
    // Draw each particle as a circle
    ctx.beginPath();
    ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
    ctx.fillStyle = particle.color; // Assign the particle's color
    ctx.fill();
    ctx.closePath();

    // Update particle position
    particle.x += particle.dx;
    particle.y += particle.dy;

    // Reverse direction if the particle hits a canvas boundary
    if (particle.x < 0 || particle.x > canvas.width) particle.dx *= -1;
    if (particle.y < 0 || particle.y > canvas.height) particle.dy *= -1;
  });

  requestAnimationFrame(drawParticles); // Repeat animation for the next frame
}

// Responsive canvas resizing
window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = document.body.scrollHeight; // Covers the full page height

  particles.length = 0; // Clear existing particles
  createParticles(); // Recreate particles for the new canvas size
});

// Initialize particles and start animation
createParticles();
drawParticles();