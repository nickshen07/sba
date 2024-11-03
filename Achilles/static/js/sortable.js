window.addEventListener("load", () => {
    // (PART A) GET TABLE ROWS, EXCLUDE HEADER ROW
    var all = document.querySelectorAll("#demo tr:not(:first-of-type)");

    // (PART B) "CURRENT ROW BEING DRAGGED"
    var dragged;

    // (PART C) DRAG-AND-DROP MECHANISM
    for (let tr of all) {
        // (C1) ROW IS DRAGGABLE
        tr.draggable = true;

        // (C2) ON DRAG START - SET "CURRENTLY DRAGGED" & DATA TRANSFER
        tr.ondragstart = e => {
            dragged = tr;
            e.dataTransfer.dropEffect = "move";
            e.dataTransfer.effectAllowed = "move";
            e.dataTransfer.setData("text/html", tr.innerHTML);
        };

        // (C3) PREVENT DRAG OVER - NECESSARY FOR DROP TO WORK
        tr.ondragover = e => e.preventDefault();

        // (C4) ON DROP - "SWAP ROWS"
        tr.ondrop = e => {
            e.preventDefault();
            if (dragged != tr) {
                dragged.innerHTML = tr.innerHTML;
                tr.innerHTML = e.dataTransfer.getData("text/html");
            }
        };

        // (C5) COSMETICS - HIGHLIGHT ROW "ON DRAG HOVER"
        tr.ondragenter = () => tr.classList.add("hover");
        tr.ondragleave = () => tr.classList.remove("hover");
        tr.ondragend = () => {
            for (let r of all) { r.classList.remove("hover"); }
        };
    }
});