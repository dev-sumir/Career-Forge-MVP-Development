// --- Define the connection to your backend API ---
const API_URL = 'http://127.0.0.1:8000/api/v1/hackrx/run';

// --- Get references to all necessary DOM elements ---
const [uploadView, dashboardView, questsView] = [document.getElementById('upload-view'), document.getElementById('dashboard-view'), document.getElementById('quests-view')];
const [analyzeBtn, fileInput, statusEl, dropZone, dropZoneText, loader] = [document.getElementById('analyzeBtn'), document.getElementById('resumeFile'), document.getElementById('status'), document.getElementById('dropZone'), document.getElementById('dropZoneText'), document.getElementById('loader')];
let selectedFile = null;
let radarChart = null; // To store Chart.js instance for destruction/recreation
let currentQuests = []; // To store quests for display

// --- Core UI Functions ---
function showView(viewToShow) {
    // Hide all main views first
    [uploadView, dashboardView, questsView].forEach(view => {
        if (view) view.style.display = 'none';
    });
    // Show the requested view with a fade-in animation
    if (viewToShow) {
        viewToShow.style.display = 'block';
        viewToShow.classList.add('fade-in');
    }
}

function handleFileSelect(files) {
    if (files.length > 0) {
        selectedFile = files[0];
        dropZoneText.textContent = `File selected: ${selectedFile.name}`;
        analyzeBtn.disabled = false; // Enable the analyze button
        statusEl.textContent = ''; // Clear any previous status message
        statusEl.classList.remove('error', 'success'); // Clear status classes
    }
}

// --- Event Listeners for Upload View ---
dropZone.addEventListener('click', () => fileInput.click()); // Clicking the div now opens the file dialog
fileInput.addEventListener('change', () => handleFileSelect(fileInput.files));

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('hover'); // Add hover class for styling
});
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('hover'));
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('hover');
    if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files; // Assign dropped files to input
        handleFileSelect(e.dataTransfer.files);
    }
});

analyzeBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        statusEl.textContent = '❌ Please select a file first.';
        statusEl.classList.add('error');
        return;
    }

    statusEl.textContent = '';
    statusEl.classList.remove('error', 'success');
    loader.style.display = 'block'; // Show loader
    analyzeBtn.disabled = true; // Disable button during analysis

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Backend response:", data); // For debugging

        // Store quests globally if they exist
        currentQuests = data.quests || [];

        displayDashboard(data); // Render the dashboard with received data
        displayQuests(currentQuests); // Render the quests view
        showView(dashboardView); // Switch to dashboard view

    } catch (error) {
        console.error('Error during analysis:', error);
        statusEl.textContent = `❌ Error: ${error.message}`;
        statusEl.classList.add('error');
        showView(uploadView); // Stay on upload view if error
    } finally {
        loader.style.display = 'none'; // Hide loader
        analyzeBtn.disabled = false; // Re-enable button
    }
});


// --- Display Functions (to render data into HTML) ---
function displayDashboard(data) {
    const { profile, experiences = [], summary = "No summary generated." } = data;

    // Group skills by category for display
    const skillsByCategory = (profile.skills || []).reduce((acc, skill) => {
        (acc[skill.category] = acc[skill.category] || []).push(skill.name);
        return acc;
    }, {});

    // Prepare scores for the radar chart (using skill count for now)
    const scores = {
        TechnicalSkills: skillsByCategory['TechnicalSkills']?.length || 0,
        SoftSkills: skillsByCategory['SoftSkills']?.length || 0,
        Intelligence: skillsByCategory['Intelligence']?.length || 0,
        // Using number of experiences as a proxy for experience score
        Experience: experiences.length,
    };

    // Build the entire dashboard HTML dynamically based on your layout drawing
    dashboardView.innerHTML = `
        <div class="dashboard-container">
            <div class="grid-header"><h1>CAREER FORGE</h1><p>PROFILE</p></div>
            <div class="grid-name grid-item"><h2>${profile.user_name || 'User Name'}</h2><p>${profile.job_title || 'Job Title'}</p></div>
            <div class="grid-rank grid-item"><h2>RANK</h2><p><span>${profile.main_rank || 'N/A'}</span> (LEVEL ${profile.level || 0})</p></div>
            <div class="grid-summary grid-item"><h2>SUMMARY</h2><div class="section-content"><p>${summary}</p></div></div>
            <div class="grid-experience grid-item"><h2>EXPERIENCE</h2><div class="section-content" id="experience-list"></div></div>
            <div class="grid-skills grid-item"><h2>SKILLS</h2><div class="section-content" id="skills-list"></div></div>
            <div class="grid-graph-quests">
                <div class="grid-graph grid-item"><h3>GRAPH</h3><canvas id="radarChart"></canvas></div>
                <div class="grid-quests grid-item"><button id="viewQuestsBtn">QUESTS</button></div>
            </div>
        </div>`;

    // Populate Experience List
    const experienceListEl = document.getElementById('experience-list');
    if (experienceListEl) {
        experienceListEl.innerHTML = experiences.length > 0 ? experiences.map(exp => `
            <div class="experience-item">
                <h3>${exp.title || 'Untitled'} <small>(${exp.category || 'General'})</small></h3>
                <p><em>${exp.organization || 'N/A'}</em></p>
                <p>${exp.description || 'No description provided.'}</p>
            </div>`).join('') : '<p>No specific experiences found.</p>';
    }

    // Populate Skills List
    const skillsListEl = document.getElementById('skills-list');
    if (skillsListEl) {
        let skillsHtml = '';
        if (Object.keys(skillsByCategory).length > 0) {
            for (const category in skillsByCategory) {
                // Format category names nicely (e.g., 'TechnicalSkills' -> 'Technical Skills')
                const formattedCategory = category.replace(/([A-Z])/g, ' $1').trim();
                skillsHtml += `<div class="skill-category"><h3>${formattedCategory}</h3><ul class="skill-list">${skillsByCategory[category].map(skillName => `<li class="skill-item">${skillName}</li>`).join('')}</ul></div>`;
            }
        } else {
            skillsHtml = '<p>No specific skills found.</p>';
        }
        skillsListEl.innerHTML = skillsHtml;
    }


    // Re-bind the "QUESTS" button event listener (since dashboard HTML was re-written)
    const viewQuestsBtn = document.getElementById('viewQuestsBtn');
    if (viewQuestsBtn) {
        viewQuestsBtn.addEventListener('click', () => showView(questsView));
    }

    // Create the radar chart
    createRadarChart(scores);
}

