function hide_element() {
    var x = document.getElementById("flask-pagedown-content-preview");
    if (x.style.display === "block") {
        x.style.display = "none";
    } else {
        x.style.display = "block";
    }
}
