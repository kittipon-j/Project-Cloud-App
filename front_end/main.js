// ฟังก์ชันสำหรับแสดง section ที่เลือก
function showSection(sectionId) {
    // ซ่อนทุก section
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.style.display = 'none';
    });

    // แสดง section ที่เลือก
    const activeSection = document.getElementById(sectionId);
    if (activeSection) {
        activeSection.style.display = 'block';
    }
}

// ฟังก์ชันสำหรับเปิดตัวเลือกไฟล์
function uploadImage(inputNumber) {
    const input = document.getElementById(`imageInput${inputNumber}`);
    if (input) {
        input.click();
    }
}

// ฟังก์ชันสำหรับแสดงภาพตัวอย่าง
function previewImage(event, inputNumber) {
    const file = event.target.files[0];
    if (!file) return;

    // Add file type validation
    if (!file.type.startsWith('image/')) {
        alert('กรุณาเลือกไฟล์รูปภาพ');
        return;
    }

    // Add file size validation (e.g., 5MB limit)
    if (file.size > 5 * 1024 * 1024) {
        alert('ขนาดไฟล์ต้องไม่เกิน 5MB');
        return;
    }

    const reader = new FileReader();
    reader.onload = function() {
        const preview = document.getElementById(`preview${inputNumber}`);
        const fileBox = document.getElementById(`fileBox${inputNumber}`);
        const selectButton = fileBox.querySelector('button');
        
        if (preview) {
            preview.src = reader.result;
            preview.style.display = 'block';
        }
        
        // ซ่อนปุ่มเลือกไฟล์
        if (selectButton) {
            selectButton.style.display = 'none';
        }
    }
    reader.onerror = function() {
        alert('Error reading file');
    }
    reader.readAsDataURL(file);
}


// ฟังก์ชันสำหรับแสดงวิดีโอตัวอย่างและซ่อนปุ่ม "Select Video"
function previewVideo(event, boxNumber) {
    const file = event.target.files[0];
    if (!file) return;

    // Add file type validation
    if (!file.type.startsWith('video/')) {
        alert('กรุณาเลือกไฟล์วิดีโอ');
        return;
    }

    // Add file size validation (e.g., 30MB limit)
    if (file.size > 30 * 1024 * 1024) {
        alert('ขนาดไฟล์ต้องไม่เกิน 30MB');
        return;
    }

    const preview = document.getElementById(`preview${boxNumber}`);
    const fileBox = document.getElementById(`fileBox${boxNumber}`);
    const selectButton = fileBox.querySelector('button');
    
    if (preview) {
        const videoURL = URL.createObjectURL(file);
        preview.src = videoURL;
        preview.style.display = 'block';
        
        // เพิ่ม event listener เพื่อล้าง URL object เมื่อไม่ได้ใช้งานแล้ว
        preview.onloadedmetadata = function() {
            URL.revokeObjectURL(videoURL);
        };

        // ซ่อนปุ่ม Select Video
        if (selectButton) {
            selectButton.style.display = 'none';
        }
    }
}


// ฟังก์ชันสำหรับแสดงผลการตรวจจับจากฐานข้อมูล
function displayDetectionResults(results) {
    // แสดงผลการตรวจจับใบหน้า
    const faceResults = results.filter(r => r.detection_type === 'face');
    if (faceResults.length > 0) {
        const latestFace = faceResults[0];
        if (latestFace.name && latestFace.student_id) {
            document.getElementById('name1').textContent = latestFace.name;
            document.getElementById('studentId1').textContent = latestFace.student_id;
            document.getElementById('detectionResult1').style.display = 'block';
        } else {
            alert('ไม่พบข้อมูลนักศึกษาในระบบ');
            document.getElementById('detectionResult1').style.display = 'none';
        }
    } else {
        alert('ไม่พบข้อมูลการตรวจจับใบหน้า');
        document.getElementById('detectionResult1').style.display = 'none';
    }

    // แสดงผลการตรวจจับทะเบียนรถ
    const plateResults = results.filter(r => r.detection_type === 'license_plate');
    if (plateResults.length > 0) {
        const latestPlate = plateResults[0];
        if (latestPlate.license_plate) {
            document.getElementById('licensePlate2').textContent = latestPlate.license_plate;
            document.getElementById('detectionResult2').style.display = 'block';
        } else {
            alert('ไม่พบข้อมูลทะเบียนรถ');
            document.getElementById('detectionResult2').style.display = 'none';
        }
    } else {
        alert('ไม่พบข้อมูลการตรวจจับทะเบียนรถ');
        document.getElementById('detectionResult2').style.display = 'none';
    }
}

/**
 * ฟังก์ชันสำหรับอัพโหลดไฟล์และประมวลผลการตรวจจับ
 * @param {number} inputNumber - หมายเลขของ input (1: ตรวจจับใบหน้า, 2: ตรวจจับป้ายทะเบียน)
 */
