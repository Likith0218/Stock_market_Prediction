const typingText = document.querySelector(".typing-text");
const phrases = [
  "Real-time Stock Forecasting",
  "Daily & Hourly Predictions",
  "Market Sentiment Analysis",
  "TradingView-style Dashboard"
];
let currentPhrase = 0;
let charIndex = 0;
let isDeleting = false;

function typeEffect() {
  const current = phrases[currentPhrase];
  if (isDeleting) {
    typingText.textContent = current.substring(0, charIndex--);
  } else {
    typingText.textContent = current.substring(0, charIndex++);
  }

  if (!isDeleting && charIndex === current.length) {
    isDeleting = true;
    setTimeout(typeEffect, 1000);
  } else if (isDeleting && charIndex === 0) {
    isDeleting = false;
    currentPhrase = (currentPhrase + 1) % phrases.length;
    setTimeout(typeEffect, 500);
  } else {
    setTimeout(typeEffect, isDeleting ? 50 : 100);
  }
}

typeEffect();
