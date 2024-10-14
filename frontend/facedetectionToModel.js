let video = document.getElementById("video");
let canvas = document.body.appendChild(document.createElement("canvas"));
let ctx = canvas.getContext("2d");
let displaySize;

let width = 480;
let height = 700;


let detectedFaceImage = null; // for collect detected face image

let videoContainer = document.createElement("div");
videoContainer.style.display = "flex";
videoContainer.style.flexDirection = "column";
videoContainer.style.alignItems = "center"; 

videoContainer.appendChild(video);
document.body.appendChild(videoContainer);

let predictBtn = document.createElement("button");
predictBtn.innerText = "FaceSays";
predictBtn.style.backgroundColor = "#567D8E"; 
predictBtn.style.color = "#fff"; 
predictBtn.style.border = "none"; 
predictBtn.style.borderRadius = "20px"; 
predictBtn.style.padding = "10px 20px"; 
predictBtn.style.fontSize = "16px"; 
predictBtn.style.cursor = "pointer"; 
predictBtn.style.marginTop = "5px"; 
predictBtn.style.zIndex = 1;
videoContainer.appendChild(predictBtn); 

// show result
let resultDiv = document.createElement("div");
resultDiv.id = "result";
resultDiv.style.position = "absolute"; 
resultDiv.style.top = "50%"; 
resultDiv.style.left = "50%"; 
resultDiv.style.transform = "translate(-50%, -50%)"; 
resultDiv.style.fontSize = "18px";
resultDiv.style.color = "#567D8E";
resultDiv.style.backgroundColor = "rgba(255, 255, 255, 0.8)";
resultDiv.style.padding = "10px";
resultDiv.style.borderRadius = "8px"; 
resultDiv.style.display = "none"; 
videoContainer.appendChild(resultDiv); 

// startStreamVideo
const startStream = () => {
    console.log("----- START STREAM ------");
    navigator.mediaDevices.getUserMedia({
        video: { width, height },
        audio: false
    }).then((stream) => { video.srcObject = stream });
}

// Load Model
console.log("----- START LOAD MODEL ------");
Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri('models'), // model for face detection
]).then(startStream).catch(err => console.error("Model loading error:", err));

// face detection
async function detect() {
    const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions());
    
    ctx.clearRect(0, 0, width, height);
    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    faceapi.draw.drawDetections(canvas, resizedDetections); // draw face detection area

    console.log(resizedDetections);

    if (resizedDetections.length > 0) {
        // cap detected face
        const box = resizedDetections[0].box; 
        captureFace(video, box);
        predictBtn.style.display = "inline-block"; 
    }
}

// cap detected face from video
function captureFace(video, box) {
    const faceCanvas = document.createElement('canvas');
    const faceCtx = faceCanvas.getContext('2d');
    const { x, y, width, height } = box;

    // setting canvas match with face size
    faceCanvas.width = width;
    faceCanvas.height = height;

    // draw face into canvas
    faceCtx.drawImage(video, x, y, width, height, 0, 0, width, height);

    // collect detected face image
    detectedFaceImage = faceCanvas.toDataURL('image/png');
}

// Convert dataURL to a Blob
function dataURLToBlob(dataURL) {
    const byteString = atob(dataURL.split(',')[1]); // Split dataURL to base64 string
    const mimeString = dataURL.split(',')[0].split(':')[1].split(';')[0]; // Get MIME type
    const arrayBuffer = new ArrayBuffer(byteString.length);
    const uint8Array = new Uint8Array(arrayBuffer);

    for (let i = 0; i < byteString.length; i++) {
        uint8Array[i] = byteString.charCodeAt(i);
    }

    return new Blob([uint8Array], { type: mimeString });
}

// Event handler for predict button
predictBtn.addEventListener('click', () => {    
    if (detectedFaceImage) {
        // Convert Data URL to Blob (image file)
        const faceImageBlob = dataURLToBlob(detectedFaceImage);

        // Create FormData and append image and language
        const formData = new FormData();
        formData.append('file', faceImageBlob, 'detected-face.png'); // File name is 'detected-face.png'
        formData.append('language', 'non-thai');  // หรือจะเปลี่ยนเป็น 'thai'

        // Send the FormData to the API
        fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultDiv.innerText = `Error: ${data.error}`;
                resultDiv.style.display = "block";
            } else {
                try {
                    // ลองบันทึกข้อมูลลงใน sessionStorage และตรวจสอบว่าบันทึกได้หรือไม่
                    window.sessionStorage.setItem('response', JSON.stringify(data));
                    
                    // แสดงผล emotion
                    const emotion = data.emotion ? data.emotion : "unknown emotion";
                    resultDiv.innerText = `You look ${emotion}`;
        
                    // เพิ่มลิงก์ Next >>
                    const nextLink = document.createElement("a");
                    nextLink.href = "opencard.html"; 
                    nextLink.innerText = "Next >>";
                    nextLink.style.display = "block"; 
                    nextLink.style.marginTop = "10px"; 
                    nextLink.style.textAlign = "center"; 
                    nextLink.style.color = "#567D8E"; 
        
                    resultDiv.appendChild(nextLink);
                    resultDiv.style.display = "block"; 
                } catch (error) {
                    console.error("Error storing in sessionStorage:", error);
                    resultDiv.innerText = "Error occurred while saving data.";
                    resultDiv.style.display = "block"; 
                }
            }
        })        
    } else {
        alert("ไม่มีใบหน้าที่ตรวจพบเพื่อจับภาพ");
    }
});

// if video start call face detection function
video.addEventListener('play', () => {
    displaySize = { width, height };
    faceapi.matchDimensions(canvas, displaySize);

    setInterval(detect, 500); 
});