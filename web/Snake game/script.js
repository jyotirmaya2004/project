const board=document.querySelector(".board");
const startButton=document.querySelector(".btn-start");
const modal=document.querySelector(".modal");
const startGameModal=document.querySelector(".start-game");
const gameOverModal=document.querySelector(".game-over");
const restartButton=document.querySelector(".btn-restart");
const score=document.querySelector("#score");
const highScore=document.querySelector("#high-score");

let hScore = Number(localStorage.getItem("lhScore")) || 0;
highScore.innerHTML = hScore;
let count=0;
let totalSeconds = 0;
let timerId=null;

const foodImages = [
    "apple.png",
    "pizza.png",
    "burger.png",
    "grapes.png",
    "donut.png"
];
let currentFoodImage = foodImages[Math.floor(Math.random() * foodImages.length)];

const blockHeight=30;
const blockWidth=30;

const cols=Math.floor(board.clientWidth / blockWidth);
const rows=Math.floor(board.clientHeight / blockHeight);
let intervalId=null;
let food={x:Math.floor(Math.random()*rows),y:Math.floor(Math.random()*cols)};

const blocks=[];
let snake=[{
	x:1,
	y:3
}];

let direction='down';


// for(let i=0;i<(rows*cols);i++){
// 	const block=document.createElement("div");
// 	block.classList.add("block");
// 	board.appendChild(block);

// }
for(let row=0;row<rows;row++){
	for(let col=0;col<cols;col++){
		const block=document.createElement("div");
		block.classList.add("block");
		board.appendChild(block);
		// block.innerText=`${row},${col}`;
		blocks[`${row},${col}`]=block;

	}
}
function render(){
	let head=null;
	const foodBlock = blocks[`${food.x},${food.y}`];
foodBlock.classList.add("food");
foodBlock.style.backgroundImage = `url(${currentFoodImage})`;
	if(direction==='left'){
		head={
			x:snake[0].x,
			y:snake[0].y-1
		}
	}
	else if(direction==='right'){
		head={
			x:snake[0].x,
			y:snake[0].y+1
		}
	}
	else if(direction==='down'){
		head={
			x:snake[0].x+1,
			y:snake[0].y
		}
	}
	else if(direction==='up'){
		head={
			x:snake[0].x-1,
			y:snake[0].y
		}
	}
	if(head.x<0||head.x>=rows||head.y<0||head.y>=cols){
		hScore=Math.max(hScore,count);
		localStorage.setItem("lhScore",hScore);
		highScore.innerHTML=`${hScore}`;

		clearInterval(intervalId);
    	clearInterval(timerId);

		modal.style.display="flex";
		startGameModal.style.display="none";
		gameOverModal.style.display="flex";

		return;
	}

	if(head.x==food.x && head.y==food.y){
		blocks[`${food.x},${food.y}`].classList.remove("food");
		count++;
		score.innerHTML=`${count<10?"0":""}${count}`;
		snake.unshift(food);
		food={x:Math.floor(Math.random()*rows),y:Math.floor(Math.random()*cols)};
		currentFoodImage = foodImages[Math.floor(Math.random() * foodImages.length)];
		showFoodAnimation();

		return;
	}

	snake.forEach(segment=>{
		blocks[`${segment.x},${segment.y}`].classList.remove("fill");
	});

	snake.unshift(head);
	snake.pop();
	snake.forEach(segment=>{
		blocks[`${segment.x},${segment.y}`].classList.add("fill");
	});
}


// intervalId=setInterval(()=>{

// 	render();
// },300);

startButton.addEventListener("click",function(){
	modal.style.display="none";
	intervalId= setInterval(()=>{render()},200);
	startTimer();
})

restartButton.addEventListener("click",restartGame)

function startTimer() {
    clearInterval(timerId);

    timerId = setInterval(() => {
        totalSeconds++;

        let minutes = Math.floor(totalSeconds / 60);
        let seconds = totalSeconds % 60;

        document.getElementById("timer").innerText =
            `${minutes < 10 ? "0" : ""}${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
    }, 1000);
}

function showFoodAnimation() {
    const foodBlock = blocks[`${food.x},${food.y}`];

    foodBlock.classList.remove("food");
    void foodBlock.offsetWidth;   // restart animation
    foodBlock.classList.add("food");

    foodBlock.style.backgroundImage = `url(${currentFoodImage})`;
}

function restartGame(){
    clearInterval(intervalId);
    clearInterval(timerId);
	totalSeconds = 0;
	document.getElementById("timer").innerText = "00:00";

    // remove old food
    blocks[`${food.x},${food.y}`].classList.remove("food");

    // remove old snake body
    snake.forEach(segment => {
        blocks[`${segment.x},${segment.y}`].classList.remove("fill");
    });

    // reset values
    count = 0;
    score.innerHTML = count;

    snake = [{ x: 1, y: 3 }];
    direction = "down";

    food = {
        x: Math.floor(Math.random() * rows),
        y: Math.floor(Math.random() * cols)
    };

    modal.style.display = "none";

    intervalId = setInterval(render, 200);
	startTimer();
}

window.addEventListener("keydown",(event)=>{
	if(event.key=="ArrowUp"){
		direction="up";
	}
	else if(event.key=="ArrowDown"){
		direction="down";
	}
	else if(event.key=="ArrowLeft"){
		direction="left";
	}
	else if(event.key=="ArrowRight"){
		direction="right";
	}
})