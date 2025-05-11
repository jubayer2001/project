// scripts.js

document.addEventListener('DOMContentLoaded', () => {
  // Hero section fade-in
  const heroInner = document.querySelector('.hero-inner');
  heroInner.style.opacity = 0;
  heroInner.style.transition = 'opacity 1s ease-in-out';
  setTimeout(() => {
    heroInner.style.opacity = 1;
  }, 100);

  // Scroll-triggered animations for service items
  const serviceItems = document.querySelectorAll('.service-item');

  const observerOptions = {
    threshold: 0.1
  };

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if(entry.isIntersecting){
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  serviceItems.forEach(item => {
    item.classList.add('fade-in');
    observer.observe(item);
  });
});
