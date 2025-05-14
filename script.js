// Dynamically create the navigation bar
function createNavbar() {
  const navbar = document.createElement("div");
  navbar.className = "navbar";

  const title = document.createElement("h1");
  title.textContent = "Stock Dashboard";

  const navList = document.createElement("ul");

  const navItems = [
    { text: "Home", href: "#home" },
    { text: "Features", href: "#features" },
    { text: "About", href: "#about" },
    { text: "Contact", href: "#contact" },
  ];

  navItems.forEach((item) => {
    const listItem = document.createElement("li");
    const link = document.createElement("a");
    link.textContent = item.text;
    link.href = item.href;
    listItem.appendChild(link);
    navList.appendChild(listItem);
  });

  navbar.appendChild(title);
  navbar.appendChild(navList);

  document.body.prepend(navbar); // Add the navbar to the top of the body
}

// Dynamically create a container for the main content
function createMainContent() {
  const container = document.createElement("div");
  container.className = "container";

  const title = document.createElement("div");
  title.className = "title";
  title.textContent = "Welcome to the Stock Dashboard";

  const typingText = document.createElement("div");
  typingText.className = "typing-text";
  typingText.textContent = ""; // Placeholder for the typing effect

  const card = document.createElement("div");
  card.className = "card";
  card.textContent = "This is a sample card. Add your content here.";

  container.appendChild(title);
  container.appendChild(typingText);
  container.appendChild(card);

  document.body.appendChild(container); // Add the container to the body
}

// Initialize the typing effect
function typeEffect() {
  const typingText = document.querySelector(".typing-text");
  const phrases = [
    "Real-time Stock Forecasting",
    "Daily & Hourly Predictions",
    "Market Sentiment Analysis",
    "TradingView-style Dashboard",
  ];
  let currentPhrase = 0;
  let charIndex = 0;
  let isDeleting = false;

  function type() {
    const current = phrases[currentPhrase];
    if (isDeleting) {
      typingText.textContent = current.substring(0, charIndex--);
    } else {
      typingText.textContent = current.substring(0, charIndex++);
    }

    if (!isDeleting && charIndex === current.length) {
      isDeleting = true;
      setTimeout(type, 1000);
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      currentPhrase = (currentPhrase + 1) % phrases.length;
      setTimeout(type, 500);
    } else {
      setTimeout(type, isDeleting ? 50 : 100);
    }
  }

  type();
}

// Run everything after the DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  createNavbar();
  createMainContent();
  typeEffect();
});
