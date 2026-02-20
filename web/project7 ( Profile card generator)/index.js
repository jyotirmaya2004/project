// let form=document.querySelector("form");
// let input=document.querySelectorAll(".form-input");
// let main=document.querySelector("#main");

// form.addEventListener("submit",function(dets){
// 	dets.preventDefault();
// 	let card=document.createElement("div");
// 	card.classList.add("card");
// 	let profile=document.createElement("div");
// 	profile.classList.add("profile");
// 	let img=document.createElement("img");
// 	img.setAttribute("src","input[4].value");
// 	let h3=document.createElement("h3");
// 	h3.textContent=`${input[0].value}`;
// 	let h6=document.createElement("h6");
// 	h6.textContent=`(${input[1].value} years old)`;
// 	let h5=document.createElement("h5");
// 	h5.textContent=`${input[2].value}`;
// 	let p=document.createElement("p");
// 	p.textContent=`${input[3].value}`;

// 	profile.appendChild(img);
// 	card.appendChild(profile);
// 	card.appendChild(h3);
// 	card.appendChild(h6);
// 	card.appendChild(h5);
// 	card.appendChild(p);

// 	main.appendChild(card);
// });

let form = document.querySelector("form");
let input = document.querySelectorAll(".form-input");
let main = document.querySelector("#main");

form.addEventListener("submit", function (e) {
  e.preventDefault();

  // Remove old card
  let oldCard = document.querySelector(".card");
  if (oldCard) oldCard.remove();

  // Create Card
  let card = document.createElement("div");
  card.classList.add("card");

  // Profile Image
  let profile = document.createElement("div");
  profile.classList.add("profile");

  let img = document.createElement("img");
  img.src = input[4].value || "https://th.bing.com/th/id/OIP.ghDeAxQENeJRnpp7tlZyCwHaHa?w=196&h=196&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3"; // FIXED IMAGE

  // Text
  let h3 = document.createElement("h3");
  h3.textContent = input[0].value;

  let h6 = document.createElement("h6");
  h6.textContent = `(${input[1].value} years old)`;

  let h5 = document.createElement("h5");
  h5.textContent = input[2].value;

  let p = document.createElement("p");
  p.textContent = input[3].value;

  // Download Button
  let downloadBtn = document.createElement("button");
  downloadBtn.textContent = "DOWNLOAD CARD";
  downloadBtn.classList.add("btn");

  // Append
  profile.appendChild(img);
  card.appendChild(profile);
  card.appendChild(h3);
  card.appendChild(h6);
  card.appendChild(h5);
  card.appendChild(p);
  card.appendChild(downloadBtn);

  main.appendChild(card);

  // Download Function (Button hidden during capture)
  downloadBtn.addEventListener("click", function () {
  downloadBtn.style.display = "none"; // hide button before capture

  html2canvas(card, {
    scale: 3,              // ⭐ MAIN FIX (Higher = Better Quality)
    useCORS: true,
    backgroundColor: null  // keeps clean background
  }).then((canvas) => {
    const link = document.createElement("a");
    link.download = "profile-card-HD.png";
    link.href = canvas.toDataURL("image/png", 1.0); // max quality
    link.click();

    downloadBtn.style.display = "block"; // show button again
  });
});
});
// Clear button functionality
let clearBtn = document.querySelector("#clearBtn");

clearBtn.addEventListener("click", function () {
  // 1. Remove the card if it exists
  const card = document.querySelector(".card");
  if (card) {
    card.remove();
  }

  // 2. Clear all input fields
  input.forEach(function (field) {
    field.value = "";
  });

  // (Optional) Reset focus to first input
  input[0].focus();
});