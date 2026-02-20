let form=document.querySelector("form");
let input=document.querySelectorAll(".form-input");
let main=document.querySelector("#main");

form.addEventListener("submit",function(dets){
	dets.preventDefault();
	let card=document.createElement("div");
	card.classList.add("card");
	let profile=document.createElement("div");
	profile.classList.add("profile");
	let img=document.createElement("img");
	img.setAttribute("src","input[4].value");
	let h3=document.createElement("h3");
	h3.textContent=`${input[0].value}`;
	let h6=document.createElement("h6");
	h6.textContent=`(${input[1].value} years old)`;
	let h5=document.createElement("h5");
	h5.textContent=`${input[2].value}`;
	let p=document.createElement("p");
	p.textContent=`${input[3].value}`;

	profile.appendChild(img);
	card.appendChild(profile);
	card.appendChild(h3);
	card.appendChild(h6);
	card.appendChild(h5);
	card.appendChild(p);

	main.appendChild(card);
});