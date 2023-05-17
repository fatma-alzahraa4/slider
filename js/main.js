
var imageList = Array.from(document.querySelectorAll('.item img'));
var lightBoxContainer = document.querySelector('.lightboxContainer');
var lightBoxItem = document.querySelector('.lightboxitem');
var close = document.querySelector('#close');
var nextBtn = document.querySelector('#next');
var previousBtn = document.querySelector('#previous');
var closeBtn = document.querySelector('#close');


var currentIndex = 0;



for(var i = 0; i< imageList.length; i++){


    imageList[i].addEventListener('click', function (e) {
        var imageSource =e.target.getAttribute('src');
        currentIndex = imageList.indexOf(e.target);
        console.log(imageSource);
        lightBoxItem.style.cssText = `background-image: url(${imageSource});`

        lightBoxContainer.classList.replace('d-none','d-flex');

    });

}

function nextSlide(){
    currentIndex++;
    if(currentIndex == imageList.length
        ){
        currentIndex=0;
    }
    imageSource = imageList[currentIndex].getAttribute('src');
    lightBoxItem.style.cssText = `background-image: url(${imageSource});`
}

function previousSlide(){
    currentIndex--;
    if(currentIndex < 0){
        currentIndex=imageList.length-1;
    }
    imageSource = imageList[currentIndex].getAttribute('src');
    lightBoxItem.style.cssText = `background-image: url(${imageSource});`
}

closeBtn.addEventListener('click', function(){
    lightBoxContainer.classList.replace('d-flex','d-none');


})

document.addEventListener('keyup',function(e){
    if(e.key == 'ArrowRight'){
        nextSlide();
    }
    else if(e.key == 'ArrowLeft'){
        previousSlide();
    }
    else if(e.key == 'Escape'){
        lightBoxContainer.classList.replace('d-flex','d-none');
        
    }
})
nextBtn.addEventListener('click', nextSlide);
previousBtn.addEventListener('click', previousSlide);
