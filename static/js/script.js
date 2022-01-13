/*****BANNER TEXT FADEOUT*****/
$(window).scroll(function(){
$(".banner-text").css("opacity",.9- $(window).scrollTop()/300);
});

/*****BANNER TEXT 2 FADEOUT*****/
$(window).scroll(function(){
    $(".banner-text2").css("opacity",1- $(window).scrollTop()/900);
    });

/*****BANNER TEXT 3 GROW LARGER*****/
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