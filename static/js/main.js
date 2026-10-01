/* ==========================================================================
   WheelX Interactive Script & Fare Calculator
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // ── 1. Vehicle Detail Page Live Price Calculator ──
    const startDateInput = document.getElementById('id_start_date');
    const endDateInput = document.getElementById('id_end_date');
    const totalPriceDisplay = document.getElementById('calc_total_price');
    const daysCountDisplay = document.getElementById('calc_days_count');
    const baseFareDisplay = document.getElementById('calc_base_fare');
    const addonsTotalDisplay = document.getElementById('calc_addons_total');
    const gstAmountDisplay = document.getElementById('calc_gst_amount');
    const depositDisplay = document.getElementById('calc_deposit_amount');

    const addonInsurance = document.getElementById('addon_insurance');
    const addonUnlimited = document.getElementById('addon_unlimited');
    const addonDelivery = document.getElementById('addon_delivery');

    function calculateDetailFare() {
        if (!startDateInput || !endDateInput) return;

        const pricePerDay = parseFloat(startDateInput.dataset.price || 0);
        const vehicleType = startDateInput.dataset.type || 'CAR';
        const startVal = startDateInput.value;
        const endVal = endDateInput.value;

        if (!startVal || !endVal) {
            if (totalPriceDisplay) totalPriceDisplay.textContent = '₹0';
            return;
        }

        const start = new Date(startVal);
        const end = new Date(endVal);

        let diffDays = 0;
        if (end > start) {
            const diffTime = Math.abs(end - start);
            diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        } else if (startVal === endVal) {
            diffDays = 1;
        }

        if (diffDays <= 0) diffDays = 1;

        const baseFare = diffDays * pricePerDay;

        // Calculate Add-ons
        let addonsTotal = 0;
        if (addonInsurance && addonInsurance.checked) {
            addonsTotal += 150 * diffDays;
        }
        if (addonUnlimited && addonUnlimited.checked) {
            addonsTotal += 250 * diffDays;
        }
        if (addonDelivery && addonDelivery.checked) {
            addonsTotal += 200; // flat fee
        }

        const taxableAmount = baseFare + addonsTotal;
        const gst = Math.round(taxableAmount * 0.18);
        const deposit = 1000;
        const grandTotal = taxableAmount + gst + deposit;

        if (daysCountDisplay) daysCountDisplay.textContent = `${diffDays} day${diffDays > 1 ? 's' : ''}`;
        if (baseFareDisplay) baseFareDisplay.textContent = `₹${baseFare.toLocaleString('en-IN')}`;
        if (addonsTotalDisplay) addonsTotalDisplay.textContent = `₹${addonsTotal.toLocaleString('en-IN')}`;
        if (gstAmountDisplay) gstAmountDisplay.textContent = `₹${gst.toLocaleString('en-IN')}`;
        if (depositDisplay) depositDisplay.textContent = `₹${deposit.toLocaleString('en-IN')}`;
        if (totalPriceDisplay) totalPriceDisplay.textContent = `₹${grandTotal.toLocaleString('en-IN')}`;
    }

    if (startDateInput && endDateInput) {
        const today = new Date().toISOString().split('T')[0];
        const tomorrow = new Date(Date.now() + 86400000).toISOString().split('T')[0];
        if (!startDateInput.value) startDateInput.value = today;
        if (!endDateInput.value) endDateInput.value = tomorrow;

        startDateInput.addEventListener('change', calculateDetailFare);
        endDateInput.addEventListener('change', calculateDetailFare);
        
        [addonInsurance, addonUnlimited, addonDelivery].forEach(el => {
            if (el) el.addEventListener('change', calculateDetailFare);
        });

        calculateDetailFare();
    }

    // ── 2. Homepage Interactive Fare Estimator ──
    const homeVehSelect = document.getElementById('home_calc_vehicle');
    const homeStartInput = document.getElementById('home_calc_start');
    const homeEndInput = document.getElementById('home_calc_end');
    const homeInsCheck = document.getElementById('home_addon_insurance');
    const homeUnlimCheck = document.getElementById('home_addon_unlimited');
    const homeDelivCheck = document.getElementById('home_addon_delivery');

    function calculateHomeFare() {
        if (!homeVehSelect || !homeStartInput || !homeEndInput) return;

        const selectedOption = homeVehSelect.options[homeVehSelect.selectedIndex];
        if (!selectedOption) return;

        const rate = parseFloat(selectedOption.dataset.price || 0);
        const vType = selectedOption.dataset.type || 'CAR';
        const vName = selectedOption.dataset.name || 'Vehicle';

        const startVal = homeStartInput.value;
        const endVal = homeEndInput.value;

        let diffDays = 1;
        if (startVal && endVal) {
            const start = new Date(startVal);
            const end = new Date(endVal);
            if (end > start) {
                diffDays = Math.ceil(Math.abs(end - start) / (1000 * 60 * 60 * 24));
            }
        }

        const baseFare = diffDays * rate;
        let addonsTotal = 0;
        if (homeInsCheck && homeInsCheck.checked) addonsTotal += 150 * diffDays;
        if (homeUnlimCheck && homeUnlimCheck.checked) addonsTotal += 250 * diffDays;
        if (homeDelivCheck && homeDelivCheck.checked) addonsTotal += 200;

        const taxable = baseFare + addonsTotal;
        const gst = Math.round(taxable * 0.18);
        const deposit = 1000;
        const grandTotal = taxable + gst + deposit;

        const outDays = document.getElementById('home_out_days');
        const outRate = document.getElementById('home_out_rate');
        const outBase = document.getElementById('home_out_base');
        const outAddons = document.getElementById('home_out_addons');
        const outGst = document.getElementById('home_out_gst');
        const outDeposit = document.getElementById('home_out_deposit');
        const outGrand = document.getElementById('home_out_grand');
        const outWaLink = document.getElementById('home_out_wa_btn');

        if (outDays) outDays.textContent = `${diffDays} Day${diffDays > 1 ? 's' : ''}`;
        if (outRate) outRate.textContent = `₹${rate.toLocaleString('en-IN')}/day`;
        if (outBase) outBase.textContent = `₹${baseFare.toLocaleString('en-IN')}`;
        if (outAddons) outAddons.textContent = `₹${addonsTotal.toLocaleString('en-IN')}`;
        if (outGst) outGst.textContent = `₹${gst.toLocaleString('en-IN')}`;
        if (outDeposit) outDeposit.textContent = `₹${deposit.toLocaleString('en-IN')}`;
        if (outGrand) outGrand.textContent = `₹${grandTotal.toLocaleString('en-IN')}`;

        if (outWaLink) {
            const msg = encodeURIComponent(
                `Hello WheelX! I calculated rental for ${vName} (${diffDays} days). Estimated Total: ₹${grandTotal.toLocaleString('en-IN')}. Please confirm availability at Luxuria Business Park, Morbi!`
            );
            outWaLink.href = `https://wa.me/919624497998?text=${msg}`;
        }
    }

    if (homeVehSelect && homeStartInput && homeEndInput) {
        const today = new Date().toISOString().split('T')[0];
        const tomorrow = new Date(Date.now() + 86400000).toISOString().split('T')[0];
        if (!homeStartInput.value) homeStartInput.value = today;
        if (!homeEndInput.value) homeEndInput.value = tomorrow;

        [homeVehSelect, homeStartInput, homeEndInput, homeInsCheck, homeUnlimCheck, homeDelivCheck].forEach(el => {
            if (el) el.addEventListener('change', calculateHomeFare);
        });

        calculateHomeFare();
    }

    // ── 3. Category Filtering on vehicle list ──
    const filterBtns = document.querySelectorAll('.tab-btn[data-filter]');
    const vehicleCards = document.querySelectorAll('.vehicle-card[data-category]');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filterValue = btn.getAttribute('data-filter');

            vehicleCards.forEach(card => {
                if (filterValue === 'all' || card.getAttribute('data-category') === filterValue) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // ── 4. Express KYC Form Mandatory Validation ──
    const bookingForm = document.getElementById('vehicle_booking_form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', (e) => {
            const dlNo = (document.getElementById('id_dl_number')?.value || '').trim();
            const dlDoc = document.getElementById('id_dl_doc')?.files.length || 0;
            const aadhaarNo = (document.getElementById('id_aadhaar_number')?.value || '').trim();
            const aadhaarDoc = document.getElementById('id_aadhaar_doc')?.files.length || 0;

            const hasDl = !!(dlNo || dlDoc);
            const hasAadhaar = !!(aadhaarNo || aadhaarDoc);

            if (!hasDl && !hasAadhaar) {
                e.preventDefault();
                alert('⚠️ Express KYC Verification Required:\n\nPlease provide either your Driving License (Number or Photo) OR Aadhaar Card (Number or Photo) to proceed with the booking.');
                
                const dlInput = document.getElementById('id_dl_number');
                if (dlInput) dlInput.focus();
                return false;
            }
        });
    }

    // ── 5. Unique 3D Canvas Scene Engine per Page ──
    const heroCanvas = document.getElementById('hero-3d-canvas');
    if (heroCanvas) {
        initThreeJSScene(heroCanvas);
    }

    const fleetCanvas = document.getElementById('fleet-3d-canvas');
    if (fleetCanvas) {
        initFleet3DSpeedwayScene(fleetCanvas);
    }

    const contactCanvas = document.getElementById('contact-3d-canvas');
    if (contactCanvas) {
        initContact3DHologramGlobe(contactCanvas);
    }

    const aboutCanvas = document.getElementById('about-3d-canvas');
    if (aboutCanvas) {
        initAbout3DKineticScene(aboutCanvas);
    }

    const detailCanvas = document.getElementById('detail-3d-canvas');
    if (detailCanvas) {
        initDetail3DCanvas(detailCanvas);
    }

    // ── 6. Interactive 3D Card Hover Tilt System ──
    init3DTiltEffects();
});

/* ════════════════════════════════════════════════════════════════
   3D Graphics & Tilt Helper Functions
   ════════════════════════════════════════════════════════════════ */

