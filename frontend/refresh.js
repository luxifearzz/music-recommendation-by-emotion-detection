function rate(val) {
    const resData = window.sessionStorage.getItem('response')
    if (resData) {
        const data = JSON.parse(resData)
        // เรียก API /new-song โดยส่งข้อมูลที่จำเป็น (id, emotion, language)
        fetch('http://127.0.0.1:5000/rate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id: data.id,
                rating: val,
                emotion: data.emotion,
                language: data.language
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error(data.error);
                } else {
                    const oldResponse = JSON.parse(window.sessionStorage.getItem('response'));
                    oldResponse.rating = data.new_rating
                    oldResponse.total_ratings = data.total_ratings
                    window.sessionStorage.setItem('response', JSON.stringify(oldResponse))
                }
            })
            .catch(error => {
                console.error("Error fetching rating:", error);
            });
    } else {
        console.error("No data found in sessionStorage.");
    }
}

function showData() {
    const data = JSON.parse(window.sessionStorage.getItem('response'))

    document.getElementById('coverImage').src = data.cover_url
    document.getElementById('lyrics').textContent = data.description
    document.getElementById('song').src = data.song_url
    document.getElementById('music-name').textContent = data.name
    document.getElementById('spotifyLink').href = data.links.spotify
    document.getElementById('youtubeLink').href = data.links.youtube
}

showData()

document.getElementById('refresh-btn').addEventListener('click', () => {
    const data = JSON.parse(window.sessionStorage.getItem('response'));
    if (data) {
        // เรียก API /new-song โดยส่งข้อมูลที่จำเป็น (id, emotion, language)
        fetch('http://127.0.0.1:5000/new-song', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id: data.id,
                emotion: data.emotion,
                language: data.language
            })
        })
            .then(response => response.json())
            .then(newSongData => {
                if (newSongData.error) {
                    console.error(newSongData.error);
                } else {
                    window.sessionStorage.setItem('response', JSON.stringify(newSongData));
                    showData();  // เรียก showData() ที่นี่เพื่อแสดงข้อมูลใหม่ทันที
                }
            })
            .catch(error => {
                console.error("Error fetching new song:", error);
            });
    } else {
        console.error("No data found in sessionStorage.");
    }
});