function displayQuests(quests) {
    questsView.innerHTML = `
        <div class="quests-header">
            <h2>YOUR QUESTS</h2>
            <button id="backToProfileBtn">BACK TO PROFILE</button>
        </div>
        <div id="quests-content" class="section-content" style="max-height: 70vh;"></div>`; // Max height for scrollable quests

    const questsContentEl = document.getElementById('quests-content');
    if (questsContentEl) {
        if (quests.length > 0) {
            questsContentEl.innerHTML = quests.map(quest => `
                <div class="quest-item">
                    <h3>${quest.title}</h3>
                    <p>${quest.description}</p>
                    <small><b>Rewards:</b> ${quest.rewards.join(', ')}</small>
                </div>`).join('');
        } else {
            questsContentEl.innerHTML = '<p>No quests generated at this time. Keep improving your profile!</p>';
        }
    }

    // Re-bind the "BACK TO PROFILE" button event listener
    const backToProfileBtn = document.getElementById('backToProfileBtn');
    if (backToProfileBtn) {
        backToProfileBtn.addEventListener('click', () => showView(dashboardView));
    }
}


function createRadarChart(scores) {
    const ctx = document.getElementById('radarChart')?.getContext('2d');
    if (!ctx) {
        console.warn("Radar chart canvas not found.");
        return;
    }

    // Destroy existing chart instance if it exists to prevent overlap/memory leaks
    if (radarChart) {
        radarChart.destroy();
    }

    const data = {
        labels: ['Technical', 'Soft Skills', 'Intelligence', 'Experience'],
        datasets: [{
            label: 'Your Profile',
            data: [
                scores.TechnicalSkills,
                scores.SoftSkills,
                scores.Intelligence,
                scores.Experience
            ],
            backgroundColor: 'rgba(142, 68, 173, 0.4)', // Primary glow purple with transparency
            borderColor: 'rgba(224, 176, 255, 1)', // Secondary glow light purple
            borderWidth: 2,
            pointBackgroundColor: 'rgba(224, 176, 255, 1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(224, 176, 255, 1)'
        }]
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false, // Allows chart to fill parent container
        plugins: {
            legend: {
                display: false // We don't need a legend for a single dataset
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return `${context.label}: ${context.raw}`;
                    }
                }
            }
        },
        scales: {
            r: {
                angleLines: {
                    color: 'rgba(255, 255, 255, 0.2)' // Light grid lines
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.2)'
                },
                pointLabels: {
                    color: 'rgba(224, 176, 255, 1)', // Light purple labels
                    font: {
                        size: 12,
                        family: 'Orbitron, sans-serif' // Futuristic font for labels
                    }
                },
                ticks: {
                    display: false, // Hide the numerical ticks
                    beginAtZero: true,
                    max: Math.max(10, ...Object.values(scores)) + 2 // Dynamically adjust max for better visual scaling
                },
                min: 0
            }
        }
    };

    radarChart = new Chart(ctx, {
        type: 'radar',
        data: data,
        options: options,
    });
}


// --- Initial Setup ---
// Initially show the upload view when the page loads
document.addEventListener('DOMContentLoaded', () => {
    showView(uploadView);
});