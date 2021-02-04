'use strict'

function save(){
    console.log("save");
}

function retry(){
    location.href = "./playing.html"
    
}

function backToMenu(){
    location.href = "./select.html"
}

function start(){
    document.getElementById("score").innerText = localStorage.last_score + "点";
    document.getElementById("undou").innerText = localStorage.movement + "pt";
    var graph_image = document.createElement("img");
    graph_image.src = localStorage.figPath;
    graph_image.alt = "graph";
    document.getElementById("graph").appendChild(graph_image);
}