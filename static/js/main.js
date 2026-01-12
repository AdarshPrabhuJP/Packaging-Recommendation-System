let costChart = null;
let co2Chart = null;

document.getElementById('fragility').addEventListener('input', function (e) {
    document.getElementById('fragilityValue').textContent = e.target.value;
});

document.getElementById('productForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const productData = {
        product_weight: parseInt(document.getElementById('weight').value),
        product_fragility: parseInt(document.getElementById('fragility').value),
        shipping_distance: parseInt(document.getElementById('distance').value),
        priority: document.getElementById('priority').value,
        top_n: 5
    };

    showLoading();
    hideError();

    try {
        const result = await getRecommendations(productData);
        displayRecommendations(result.recommendations);
        createCharts(result.recommendations);
    } catch (error) {
        showError('Failed to get recommendations. Please try again.');
        console.error(error);
    } finally {
        hideLoading();
    }
});

function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('results').style.display = 'block';
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

function hideError() {
    document.getElementById('error').style.display = 'none';
}

function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendationsList');
    container.innerHTML = '';

    recommendations.forEach(rec => {
        const card = document.createElement('div');
        card.className = 'recommendation-card';

        card.innerHTML = `
            <div class="rank-badge">${rec.rank}</div>
            <div class="material-name">${rec.material}</div>
            <div class="metrics-row">
                <div class="metric">
                    <div class="metric-label">Predicted Cost</div>
                    <div class="metric-value">₹${rec.predicted_cost.toFixed(2)}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">CO₂ Footprint</div>
                    <div class="metric-value">${rec.predicted_co2.toFixed(3)} kg</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Score</div>
                    <div class="metric-value">${(rec.score * 100).toFixed(1)}%</div>
                </div>
            </div>
            <div class="tags">
                ${rec.recyclable ? '<span class="tag recyclable">Recyclable</span>' : ''}
                <span class="tag">Durability: ${rec.durability}/10</span>
                <span class="tag">Biodegradability: ${rec.biodegradability}/10</span>
            </div>
        `;

        container.appendChild(card);
    });
}

function createCharts(recommendations) {
    const labels = recommendations.map(r => r.material);
    const costs = recommendations.map(r => r.predicted_cost);
    const co2 = recommendations.map(r => r.predicted_co2);

    if (costChart) {
        costChart.destroy();
    }
    if (co2Chart) {
        co2Chart.destroy();
    }

    const costCtx = document.getElementById('costChart').getContext('2d');
    costChart = new Chart(costCtx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Predicted Cost (₹)',
                data: costs,
                backgroundColor: 'rgba(13, 110, 253, 0.6)',
                borderColor: 'rgba(13, 110, 253, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const co2Ctx = document.getElementById('co2Chart').getContext('2d');
    co2Chart = new Chart(co2Ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'CO₂ Footprint (kg)',
                data: co2,
                backgroundColor: 'rgba(25, 135, 84, 0.6)',
                borderColor: 'rgba(25, 135, 84, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

async function loadAllMaterials() {
    try {
        const result = await getAllMaterials();
        const tbody = document.getElementById('materialsTableBody');
        tbody.innerHTML = '';

        result.materials.forEach(material => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${material.material_type}</td>
                <td>₹${material.cost_per_unit.toFixed(2)}</td>
                <td>${material.co2_footprint.toFixed(3)}</td>
                <td>${material.durability_score}/10</td>
                <td>${material.recyclable ? '<span class="badge bg-success">Yes</span>' : '<span class="badge bg-secondary">No</span>'}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Failed to load materials:', error);
    }
}

loadAllMaterials();