function uploadFile(inputNumber) {
    // ดึงข้อมูลที่จำเป็น
    const formData = new FormData();
    const fileInput = document.getElementById(`imageInput${inputNumber}`);
    const detectionResult = document.getElementById(`detectionResult${inputNumber}`);

    // ตรวจสอบว่ามีการเลือกไฟล์หรือไม่
    if (fileInput.files.length === 0) {
        alert("กรุณาเลือกไฟล์");
        return;
    }

    // แสดงข้อความยืนยันการตรวจจับ
    alert("กด Ok เพื่อยืนยันการตรวจจับ\nกรุณารอสักครู่...");

    // เพิ่มไฟล์ลงใน FormData
    formData.append('file', fileInput.files[0]);

    // กำหนด endpoint ตามประเภทการตรวจจับ
    const endpoint = inputNumber === 1 
        ? `http://localhost:5000/face_check` 
        : `http://localhost:5555/plate_check`;

    // ส่งข้อมูลไปยัง API
    fetch(endpoint, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => handleDetectionResponse(data, inputNumber, detectionResult))
    .catch(error => handleDetectionError(error, detectionResult));
}

/**
 * ฟังก์ชันจัดการผลลัพธ์จากการตรวจจับ
 * @param {Object} data - ข้อมูลผลลัพธ์จาก API
 * @param {number} inputNumber - หมายเลขของ input
 * @param {HTMLElement} detectionResult - element สำหรับแสดงผลการตรวจจับ
 */
function handleDetectionResponse(data, inputNumber, detectionResult) {
    if (!data.success) {
        // กรณีไม่สำเร็จ
        alert(data.case);
        detectionResult.style.display = 'none';
        return;
    }

    // กรณีตรวจจับสำเร็จ
    detectionResult.style.display = 'block';
    
    if (inputNumber === 1) {
        // แสดงผลการตรวจจับใบหน้า
        document.getElementById('name1').textContent = data.name;
        document.getElementById('studentId1').textContent = data.user_id;
    } else {
        // แสดงผลการตรวจจับป้ายทะเบียน
        document.getElementById('licensePlate2').textContent = data.plate;
    }
}

/**
 * ฟังก์ชันจัดการข้อผิดพลาดจากการตรวจจับ
 * @param {Error} error - ข้อผิดพลาดที่เกิดขึ้น
 * @param {HTMLElement} detectionResult - element สำหรับแสดงผลการตรวจจับ
 */
function handleDetectionError(error, detectionResult) {
    console.error('Error:', error);
    alert('เกิดข้อผิดพลาดในการตรวจจับ');
    detectionResult.style.display = 'none';
}

// ฟังก์ชันสำหรับรีเฟรชหน้า detection
function refreshDetectionSection() {
    // รีเซ็ตการแสดงตัวอย่างรูปภาพเฉพาะส่วนตรวจจับ
    const previews = document.querySelectorAll('#detection img[id^="preview"]');
    const imageInputs = document.querySelectorAll('#detection input[type="file"]');
    const fileBoxes = document.querySelectorAll('#detection .file-box');
    const detectionResults = document.querySelectorAll('#detection .detection-result');

    previews.forEach(preview => {
        preview.style.display = 'none';
        preview.src = '';
    });

    imageInputs.forEach(input => {
        input.value = '';
    });

    fileBoxes.forEach(fileBox => {
        const selectButton = fileBox.querySelector('button');
        if (selectButton) {
            selectButton.style.display = 'inline-block';
        }
    });

    // ซ่อนผลการตรวจจับ
    detectionResults.forEach(result => {
        result.style.display = 'none';
    });
}

// ฟังก์ชันสำหรับล้างข้อมูลฟอร์ม
function clearAddDataForm() {
    // ล้างวิดีโอ
    const preview = document.getElementById('preview3');
    if (preview) {
        preview.src = '';
        preview.style.display = 'none';
        preview.pause();
        preview.currentTime = 0;
    }

    // ล้าง input fields
    const user_idInput = document.getElementById('user_id');
    const nameInput = document.getElementById('name');
    const lastnameInput = document.getElementById('lastname');
    const videoInput = document.getElementById('video');
    
    if (user_idInput) user_idInput.value = '';
    if (nameInput) nameInput.value = '';
    if (lastnameInput) lastnameInput.value = '';
    if (videoInput) videoInput.value = '';

    // แสดงปุ่ม "เลือกวิดีโอ" กลับมา
    const fileBox = document.getElementById('fileBox3');
    const selectButton = fileBox.querySelector('button');
    if (selectButton) {
        selectButton.style.display = 'inline-block';
    }

    // ล้างและซ่อนข้อความสถานะ
    const statusDiv = document.getElementById('processingStatus');
    if (statusDiv) {
        statusDiv.textContent = '';
        statusDiv.className = '';
    }
}

