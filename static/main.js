// Simple JavaScript version for local testing
document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Remove active class from all tabs and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });

    // Single Review Analysis functionality
    const reviewForm = document.getElementById('reviewForm');
    const reviewText = document.getElementById('reviewText');
    const placeName = document.getElementById('placeName');
    const starRating = document.getElementById('starRating');
    const businessType = document.getElementById('businessType');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultsDiv = document.getElementById('results');
    const errorDiv = document.getElementById('error');

    // CSV Dashboard functionality
    const csvFile = document.getElementById('csvFile');
    const uploadCsvBtn = document.getElementById('uploadCsvBtn');
    const csvError = document.getElementById('csvError');
    const csvLoading = document.getElementById('csvLoading');
    const csvDashboard = document.getElementById('csvDashboard');

    // Sample reviews for testing
    const sampleReviews = [
        "This product is amazing! I love it so much and would highly recommend it to everyone. Best purchase ever!",
        "The quality is decent for the price. Shipping was fast and packaging was good. Would consider buying again.",
        "Terrible product! Don't waste your money. Click here for better deals at amazing prices!",
        "I love my new phone, but this place is too noisy for working.",
        "Great service! The staff was friendly and the food was delicious.",
        "Never been to this place but I heard it's terrible. People say the service is awful."
    ];

    // Add sample review buttons to single review tab
    const singleReviewTab = document.getElementById('single-review');
    const sampleContainer = document.createElement('div');
    sampleContainer.innerHTML = '<h3>Sample Reviews (click to test):</h3>';
    sampleReviews.forEach((sample, index) => {
        const btn = document.createElement('button');
        btn.textContent = `Sample ${index + 1}`;
        btn.className = 'sample-btn';
        btn.onclick = () => {
            reviewText.value = sample;
        };
        sampleContainer.appendChild(btn);
    });
    reviewForm.parentNode.insertBefore(sampleContainer, reviewForm);

    // Single review analysis
    analyzeBtn.addEventListener('click', async function() {
        const text = reviewText.value.trim();
        if (!text) {
            showError('Please enter a review to analyze');
            return;
        }

        analyzeBtn.disabled = true;
        analyzeBtn.textContent = 'Analyzing...';
        hideError();
        hideResults();

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    place_name: placeName.value,
                    star_rating: starRating.value ? parseInt(starRating.value) : null,
                    business_type: businessType.value
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            showResults(result);
        } catch (error) {
            console.error('Error:', error);
            showError('Failed to analyze review. Please try again.');
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = 'Analyze Review';
        }
    });

    // CSV upload and dashboard generation
    uploadCsvBtn.addEventListener('click', async function() {
        const file = csvFile.files[0];
        if (!file) {
            showCsvError('Please select a CSV file to upload');
            return;
        }

        if (!file.name.toLowerCase().endsWith('.csv')) {
            showCsvError('Please select a valid CSV file');
            return;
        }

        uploadCsvBtn.disabled = true;
        uploadCsvBtn.textContent = 'Processing...';
        hideCsvError();
        hideCsvDashboard();
        showCsvLoading();

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('/api/upload-csv', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            hideCsvLoading();
            showCsvDashboard(result);
        } catch (error) {
            console.error('Error:', error);
            hideCsvLoading();
            showCsvError(`Failed to process CSV file: ${error.message}`);
        } finally {
            uploadCsvBtn.disabled = false;
            uploadCsvBtn.textContent = 'Generate Dashboard';
        }
    });

    // Helper functions for single review analysis
    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }

    function hideError() {
        errorDiv.style.display = 'none';
    }

    function showResults(result) {
        const statusClass = result.legitimate ? 'legitimate' : 'illegitimate';
        const statusText = result.legitimate ? 'Legitimate' : 'Potentially Problematic';
        
        resultsDiv.innerHTML = `
            <div class="result-card ${statusClass}">
                <h3>Analysis Result: ${statusText}</h3>
                <p><strong>Status:</strong> ${result.status}</p>
                <p><strong>Confidence:</strong> ${(result.confidence * 100).toFixed(1)}%</p>
                <p><strong>Sentiment:</strong> ${result.analysis.sentiment}</p>
                
                ${result.analysis.policy_violations.length > 0 ? `
                    <div class="violations">
                        <h4>Policy Violations:</h4>
                        <ul>
                            ${result.analysis.policy_violations.map(v => `<li><strong>${v.type}:</strong> ${v.description}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                <div class="text-features">
                    <h4>Text Analysis:</h4>
                    <p>Length: ${result.analysis.text_features.length} characters</p>
                    <p>Word Count: ${result.analysis.text_features.word_count}</p>
                    <p>Readability: ${result.analysis.text_features.readability}</p>
                </div>
                
                ${result.analysis.recommendations.length > 0 ? `
                    <div class="recommendations">
                        <h4>Recommendations:</h4>
                        <ul>
                            ${result.analysis.recommendations.map(r => `<li>${r}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        `;
        resultsDiv.style.display = 'block';
    }

    function hideResults() {
        resultsDiv.style.display = 'none';
    }

    // Helper functions for CSV dashboard
    function showCsvError(message) {
        csvError.textContent = message;
        csvError.style.display = 'block';
    }

    function hideCsvError() {
        csvError.style.display = 'none';
    }

    function showCsvLoading() {
        csvLoading.style.display = 'block';
    }

    function hideCsvLoading() {
        csvLoading.style.display = 'none';
    }

    function showCsvDashboard(data) {
        const dashboard = data.dashboard;
        const metadata = data.metadata;

        let dashboardHTML = `
            <div class="dashboard-header">
                <h2>CSV Analysis Dashboard</h2>
                <p>File: ${metadata.file_name} | Total Reviews: ${metadata.total_reviews} | Processed: ${new Date(metadata.processed_at).toLocaleString()}</p>
            </div>
            <div class="dashboard-content">
        `;

        // Overall Statistics
        if (dashboard.overall_stats) {
            dashboardHTML += `
                <div class="dashboard-section">
                    <h3>📊 Overall Statistics</h3>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-value">${dashboard.overall_stats.total_reviews}</div>
                            <div class="stat-label">Total Reviews</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${dashboard.overall_stats.total_companies}</div>
                            <div class="stat-label">Companies</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${dashboard.overall_stats.total_authors}</div>
                            <div class="stat-label">Authors</div>
                        </div>
                    </div>
                </div>
            `;
        }

        // Rating Analysis
        if (dashboard.ratings) {
            dashboardHTML += `
                <div class="dashboard-section">
                    <h3>⭐ Rating Analysis</h3>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-value">${dashboard.ratings.statistics?.mean || 'N/A'}</div>
                            <div class="stat-label">Average Rating</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${dashboard.ratings.categories?.excellent || 0}</div>
                            <div class="stat-label">Excellent (4.5+)</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${dashboard.ratings.categories?.good || 0}</div>
                            <div class="stat-label">Good (3.5-4.4)</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${dashboard.ratings.categories?.poor || 0}</div>
                            <div class="stat-label">Poor (<2.5)</div>
                        </div>
                    </div>
                </div>
            `;
        }

        // Company Analysis
        if (dashboard.companies) {
            dashboardHTML += `
                <div class="dashboard-section">
                    <h3>🏢 Top Companies</h3>
                    <div class="company-list">
            `;
            
            Object.entries(dashboard.companies.average_ratings || {}).slice(0, 6).forEach(([company, stats]) => {
                const stars = '★'.repeat(Math.round(stats.mean));
                dashboardHTML += `
                    <div class="company-card">
                        <div class="company-name">${company}</div>
                        <div class="company-stats">
                            Average: ${stats.mean} <span class="rating-stars">${stars}</span><br>
                            Reviews: ${stats.count}
                        </div>
                    </div>
                `;
            });
            
            dashboardHTML += `
                    </div>
                </div>
            `;
        }

        // Classification Analysis
        if (dashboard.classifications) {
            dashboardHTML += `
                <div class="dashboard-section">
                    <h3>🔍 Review Classifications</h3>
                    <div class="stats-grid">
            `;
            
            Object.entries(dashboard.classifications.distribution || {}).forEach(([classification, count]) => {
                const percentage = dashboard.classifications.percentages[classification] || 0;
                dashboardHTML += `
                    <div class="stat-card">
                        <div class="stat-value">${count}</div>
                        <div class="stat-label">${classification.replace('_', ' ')} (${percentage}%)</div>
                    </div>
                `;
            });
            
            dashboardHTML += `
                    </div>
                </div>
            `;
        }

        // Sample Reviews
        if (dashboard.sample_reviews) {
            dashboardHTML += `
                <div class="dashboard-section">
                    <h3>📝 Sample Reviews</h3>
                    <div class="sample-reviews">
            `;
            
            Object.entries(dashboard.sample_reviews).forEach(([classification, reviews]) => {
                reviews.forEach(review => {
                    const stars = review.rating !== 'N/A' ? '★'.repeat(Math.round(review.rating)) : '';
                    dashboardHTML += `
                        <div class="review-card ${classification}">
                            <div class="review-header">
                                <span class="review-author">${review.author}</span>
                                <span class="review-rating">${stars}</span>
                            </div>
                            <div class="review-text">${review.text}</div>
                            <div class="review-company">${review.company} • ${classification.replace('_', ' ')}</div>
                        </div>
                    `;
                });
            });
            
            dashboardHTML += `
                    </div>
                </div>
            `;
        }

        dashboardHTML += `</div>`;
        
        csvDashboard.innerHTML = dashboardHTML;
        csvDashboard.style.display = 'block';
    }

    function hideCsvDashboard() {
        csvDashboard.style.display = 'none';
    }
});

