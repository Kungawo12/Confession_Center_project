// imgContainer
const imgContainer = document.querySelector('.image-container');
//  preBtn
const preBtn = document.getElementById('prev')
// nextBtn
const nextBtn = document.getElementById('next')


let x = 0;

preBtn.addEventListener('click',()=>{
    x += 45;
    rotate();
});

nextBtn.addEventListener('click',()=>{
    x -= 45;
    rotate();
});

function rotate(){
    imgContainer.style.transform = `perspective(1000px) rotateY(${x}deg)`;
}

// document.addEventListener('DOMContentLoaded', function() {
//     const likeButton = document.getElementById('likeButton');
//     const like = document.getElementById('like');
//     let count = 0;

//     likeButton.addEventListener('click', function() {
//         count++;
//         like.textContent = count;
//     });
// });
// const likeButton = document.getElementById('likeButton');



const likeButton = document.getElementById('likeButton');
const like = document.getElementById('like');
let count = 0;
likeButton.addEventListener('click', addLike());

function addLike(){
    count++;
    like.textContent = count;
}


function submitForm() {
    document.getElementById("categoryForm").submit();
}



function initMap() {
    var mapOptions = {
        center: { lat: 44.97043123001183, lng: -93.26979313386376 }, // Downtown Minneapolis coordinates
        zoom: 17 // Initial zoom level
    };
    var map = new google.maps.Map(document.getElementById('map'), mapOptions);
}
