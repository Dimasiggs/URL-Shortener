document.getElementById('linkForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const urlInput = document.getElementById('urlInput');
    const url = urlInput.value;

    try {
        const response = await fetch('api', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
        });

        if (!response.ok) {
            throw new Error('Ошибка при сокращении ссылки');
        }

        const data = await response.json();
        displayResult(data.ShortenedUrl);
    } catch (error) {
        alert(error.message);
    }
});

function displayResult(ShortenedUrl) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `
        <h3>Сокращенная ссылка:</h3>
        <a href="${ShortenedUrl}" target="_blank">${ShortenedUrl}</a>
        `;
    resultDiv.style.display = 'block';
}
