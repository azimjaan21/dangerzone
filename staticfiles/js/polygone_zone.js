document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("video-stream");

    // Wait for the video to load before initializing Konva
    video.onload = function () {
        initializeKonva(video);
    };

    function initializeKonva(video) {
        const stage = new Konva.Stage({
            container: 'konva-container',
            width: video.width,
            height: video.height
        });

        const layer = new Konva.Layer();
        stage.add(layer);

        let polygons = [];
        let currentPolygon = null;

        // Start drawing a polygon
        window.startDrawing = function () {
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

        // Add points to the polygon
        stage.on('click', function (e) {
            if (!currentPolygon) return;
            const pointer = stage.getPointerPosition();
            const points = currentPolygon.points();
            points.push(pointer.x, pointer.y);
            currentPolygon.points(points);
            layer.draw();
        });

        // Clear all polygons
        window.clearPolygons = function () {
            polygons.forEach(poly => poly.destroy());
            polygons = [];
            layer.draw();
        };

        // Save polygons to Django backend
        window.savePolygons = function () {
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
            .then(data => alert(data.message))
            .catch(error => console.error("Error:", error));
        };

        // Get CSRF token from Django
        function getCSRFToken() {
            return document.cookie.split("; ")
                .find(row => row.startsWith("csrftoken="))
                ?.split("=")[1];
        }
    }
});
