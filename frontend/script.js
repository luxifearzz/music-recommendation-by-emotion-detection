document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting the traditional way

    const fileInput = document.getElementById('fileInput');
    const languageSelect = document.getElementById('languageSelect'); // Get the selected language

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('language', languageSelect.value); // Append the selected language

    // Fetch the response from the backend API
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

            // Display description of the song
            document.getElementById('description').textContent = 'Description: ' + data.description;

            // Display cover image
            const coverImageElement = document.getElementById('coverImage');
            coverImageElement.src = data.cover_url;
            coverImageElement.style.display = 'block';

            // Display the song in the audio element
            const songElement = document.getElementById('song');
            songElement.src = data.song_url;
            songElement.style.display = 'block';

            // Display YouTube and Spotify links if available
            const youtubeLink = document.getElementById('youtubeLink');
            const spotifyLink = document.getElementById('spotifyLink');

            if (data.links.youtube) {
                youtubeLink.href = data.links.youtube;
                youtubeLink.textContent = "Listen on YouTube <" + data.links.youtube + ">";
                youtubeLink.style.display = 'block';
            } else {
                youtubeLink.style.display = 'none';
            }

            if (data.links.spotify) {
                spotifyLink.href = data.links.spotify;
                spotifyLink.textContent = "Listen on Spotify <" + data.links.spotify + ">";
                spotifyLink.style.display = 'block';
            } else {
                spotifyLink.style.display = 'none';
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error occurred while analyzing the emotion.');
    });
});
