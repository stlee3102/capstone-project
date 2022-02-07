/*****BANNER TEXT FADEOUT - "WELCOME"*****/
$(window).scroll(function(){
$(".banner-text").css("opacity",.9- $(window).scrollTop()/300); //full transluscent opacity at window scrolltop 300
});

/*****BANNER TEXT 2 FADEOUT - "TO A NEW ADVENTURE"*****/
$(window).scroll(function(){
    ($(window).scrollTop()<=575)  // step function to introduce different behavior when threshold is passed - switch off opacity equations when window scrolltop offset reaches 575
    ?
    $(".banner-text2").css("opacity",.9)
    :
    $(".banner-text2").css("opacity",(-.9/(900-575)) * ($(window).scrollTop() - 575) + 0.9)
    /******************************
    y = m(x-a)+b
    where y is the resulting opacity and x is the window scrolltop position
    m = (y1 - y0) / (x1 - x0)

    m = (0 - 0.9) / (900 - 575) 
    //y0 initially starts at full opaque when opacity is at 0.9 (softer look than full 1)
    //y1 ends at fully translucent when opacity is 0
    //x0 initially starts when the switch over to fade equation at 575
    //x1 ends at fully translucent when window scrolltop reaches 900
    
    y = ((0 - 0.9) / (900 - 575)) * (x - 575) + 0.9
    *******************************/
    });

/*****BANNER TEXT 3 GROW LARGER - "ROADTRIPPR"*****/
$(window).scroll(function(){
	$(".banner-text3").css('font-size',(($(this).scrollTop()*.03)+40)+'px');
});


/*****TRAVELING CAR ANIMATION*****/
const html = document.documentElement; //get the full html height (including area outside of window)
const canvas = document.getElementById("traveling-car"); //get the canvas
const context = canvas.getContext("2d"); //get the space in the canvas to do draw commands

const frameCount = 475; //image frames
const currentFrame = index => ( //change index to then current image frame
  `/static/img/${index.toString().padStart(4, '0')}.jpg`
)

const preloadImages = () => { //preload all images to avoid lag in image download on scrolling
  for (let i = 1; i < frameCount; i++) {
    const img = new Image();
    img.src = currentFrame(i);
  }
};


//on startup load the first image
const img = new Image()
img.src = currentFrame(1);
canvas.width=1858; //set canvas width
canvas.height=770; //set canvas height
img.onload=function(){
  context.drawImage(img, 0, 0);  //when image is loaded, draw the image on the canvas
}

//update image index and redraw new image
const updateImage = index => { 
  img.src = currentFrame(index);
  context.drawImage(img, 0, 0);
}


//when user scrolls, update and draw images
window.addEventListener('scroll', () => {  
  const scrollTop = html.scrollTop; //get the pixel number offset from the top of the full html page based on the top of the window when user scrolls vertically, 
  const maxScrollTop = html.scrollHeight - window.innerHeight; //maximum pixel number of scroll top when the window reaches the bottom of the full html page
  const scrollFraction = scrollTop / maxScrollTop;
  const frameIndex = Math.min(
    frameCount - 2, //show last frame if fraction is greater than 1 (note that updateImage is + 1 )
    Math.ceil(scrollFraction * frameCount) //calculate image to show based on user's scroll
  );
  
  requestAnimationFrame(() => updateImage(frameIndex + 1)) //update animation with the next image
});

//call images to be preloaded
preloadImages()