// เรียกใช้เมื่อโหลดเริ่มต้นเพื่อแสดง section แรก
document.addEventListener('DOMContentLoaded', () => {
    showSection('detection');
    
    // เพิ่ม event listeners สำหรับปุ่มยืนยัน
    document.querySelector('.face .confirm-button').addEventListener('click', () => {
        handleConfirm(1, 'face');
    });
    
    document.querySelector('.sign .confirm-button').addEventListener('click', () => {
        handleConfirm(2, 'license_plate');
    });

    // เพิ่ม event listener สำหรับปุ่มบันทึกข้อมูล
    document.querySelector('.save-button').addEventListener('click', handleSaveStudent);

    // ดึงผลการตรวจจับเมื่อโหลดหน้า
    fetchDetectionResults();
});

// ฟังก์ชันสำหรับตรวจสอบความถูกต้องของข้อมูล
function validateForm() {
    const nameInput = document.querySelector('input[placeholder="ชื่อ-นามสกุล"]');
    const detailInput = document.querySelector('input[placeholder="รหัสผู้ใช้งาน"]');
    
    if (!nameInput.value.trim()) {
        alert('Please enter a name');
        return false;
    }
    if (!detailInput.value.trim()) {
        alert('Please enter details');
        return false;
    }
    return true;
}

// ฟังก์ชันสำหรับอัพโหลดวิดีโอและประมวลผลข้อมูล
function uploadVideo() {
    // สร้าง FormData object สำหรับส่งข้อมูลแบบ multipart/form-data
    const formData = new FormData();
    
    // ดึงข้อมูลจาก input fields
    const videoFile = document.getElementById('video').files[0];
    const name = document.getElementById('name').value;
    const lastname = document.getElementById('lastname').value;
    const user_id = document.getElementById('user_id').value;
    const statusDiv = document.getElementById('processingStatus'); 

    // ตรวจสอบว่ากรอกข้อมูลครบทุกช่องหรือไม่
    if (!videoFile || !name || !lastname || !user_id) {
        statusDiv.className = 'error';
        statusDiv.textContent = '❌ กรุณากรอกข้อมูลให้ครบถ้วน';
        return;
    }

    // ตรวจสอบประเภทของไฟล์ว่าเป็นวิดีโอหรือไม่
    if (!videoFile.type.startsWith('video/')) {
        statusDiv.className = 'error';
        statusDiv.textContent = '❌ กรุณาเลือกไฟล์วิดีโอ';
        return;
    }

    // ตรวจสอบขนาดไฟล์ต้องไม่เกิน 30MB
    if (videoFile.size > 30 * 1024 * 1024) {
        statusDiv.className = 'error';
        statusDiv.textContent = '❌ ขนาดไฟล์ต้องไม่เกิน 30MB';
        return;
    }

    // เพิ่มข้อมูลเข้าไปใน FormData
    formData.append('video', videoFile);
    formData.append('name', name);
    formData.append('lastname', lastname);
    formData.append('user_id', user_id);

    // แสดงสถานะกำลังประมวลผล
    statusDiv.className = 'loading';
    statusDiv.textContent = '⏳ กำลังประมวลผลวิดีโอ...';

    // ส่งข้อมูลไปยัง API endpoint
    fetch('http://localhost:3000/api/process-video', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // กรณีประมวลผลสำเร็จ
            statusDiv.className = 'success';
            statusDiv.textContent = '✅ ' + data.message + ' (' + data.framesCount + ' เฟรม)';
            
            // ซ่อนข้อความสถานะและล้างฟอร์มหลังจาก 10 วินาที
            setTimeout(() => {
                statusDiv.className = '';
                clearAddDataForm();
            }, 10000);
        } else {
            // กรณีเกิดข้อผิดพลาดจากการประมวลผล
            statusDiv.className = 'error';
            statusDiv.textContent = '❌ เกิดข้อผิดพลาด: ' + data.message;
            
            // ซ่อนข้อความแสดงข้อผิดพลาดหลังจาก 10 วินาที
            setTimeout(() => {
                statusDiv.className = '';
            }, 10000);
        }
    })
    .catch(err => {
        // กรณีไม่สามารถเชื่อมต่อกับ API ได้
        statusDiv.className = 'error';
        statusDiv.textContent = '❌ ไม่สามารถเชื่อมต่อกับ API ได้';
        console.error(err);
        
        // ซ่อนข้อความแสดงข้อผิดพลาดหลังจาก 10 วินาที
        setTimeout(() => {
            statusDiv.className = '';
        }, 10000);
    });
}