function initThreeJSScene(canvas) {
    if (typeof THREE === 'undefined') return;

    const heroSection = canvas.parentElement;
    let width = heroSection.clientWidth || window.innerWidth;
    let height = heroSection.clientHeight || 500;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
    camera.position.z = 30;

    const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // 3D Glowing Particle Cloud
    const particleCount = 140;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const colorBlue = new THREE.Color('#0EA5E9');
    const colorSky = new THREE.Color('#38BDF8');
    const colorNavy = new THREE.Color('#0284C7');

    for (let i = 0; i < particleCount; i++) {
        positions[i * 3] = (Math.random() - 0.5) * 85;
        positions[i * 3 + 1] = (Math.random() - 0.5) * 55;
        positions[i * 3 + 2] = (Math.random() - 0.5) * 45;

        const mixedColor = Math.random() > 0.5 ? colorBlue.clone().lerp(colorSky, Math.random()) : colorNavy;
        colors[i * 3] = mixedColor.r;
        colors[i * 3 + 1] = mixedColor.g;
        colors[i * 3 + 2] = mixedColor.b;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
        size: 0.9,
        vertexColors: true,
        transparent: true,
        opacity: 0.8,
    });

    const particleSystem = new THREE.Points(geometry, material);
    scene.add(particleSystem);

    // 3D Dynamic Wireframe Ring Mesh
    const torusGeom = new THREE.TorusGeometry(9, 2.5, 16, 60);
    const wireframeMat = new THREE.MeshBasicMaterial({
        color: 0x0EA5E9,
        wireframe: true,
        transparent: true,
        opacity: 0.16
    });
    const torusMesh = new THREE.Mesh(torusGeom, wireframeMat);
    torusMesh.position.set(16, 2, -10);
    scene.add(torusMesh);

    // Mouse interactive tracking
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    window.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX - window.innerWidth / 2) * 0.012;
        mouseY = (e.clientY - window.innerHeight / 2) * 0.012;
    });

    // Window resize listener
    window.addEventListener('resize', () => {
        width = heroSection.clientWidth || window.innerWidth;
        height = heroSection.clientHeight || 500;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    });

    // 60FPS Render Loop
    function animate() {
        requestAnimationFrame(animate);

        targetX += (mouseX - targetX) * 0.05;
        targetY += (mouseY - targetY) * 0.05;

        particleSystem.rotation.y += 0.0012;
        particleSystem.rotation.x += 0.0006;

        torusMesh.rotation.x += 0.004;
        torusMesh.rotation.y += 0.007;

        camera.position.x = targetX;
        camera.position.y = -targetY;
        camera.lookAt(scene.position);

        renderer.render(scene, camera);
    }

    animate();
}

