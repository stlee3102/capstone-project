/*****BANNER TEXT FADEOUT - "WELCOME"*****/
$(window).scroll(function(){
$(".banner-text").css("opacity",.9- $(window).scrollTop()/300); //full transluscent opacity at window scrolltop 300
console.log($(window).scrollTop())
});

/*****BANNER TEXT 2 FADEOUT - "TO A NEW ADVENTURE"*****/
$(window).scroll(function(){
    ($(window).scrollTop()<=575)  // switch off opacity equations when window scrolltop offset reaches 575
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
const html = document.documentElement;
const canvas = document.getElementById("traveling-car");
const context = canvas.getContext("2d");

const frameCount = 478;
const currentFrame = index => (
  `/static/img/${index.toString().padStart(4, '0')}.jpg`
)

const preloadImages = () => {
  for (let i = 1; i < frameCount; i++) {
    const img = new Image();
    img.src = currentFrame(i);
  }
};

const img = new Image()
img.src = currentFrame(1);
canvas.width=1858;
canvas.height=770;
img.onload=function(){
  context.drawImage(img, 0, 0);
}

const updateImage = index => {
  img.src = currentFrame(index);
  context.drawImage(img, 0, 0);
}

window.addEventListener('scroll', () => {  
  const scrollTop = html.scrollTop;
  const maxScrollTop = html.scrollHeight - window.innerHeight;
  const scrollFraction = scrollTop / maxScrollTop;
  const frameIndex = Math.min(
    frameCount - 1,
    Math.ceil(scrollFraction * frameCount)
  );
  
  requestAnimationFrame(() => updateImage(frameIndex + 1))
});

preloadImages()