let video = document.getElementById("video");
let canvas = document.body.appendChild(document.createElement("canvas"));
let ctx = canvas.getContext("2d");
let displaySize;

let width = 480;
let height = 700;

let detectedFaceImage = null; // เก็บภาพใบหน้าที่ตรวจจับได้

// ปุ่มดาวน์โหลด
let downloadBtn = document.body.appendChild(document.createElement("button"));
downloadBtn.innerText = "Download Captured Face";
downloadBtn.style.display = "none"; // ซ่อนปุ่มไว้จนกว่าจะตรวจจับใบหน้าได้

// เริ่มสตรีมวิดีโอ
const startStream = () => {
    console.log("----- START STREAM ------");
    navigator.mediaDevices.getUserMedia({
        video: { width, height },
        audio: false
    }).then((stream) => { video.srcObject = stream });
}

// โหลดโมเดล
console.log("----- START LOAD MODEL ------");
Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri('models'), // ใช้โมเดลสำหรับการตรวจจับใบหน้า
]).then(startStream);

// ฟังก์ชันตรวจจับใบหน้า
async function detect() {
    const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()); // ใช้ TinyFaceDetectorOptions หรือ SSD options
    
    ctx.clearRect(0, 0, width, height);
    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    faceapi.draw.drawDetections(canvas, resizedDetections); // วาดกรอบสี่เหลี่ยมรอบใบหน้า

    console.log(resizedDetections);

    if (resizedDetections.length > 0) {
        // จับภาพใบหน้าที่ตรวจจับได้
        const box = resizedDetections[0].box; // ใช้ใบหน้าที่ตรวจพบแรกสุด
        captureFace(video, box);
        downloadBtn.style.display = "inline-block"; // แสดงปุ่มดาวน์โหลดเมื่อมีการตรวจจับใบหน้า
    } else {
        downloadBtn.style.display = "none"; // ซ่อนปุ่มถ้าไม่เจอใบหน้า
    }
}

// ฟังก์ชันจับภาพใบหน้าจากวิดีโอ
function captureFace(video, box) {
    const faceCanvas = document.createElement('canvas');
    const faceCtx = faceCanvas.getContext('2d');
    const { x, y, width, height } = box;

    // ตั้งค่าขนาดแคนวาสให้ตรงกับขนาดใบหน้า
    faceCanvas.width = width;
    faceCanvas.height = height;

    // วาดบริเวณใบหน้าลงบนแคนวาส
    faceCtx.drawImage(video, x, y, width, height, 0, 0, width, height);

    // เก็บภาพใบหน้าที่จับได้เป็น base64
    detectedFaceImage = faceCanvas.toDataURL('image/png');
}

// จัดการการคลิกปุ่มดาวน์โหลด
downloadBtn.addEventListener('click', () => {
    if (detectedFaceImage) {
        const link = document.createElement('a');
        link.href = detectedFaceImage;
        link.download = 'captured_face.png';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } else {
        alert("ไม่มีใบหน้าที่ตรวจพบเพื่อจับภาพ");
    }
});

// เมื่อวิดีโอเริ่มเล่น เรียกใช้ฟังก์ชันตรวจจับใบหน้า
video.addEventListener('play', () => {
    displaySize = { width, height };
    faceapi.matchDimensions(canvas, displaySize);

    setInterval(detect, 100); // เรียกใช้ฟังก์ชัน detect ทุก 100 มิลลิวินาที
});
