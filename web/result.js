'use strict'

async function save(){
    var val = await eel.save_movement(localStorage.movement);
    console.log("save");
}

async function retry() {
    var music_path = await eel.select_dance(localStorage.music_id)();
    location.href = "./playing.html";
}

function backToMenu(){
    location.href = "./select.html"
}

function start(){
    document.getElementById("score").innerText = localStorage.getItem("last_score") + "点";
    document.getElementById("undou").innerText = localStorage.movement + "pt";

    var graph_image = document.createElement("img");
    graph_image.src = localStorage.figPath;
    graph_image.alt = "graph";
    graph_image.width = 1200;
    graph_image.height = 300;
    document.getElementById("graph").appendChild(graph_image);
}