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