function init3DTiltEffects() {
    const tiltElements = document.querySelectorAll('.vehicle-card, .brand-card, .feature-box, .contact-info-card');

    tiltElements.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((y - centerY) / centerY) * -10;
            const rotateY = ((x - centerX) / centerX) * 10;

            card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateZ(8px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
        });
    });
}

/* ════════════════════════════════════════════════════════════════
   UNIQUE PAGE 3D SCENE 1: Fleet Speedway Grid Tunnel
   ════════════════════════════════════════════════════════════════ */
function initFleet3DSpeedwayScene(canvas) {
    if (typeof THREE === 'undefined') return;

    const parent = canvas.parentElement;
    let width = parent.clientWidth || window.innerWidth;
    let height = parent.clientHeight || 450;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(65, width / height, 0.1, 1000);
    camera.position.set(0, 4, 25);

    const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Moving 3D Road Grid Mesh
    const gridHelper = new THREE.GridHelper(140, 45, 0x0EA5E9, 0x38BDF8);
    gridHelper.position.y = -5;
    gridHelper.position.z = -10;
    scene.add(gridHelper);

    // Speed Lines drifting towards camera
    const lineCount = 50;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(lineCount * 6);

    for (let i = 0; i < lineCount; i++) {
        const x = (Math.random() - 0.5) * 60;
        const y = (Math.random() - 0.5) * 12 - 1;
        const z = (Math.random() - 0.5) * 80;

        positions[i * 6] = x;
        positions[i * 6 + 1] = y;
        positions[i * 6 + 2] = z;

        positions[i * 6 + 3] = x;
        positions[i * 6 + 4] = y;
        positions[i * 6 + 5] = z + 5;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    const lineMat = new THREE.LineBasicMaterial({
        color: 0x0EA5E9,
        transparent: true,
        opacity: 0.65
    });

    const speedLines = new THREE.LineSegments(geometry, lineMat);
    scene.add(speedLines);

    let mouseX = 0;
    let mouseY = 0;
    window.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX - window.innerWidth / 2) * 0.008;
        mouseY = (e.clientY - window.innerHeight / 2) * 0.008;
    });

    window.addEventListener('resize', () => {
        width = parent.clientWidth || window.innerWidth;
        height = parent.clientHeight || 450;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    });

    function animate() {
        requestAnimationFrame(animate);

        gridHelper.position.z += 0.22;
        if (gridHelper.position.z > 5) gridHelper.position.z = -10;

        const posAttr = speedLines.geometry.attributes.position;
        for (let i = 0; i < lineCount; i++) {
            posAttr.array[i * 6 + 2] += 0.35;
            posAttr.array[i * 6 + 5] += 0.35;
            if (posAttr.array[i * 6 + 2] > 30) {
                posAttr.array[i * 6 + 2] = -50;
                posAttr.array[i * 6 + 5] = -45;
            }
        }
        posAttr.needsUpdate = true;

        camera.position.x += (mouseX - camera.position.x) * 0.05;
        camera.position.y += (4 - mouseY - camera.position.y) * 0.05;
        camera.lookAt(0, 0, -20);

        renderer.render(scene, camera);
    }
    animate();
}

