// เลือกดาวทั้งหมด
const stars = document.querySelectorAll('.star');

// วนลูปเพื่อเพิ่ม event listener ให้กับแต่ละดาว
stars.forEach((star) => {
    star.addEventListener('click', () => {
        // ลบ class 'selected' จากทุกดาว
        stars.forEach((s) => s.classList.remove('selected'));
        
        // เพิ่ม class 'selected' ให้กับดาวที่ถูกคลิกและดาวก่อนหน้า
        star.classList.add('selected');
        let value = star.getAttribute('data-value'); // ค่าของดาวที่ถูกคลิก
        
        for (let i = 0; i < value - 1; i++) {
            stars[i].classList.add('selected'); // เพิ่ม class ให้ดาวที่อยู่ก่อนหน้า
        }
    });
});