let video = document.getElementById("video");
let canvas = document.body.appendChild(document.createElement("canvas"));
let ctx = canvas.getContext("2d");
let displaySize;

let width = 1280;
let height = 720;

// let width = 480;
// let height = 700;

const startStream = () => {
    console.log("----- START STREAM ------");
    navigator.mediaDevices.getUserMedia({
        video: {width, height},
        audio: false
    }).then((stream) => {video.srcObject = stream});
}

console.log("----- START LOAD MODEL ------");
Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri('models'), // ใช้โมเดลสำหรับการตรวจจับใบหน้า
    // หรือใช้ faceapi.nets.ssdMobilenetv1.loadFromUri('models') แทน
]).then(startStream);

async function detect() {
    const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()); // ใช้ TinyFaceDetectorOptions หรือ SSD options
    
    ctx.clearRect(0, 0, width, height);
    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    faceapi.draw.drawDetections(canvas, resizedDetections); // วาดกรอบสี่เหลี่ยมรอบใบหน้า
    
    console.log(resizedDetections);
}

video.addEventListener('play', () => {
    displaySize = { width, height };
    faceapi.matchDimensions(canvas, displaySize);

    setInterval(detect, 100); // เรียกใช้ฟังก์ชัน detect ทุก 100 มิลลิวินาที
});
