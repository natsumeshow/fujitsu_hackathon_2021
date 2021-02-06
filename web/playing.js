function goToResult(){
    //console.log("test1");
    result_f();
    setTimeout(function(){
        location.href='result.html';
    }, 10000);
}

async function result_f() {
    var val = await eel.result()();
    localStorage.setItem("last_score", val.last_score);
    localStorage.setItem("figPath", val.figPath);
    localStorage.setItem("movement", val.movement);
}



var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');

var v = document.getElementById("movie");
var flag = true;

function getCurrentTime(){
    if(console.currentTime!=0 && !v.ended && !v.paused){
        return v.currentTime;
    }else if(v.ended){
        return -2;
    }else{
        return -1;
    }
}

async function Play1(){
    console.log("clicked");
    if(flag){
        flag = false;
        setTimeout(function(){
            v.play();
            console.log("started");

        },3000);

        var videoFlag = true;
        while(videoFlag){
            if(getCurrentTime()==-2){
                videoFlag = false;
                goToResult();
            }else{

                var val = await eel.disp_score(getCurrentTime())();

                if(val.isPlaying){
                    //console.log(val.score);
                    deleteCanvas();
                    drawMatchRate(val.score);
                    drawStickFig(val.landmark);
                }
            }
        }
    }
}

function Pause1(){
    v.pause();
    flag = true;
}

function deleteCanvas(){
    ctx.clearRect(0, 0, canvas.clientWidth, canvas.height);
}

//val(得点) に応じてゲージ的なものを描画
function drawMatchRate(val){
    ctx.fillStyle = 'blue';
    ctx.fillRect(10, 100-val+10, 50, val);
}

function drawStickFig(val){

    for(var i=0;i<14;i++){
        if(val[i][0]>=0 && val[i][1]>=0){
            ctx.beginPath();
            ctx.arc(val[i][0], val[i][1], 10, 0, Math.PI*2, false);
            ctx.fill();
        }
    }

    drawLine(val[0], val[13]);
    drawLine(val[1], val[13]);
    drawLine(val[4], val[13]);
    drawLine(val[1], val[2]);
    drawLine(val[2], val[3]);
    drawLine(val[4], val[5]);
    drawLine(val[5], val[6]);
    drawLine(val[13], val[7]);
    drawLine(val[7], val[8]);
    drawLine(val[8], val[9]);
    drawLine(val[13], val[10]);
    drawLine(val[10], val[11]);
    drawLine(val[11], val[12]);

}

function drawLine(p1, p2){
    if(p1[0]<0 || p2[0]<0){
        return false;
    }
    ctx.beginPath();
    ctx.lineWidth = 5;
    ctx.strokeStyle = "aliceblue";
    ctx.moveTo(p1[0], p1[1]);
    ctx.lineTo(p2[0],p2[1]);
    ctx.stroke();
}