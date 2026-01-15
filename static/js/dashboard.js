let co2Chart, costChart, materialPieChart, sustainabilityChart;

async function loadDashboardData() {
    try {
        const response = await fetch('http://localhost:5000/api/dashboard-data');
        const result = await response.json();

        if (result.status === 'success') {
            updateMetrics(result.key_metrics);
            renderCO2Chart(result.co2_reduction);
            renderCostChart(result.cost_savings);
            renderMaterialPieChart(result.material_trends);
            renderSustainabilityChart(result.sustainability_metrics);
        }
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

function updateMetrics(metrics) {
    document.getElementById('totalMaterials').textContent = metrics.total_materials;
    document.getElementById('co2Saved').textContent = metrics.co2_saved_percent.toFixed(1) + '%';
    document.getElementById('costSaved').textContent = '₹' + metrics.cost_saved.toFixed(2);
    document.getElementById('ecoPercent').textContent = metrics.eco_friendly_percent + '%';
}

function renderCO2Chart(data) {
    const ctx = document.getElementById('co2Chart').getContext('2d');

    if (co2Chart) co2Chart.destroy();

    co2Chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Baseline CO₂', 'Eco Materials CO₂'],
            datasets: [{
                label: 'CO₂ Footprint (kg)',
                data: [data.baseline_co2, data.eco_co2],
                backgroundColor: ['#dc3545', '#28a745'],
                borderColor: ['#c82333', '#218838'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: `Reduction: ${data.reduction_percent.toFixed(1)}%`
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'CO₂ (kg)'
                    }
                }
            }
        }
    });
}

function renderCostChart(data) {
    const ctx = document.getElementById('costChart').getContext('2d');

    if (costChart) costChart.destroy();

    costChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Baseline Cost', 'Budget Cost'],
            datasets: [{
                label: 'Cost (₹)',
                data: [data.baseline_cost, data.budget_cost],
                backgroundColor: ['#ffc107', '#0d6efd'],
                borderColor: ['#e0a800', '#0b5ed7'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: `Savings: ${data.savings_percent.toFixed(1)}%`
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Cost (₹)'
                    }
                }
            }
        }
    });
}

function renderMaterialPieChart(data) {
    const ctx = document.getElementById('materialPieChart').getContext('2d');

    if (materialPieChart) materialPieChart.destroy();

    const labels = Object.keys(data);
    const values = Object.values(data);

    materialPieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    '#28a745',
                    '#0d6efd',
                    '#ffc107',
                    '#17a2b8',
                    '#6c757d'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function renderSustainabilityChart(data) {
    const ctx = document.getElementById('sustainabilityChart').getContext('2d');

    if (sustainabilityChart) sustainabilityChart.destroy();

    const labels = Object.keys(data);
    const values = Object.values(data);

    sustainabilityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Materials',
                data: values,
                backgroundColor: '#28a745',
                borderColor: '#218838',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    },
                    title: {
                        display: true,
                        text: 'Count'
                    }
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', loadDashboardData);