/* ════════════════════════════════════════════════════════════════
   UNIQUE PAGE 3D SCENE 2: Contact Cyber Hologram Globe
   ════════════════════════════════════════════════════════════════ */
function initContact3DHologramGlobe(canvas) {
    if (typeof THREE === 'undefined') return;

    const parent = canvas.parentElement;
    let width = parent.clientWidth || window.innerWidth;
    let height = parent.clientHeight || 500;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 1000);
    camera.position.set(0, 0, 32);

    const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // 1. Holographic Wireframe Earth Globe
    const sphereGeom = new THREE.SphereGeometry(10.5, 24, 24);
    const wireframeMat = new THREE.MeshBasicMaterial({
        color: 0x0EA5E9,
        wireframe: true,
        transparent: true,
        opacity: 0.22
    });
    const globeMesh = new THREE.Mesh(sphereGeom, wireframeMat);
    scene.add(globeMesh);

    // 2. Inner Core Mesh
    const coreGeom = new THREE.IcosahedronGeometry(7, 2);
    const coreMat = new THREE.MeshBasicMaterial({
        color: 0x38BDF8,
        wireframe: true,
        transparent: true,
        opacity: 0.15
    });
    const coreMesh = new THREE.Mesh(coreGeom, coreMat);
    scene.add(coreMesh);

    // 3. Orbiting Hologram Radar Ring
    const ringGeom = new THREE.RingGeometry(12.5, 12.9, 64);
    const ringMat = new THREE.MeshBasicMaterial({
        color: 0x0EA5E9,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.35
    });
    const radarRing = new THREE.Mesh(ringGeom, ringMat);
    radarRing.rotation.x = Math.PI / 3;
    scene.add(radarRing);

    // 4. GPS Location Beacons
    const beaconCount = 10;
    const beaconGroup = new THREE.Group();
    for (let i = 0; i < beaconCount; i++) {
        const phi = Math.acos(-1 + (2 * i) / beaconCount);
        const theta = Math.sqrt(beaconCount * Math.PI) * phi;

        const beaconGeom = new THREE.SphereGeometry(0.35, 8, 8);
        const beaconMat = new THREE.MeshBasicMaterial({ color: 0x38BDF8 });
        const beacon = new THREE.Mesh(beaconGeom, beaconMat);

        beacon.position.setFromSphericalCoords(10.7, phi, theta);
        beaconGroup.add(beacon);
    }
    scene.add(beaconGroup);

    let mouseX = 0;
    let mouseY = 0;
    window.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX - window.innerWidth / 2) * 0.01;
        mouseY = (e.clientY - window.innerHeight / 2) * 0.01;
    });

    window.addEventListener('resize', () => {
        width = parent.clientWidth || window.innerWidth;
        height = parent.clientHeight || 500;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    });

    function animate() {
        requestAnimationFrame(animate);

        globeMesh.rotation.y += 0.003;
        coreMesh.rotation.y -= 0.005;
        coreMesh.rotation.x += 0.002;
        radarRing.rotation.z += 0.006;
        beaconGroup.rotation.y += 0.003;

        camera.position.x += (mouseX - camera.position.x) * 0.05;
        camera.position.y += (-mouseY - camera.position.y) * 0.05;
        camera.lookAt(scene.position);

        renderer.render(scene, camera);
    }
    animate();
}

