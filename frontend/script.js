document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting the traditional way

    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('http://127.0.0.1:5000/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            // Display emotion
            document.getElementById('emotion').textContent = 'Emotion: ' + data.emotion;

            // Display cover image
            const coverImageElement = document.getElementById('coverImage');
            coverImageElement.src = data.cover_url;
            coverImageElement.style.display = 'block';

            // Display song
            const songElement = document.getElementById('song');
            songElement.src = data.song_url;
            songElement.style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
