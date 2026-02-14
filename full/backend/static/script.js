document.getElementById('detection-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const url = document.getElementById('url-input').value;
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    const resultText = document.getElementById('result-text');
    const probabilities = document.getElementById('probabilities');
    const errorText = document.getElementById('error-text');

    // Hide previous results/errors
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');

    try {
        // Send POST request to backend (relative URL now)
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to detect. Please try again.');
        }

        // Display result
        resultText.textContent = data.message;
        probabilities.textContent = `Phishing Probability: ${data.phishing_prob}% | Legitimate Probability: ${data.legit_prob}%`;
        resultDiv.classList.remove('hidden');
    } catch (error) {
        errorText.textContent = error.message;
        errorDiv.classList.remove('hidden');
    }
});