/* ════════════════════════════════════════════════════════════════
   UNIQUE PAGE 3D SCENE 3: About Page Kinetic Engine Core
   ════════════════════════════════════════════════════════════════ */
function initAbout3DKineticScene(canvas) {
    if (typeof THREE === 'undefined') return;

    const parent = canvas.parentElement;
    let width = parent.clientWidth || window.innerWidth;
    let height = parent.clientHeight || 500;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 1000);
    camera.position.set(0, 0, 28);

    const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // 1. Central Spinning Kinetic Octahedron Core
    const octGeom = new THREE.OctahedronGeometry(8, 1);
    const octMat = new THREE.MeshBasicMaterial({
        color: 0x0EA5E9,
        wireframe: true,
        transparent: true,
        opacity: 0.25
    });
    const octMesh = new THREE.Mesh(octGeom, octMat);
    scene.add(octMesh);

    // 2. Outer Rotating Orbital Ring
    const torusGeom = new THREE.TorusGeometry(12, 0.4, 16, 60);
    const torusMat = new THREE.MeshBasicMaterial({
        color: 0x38BDF8,
        wireframe: true,
        transparent: true,
        opacity: 0.3
    });
    const torusMesh = new THREE.Mesh(torusGeom, torusMat);
    torusMesh.rotation.x = Math.PI / 4;
    scene.add(torusMesh);

    // 3. Floating Kinetic Cube Nodes
    const cubeGroup = new THREE.Group();
    const cubeCount = 14;
    for (let i = 0; i < cubeCount; i++) {
        const cGeom = new THREE.BoxGeometry(1.2, 1.2, 1.2);
        const cMat = new THREE.MeshBasicMaterial({
            color: 0x0EA5E9,
            wireframe: true,
            transparent: true,
            opacity: 0.45
        });
        const cube = new THREE.Mesh(cGeom, cMat);

        const angle = (i / cubeCount) * Math.PI * 2;
        const radius = 14;
        cube.position.set(Math.cos(angle) * radius, (Math.random() - 0.5) * 8, Math.sin(angle) * radius);
        cubeGroup.add(cube);
    }
    scene.add(cubeGroup);

    let mouseX = 0;
    let mouseY = 0;
    window.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX - window.innerWidth / 2) * 0.01;
        mouseY = (e.clientY - window.innerHeight / 2) * 0.01;
    });

    window.addEventListener('resize', () => {
        width = parent.clientWidth || window.innerWidth;
        height = parent.clientHeight || 500;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    });

    function animate() {
        requestAnimationFrame(animate);

        octMesh.rotation.y += 0.005;
        octMesh.rotation.x += 0.003;

        torusMesh.rotation.z += 0.004;
        torusMesh.rotation.y -= 0.002;

        cubeGroup.rotation.y += 0.004;

        camera.position.x += (mouseX - camera.position.x) * 0.05;
        camera.position.y += (-mouseY - camera.position.y) * 0.05;
        camera.lookAt(scene.position);

        renderer.render(scene, camera);
    }
    animate();
}

