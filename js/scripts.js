// Sapphire Intelligence - Global Scripts

console.log('scripts.js loaded');

// Form submission handler
function handleFormSubmit(form) {
  event.preventDefault();
  
  // Get parent container
  const formContainer = form.parentElement;
  
  // Create success message
  const successDiv = document.createElement('div');
  successDiv.className = 'bg-green-50 border border-green-200 rounded-md p-4 text-green-800';
  successDiv.innerHTML = '<p class="font-medium">Thank you for your inquiry!</p><p class="text-sm mt-1">We\'ll get back to you within 24 hours.</p>';
  
  // Hide form and show success
  form.style.display = 'none';
  formContainer.appendChild(successDiv);
}

// Contact page form handler
function handleContactForm(form) {
  event.preventDefault();
  
  // Find parent container (white panel div)
  const formPanel = form.closest('.bg-white') || form.parentElement;
  
  // Create success message
  const successDiv = document.createElement('div');
  successDiv.className = 'bg-green-50 border border-green-200 rounded-md p-6 text-green-800 text-center';
  successDiv.innerHTML = '<p class="text-xl font-semibold mb-2" style="font-family: \'Playfair Display\', serif;">Thank You</p><p class="text-sm">We\'ll get back to you within 24 hours.</p>';
  
  // Hide form and show success
  form.style.display = 'none';
  formPanel.appendChild(successDiv);
}

document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM ready, running scripts');

  // Navbar scroll effect
  const navbar = document.querySelector('.navbar');
  
  if (navbar) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 20) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
  }

  // Mobile menu toggle
  const menuToggle = document.querySelector('.mobile-menu-toggle');
  const navbarMenu = document.querySelector('.navbar-menu');
  const navbarCta = document.querySelector('.navbar-container > .navbar-cta');

  if (navbarMenu && navbarCta && !navbarMenu.querySelector('.navbar-mobile-cta')) {
    const mobileCta = navbarCta.cloneNode(true);
    mobileCta.classList.add('navbar-mobile-cta');
    navbarMenu.appendChild(mobileCta);
  }

  if (menuToggle && navbarMenu) {
    menuToggle.addEventListener('click', function() {
      navbarMenu.classList.toggle('active');

      const spans = menuToggle.querySelectorAll('span');
      if (navbarMenu.classList.contains('active')) {
        spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
        spans[1].style.opacity = '0';
        spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
      } else {
        spans[0].style.transform = 'none';
        spans[1].style.opacity = '1';
        spans[2].style.transform = 'none';
      }
    });
  }

  // Mobile dropdown toggle
  const dropdownTriggers = document.querySelectorAll('.dropdown-trigger');
  dropdownTriggers.forEach(function(trigger) {
    trigger.addEventListener('click', function(e) {
      // Only for mobile view
      if (window.innerWidth <= 1024) {
        e.preventDefault();
        const dropdown = this.closest('.dropdown');
        dropdown.classList.toggle('active');
      }
    });
  });

  // Dropdown hover effect for desktop
  const dropdowns = document.querySelectorAll('.dropdown');
  
  dropdowns.forEach(function(dropdown) {
    if (window.innerWidth > 768) {
      dropdown.addEventListener('mouseenter', function() {
        const menu = this.querySelector('.dropdown-menu');
        if (menu) {
          menu.style.opacity = '1';
          menu.style.visibility = 'visible';
          menu.style.transform = 'translateX(-50%) translateY(0)';
        }
      });
      
      dropdown.addEventListener('mouseleave', function() {
        const menu = this.querySelector('.dropdown-menu');
        if (menu) {
          menu.style.opacity = '0';
          menu.style.visibility = 'hidden';
          menu.style.transform = 'translateX(-50%) translateY(10px)';
        }
      });
    }
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href !== '#' && href.length > 1) {
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    });
  });

  // Methodology Step Indicator
  const stepItemsCentered = document.querySelectorAll('.step-item');
  const stepIndicator = document.getElementById('step-indicator');
  const stepNumbers = document.querySelectorAll('.step-number');
  const stepTitles = document.querySelectorAll('.step-title');
  const stepDescs = document.querySelectorAll('.step-desc');

  let currentStepCentered = 1;
  let autoPlayIntervalCentered;

  function updateStepCentered(step) {
    // Update indicator (active section highlight via number styles)
    stepItemsCentered.forEach(function(item, index) {
      const numEl = item.querySelector('.step-number');
      const titleEl = item.querySelector('.step-title');
      const descEl = item.querySelector('.step-desc');
      
      if (index + 1 === step) {
        numEl.classList.add('bg-[#2563EB]', 'text-white', 'shadow-md', 'shadow-[#2563EB]/30');
        numEl.classList.remove('bg-[#2563EB]/20', 'text-[#2563EB]');
        titleEl.classList.add('text-[#2563EB]');
        titleEl.classList.remove('text-[#0b132b]');
        descEl.classList.remove('text-gray-500');
        descEl.classList.add('text-gray-700');
      } else {
        numEl.classList.remove('bg-[#2563EB]', 'text-white', 'shadow-md', 'shadow-[#2563EB]/30');
        numEl.classList.add('bg-[#2563EB]/20', 'text-[#2563EB]');
        titleEl.classList.remove('text-[#2563EB]');
        titleEl.classList.add('text-[#0b132b]');
        descEl.classList.add('text-gray-500');
        descEl.classList.remove('text-gray-700');
      }
    });

    currentStepCentered = step;
  }

  function startAutoPlayCentered() {
    autoPlayIntervalCentered = setInterval(function() {
      const nextStep = currentStepCentered >= 3 ? 1 : currentStepCentered + 1;
      updateStepCentered(nextStep);
    }, 2000);
  }

  function stopAutoPlayCentered() {
    clearInterval(autoPlayIntervalCentered);
  }

  stepItemsCentered.forEach(function(item) {
    item.addEventListener('click', function() {
      const step = parseInt(this.getAttribute('data-step'));
      updateStepCentered(step);
      stopAutoPlayCentered();
      startAutoPlayCentered();
    });
  });

  if (stepItemsCentered.length > 0) {
    updateStepCentered(1);
    startAutoPlayCentered();
  }
});
