console.log("conn js success");

// เลือกดาวทั้งหมด
const stars = document.querySelectorAll('.star');
let isRated = false;

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
                    console.log(oldResponse);
                }
            })
            .catch(error => {
                console.error("Error fetching rating:", error);
            });
    } else {
        console.error("No data found in sessionStorage.");
    }
}

// วนลูปเพื่อเพิ่ม event listener ให้กับแต่ละดาว
stars.forEach((star) => {
    star.addEventListener('click', () => {
        if (!isRated) {
            // ลบ class 'selected' จากทุกดาว
            stars.forEach((s) => s.classList.remove('selected'));

            // เพิ่ม class 'selected' ให้กับดาวที่ถูกคลิกและดาวก่อนหน้า
            star.classList.add('selected');
            let value = star.getAttribute('data-value'); // ค่าของดาวที่ถูกคลิก

            for (let i = 0; i < value - 1; i++) {
                stars[i].classList.add('selected'); // เพิ่ม class ให้ดาวที่อยู่ก่อนหน้า
            }

            rate(value)
            isRated = true
        }
    });
});

document.getElementById('refresh-btn').addEventListener('click', () => {
    stars.forEach((s) => s.classList.remove('selected'));
    isRated = false
})