/* ════════════════════════════════════════════════════════════════
   UNIQUE PAGE 3D SCENE 4: Vehicle Detail Hologram Stage
   ════════════════════════════════════════════════════════════════ */
function initDetail3DCanvas(canvas) {
    if (typeof THREE === 'undefined') return;

    const parent = canvas.parentElement;
    let width = parent.clientWidth || window.innerWidth;
    let height = parent.clientHeight || 350;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
    camera.position.set(0, 0, 22);

    const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // 3D Stage Ring
    const stageGeom = new THREE.CylinderGeometry(8, 9, 1, 32, 1, true);
    const stageMat = new THREE.MeshBasicMaterial({
        color: 0x0EA5E9,
        wireframe: true,
        transparent: true,
        opacity: 0.25
    });
    const stageMesh = new THREE.Mesh(stageGeom, stageMat);
    stageMesh.position.y = -4;
    scene.add(stageMesh);

    // Orbiting Spec Spheres
    const pGroup = new THREE.Group();
    for (let i = 0; i < 12; i++) {
        const pGeom = new THREE.OctahedronGeometry(0.8, 0);
        const pMat = new THREE.MeshBasicMaterial({ color: 0x38BDF8, wireframe: true });
        const pMesh = new THREE.Mesh(pGeom, pMat);

        const angle = (i / 12) * Math.PI * 2;
        pMesh.position.set(Math.cos(angle) * 11, Math.sin(angle) * 4, Math.sin(angle) * 2);
        pGroup.add(pMesh);
    }
    scene.add(pGroup);

    let mouseX = 0;
    let mouseY = 0;
    window.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX - window.innerWidth / 2) * 0.008;
        mouseY = (e.clientY - window.innerHeight / 2) * 0.008;
    });

    window.addEventListener('resize', () => {
        width = parent.clientWidth || window.innerWidth;
        height = parent.clientHeight || 350;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    });

    function animate() {
        requestAnimationFrame(animate);

        stageMesh.rotation.y += 0.004;
        pGroup.rotation.y += 0.006;
        pGroup.rotation.z += 0.002;

        camera.position.x += (mouseX - camera.position.x) * 0.05;
        camera.position.y += (-mouseY - camera.position.y) * 0.05;
        camera.lookAt(scene.position);

        renderer.render(scene, camera);
    }
    animate();
}
