document.addEventListener("DOMContentLoaded", function () {
    console.log("🚀 polygon_zone.js loaded successfully!");

    const video = document.getElementById("video-stream");
    const container = document.getElementById("konva-container");

    if (!video || !container) {
        console.error("❌ ERROR: Video or container not found!");
        return;
    }

    console.log("✅ Video element found, waiting for load...");

    // Initialize Konva.js only after the video is loaded
    video.onload = function () {
        console.log("✅ Video loaded successfully!");
        initializeKonva(video);
    };

    function initializeKonva(video) {
        console.log("🔧 Initializing Konva.js...");

        container.style.position = "absolute";
        container.style.left = video.offsetLeft + "px";
        container.style.top = video.offsetTop + "px";
        container.style.width = video.clientWidth + "px";
        container.style.height = video.clientHeight + "px";

        // Create Konva Stage
        const stage = new Konva.Stage({
            container: 'konva-container',
            width: video.clientWidth,
            height: video.clientHeight
        });

        const layer = new Konva.Layer();
        stage.add(layer);

        let polygons = [];
        let currentPolygon = null;

        // Load saved polygons from Django
        fetch("/get_polygons/")
            .then(response => response.json())
            .then(data => {
                data.polygons.forEach(points => {
                    let polygon = new Konva.Line({
                        points: points.flatMap(p => [p.x, p.y]),
                        fill: 'rgba(255, 0, 0, 0.3)',
                        stroke: 'red',
                        strokeWidth: 2,
                        closed: true,
                        draggable: true
                    });
                    layer.add(polygon);
                    polygons.push(polygon);
                });
                layer.draw();
            });

        // Function to start drawing a polygon
        window.startDrawing = function () {
            console.log("🎨 Polygon drawing started...");
            currentPolygon = new Konva.Line({
                points: [],
                fill: 'rgba(255, 0, 0, 0.3)',
                stroke: 'red',
                strokeWidth: 2,
                closed: true,
                draggable: true
            });

            layer.add(currentPolygon);
            polygons.push(currentPolygon);
        };

        // Event listener to add points to the polygon
        stage.on('click', function (e) {
            if (!currentPolygon) {
                console.warn("⚠️ WARNING: No active polygon. Click 'Draw Polygon' first.");
                return;
            }

            const pointer = stage.getPointerPosition();
            console.log(`🖱️ Point added at: ${pointer.x}, ${pointer.y}`);

            const points = currentPolygon.points();
            points.push(pointer.x, pointer.y);
            currentPolygon.points(points);
            layer.draw();
        });

        // Function to clear all polygons
        window.clearPolygons = function () {
            console.log("🗑️ Clearing all polygons...");
            polygons.forEach(poly => poly.destroy());
            polygons = [];
            layer.draw();
        };

        // Function to send polygons to Django backend
        window.savePolygons = function () {
            console.log("💾 Saving polygons to backend...");
            let polygonData = polygons.map(poly => {
                return poly.points().reduce((acc, value, index, array) => {
                    if (index % 2 === 0) acc.push({ x: value, y: array[index + 1] });
                    return acc;
                }, []);
            });

            fetch("/save_polygons/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify({ polygons: polygonData })
            })
            .then(response => response.json())
            .then(data => console.log("✅ Polygon saved successfully!", data))
            .catch(error => console.error("❌ ERROR:", error));
        };

        // Function to get CSRF token from Django
        function getCSRFToken() {
            return document.cookie.split("; ")
                .find(row => row.startsWith("csrftoken="))
                ?.split("=")[1];
        }
    }
});
