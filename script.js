// Configure MathJax
window.MathJax = {
    tex: {
        inlineMath: [['\\(', '\\)']],
        displayMath: [['\\[', '\\]']],
        processEscapes: true,
        processEnvironments: true
    },
    options: {
        skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
    }
};

// Update last modified date
document.addEventListener('DOMContentLoaded', function() {
    const lastUpdated = document.getElementById('last-updated');
    if (lastUpdated) {
        lastUpdated.textContent = new Date().toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
    
    // Add smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Add interactive prime gap visualization (placeholder for future)
    createPrimeGapVisualization();
    
    // Add section for dynamically adding new discoveries
    setupDynamicContent();
});

// Placeholder for prime gap visualization
function createPrimeGapVisualization() {
    // This will be implemented to show an interactive graph of prime gaps
    console.log('Prime gap visualization placeholder loaded');
}

// Setup for dynamically adding new content
function setupDynamicContent() {
    // Create a container for future discoveries
    const futureWork = document.getElementById('future-work');
    if (futureWork) {
        const addButton = document.createElement('button');
        addButton.textContent = 'Check for Updates';
        addButton.style.cssText = `
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            margin-top: 1rem;
        `;
        addButton.addEventListener('click', checkForUpdates);
        futureWork.appendChild(addButton);
    }
}

// Placeholder for checking updates
function checkForUpdates() {
    alert('This feature will check for new prime discoveries in future updates!');
}

// Function to add a new discovery section (for future use)
function addNewDiscovery(title, content, date) {
    const main = document.querySelector('main');
    const futureWork = document.getElementById('future-work');
    
    const newSection = document.createElement('section');
    newSection.className = 'new-discovery';
    newSection.innerHTML = `
        <h2>${title}</h2>
        <div class="discovery-date">Discovered: ${date}</div>
        <div class="discovery-content">${content}</div>
    `;
    
    main.insertBefore(newSection, futureWork);
    
    // Re-render MathJax for new content
    if (window.MathJax) {
        MathJax.typesetPromise([newSection]).catch((e) => console.error(e));
    }
}

// Export functions for potential use in adding new content
window.primeDiscoveries = {
    addNewDiscovery: addNewDiscovery,
    updateLastModified: function() {
        const lastUpdated = document.getElementById('last-updated');
        if (lastUpdated) {
            lastUpdated.textContent = new Date().toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        }
    }
};