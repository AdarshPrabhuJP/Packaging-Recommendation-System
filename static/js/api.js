const API_BASE_URL = 'http://localhost:5000/api';

async function getRecommendations(productData) {
    const response = await fetch(`${API_BASE_URL}/recommend`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(productData)
    });

    if (!response.ok) {
        throw new Error('Failed to get recommendations');
    }

    return await response.json();
}

async function getAllMaterials() {
    const response = await fetch(`${API_BASE_URL}/materials`);

    if (!response.ok) {
        throw new Error('Failed to fetch materials');
    }

    return await response.json();
}
