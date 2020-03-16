//MOUSE HOVER AND MOUSE OUT ANIMATION

var allcolumns = document.querySelectorAll('.column');

for (let i = 0; i < allcolumns.length; i++) {
	allcolumns[i].addEventListener('mouseover', function() {
		document.querySelectorAll('.column')[i].style.transform = 'scale(1.1)';
	})

	allcolumns[i].addEventListener('mouseout' , function(){
		document.querySelectorAll('.column')[i].style.transform = 'scale(1)';
	})

};







//Animation for the dropdown on profile username
$(".userprofilename").on("mouseover", function() {
	$(".userprofilename").css("color","brown");
})


$(".userprofilename").on("mouseout", function() {
	$(".userprofilename").css("color","white");
})

$(".userprofilename").on("click", function() {
		$("nav ul li ul").slideDown("slow");
		
})


window.onclick = function(event) {
	if (!event.target.matches(".userprofilename")){
		$("nav ul li ul").slideUp("slow");
	}
}



//SEARCH BAR CLICK FUNCTION
$(".searchbar input[type=text]").on('click', function() {
	$(".searchbar input[type=text] ").css("opacity", "1");
})








// NAVIGATION BAR ANIMATION

//NOTE: CHANGE THIS OPTION IF YOU KNOW HOW TO PASS JINJA DATA TO JAVASCRIPT

window.addEventListener('scroll', function(){
	var navBar = document.querySelector('.loginnav');

	
	if (window.location.pathname == '/' || window.location.pathname =='/ryanulysses' ) {

		if (window.scrollY < 631) {

		navBar.classList.remove("loginnav-fixed");
		$('nav ul a').css('color','white');
		$('nav a h2').css('color','white');
		$('.searchbar input[type=text]').css('opacity','0.2');
		$('.userprofilename').css('color','white');
		$('.loginnav').css('position', 'fixed')
		$('.loginnav').css('border-bottom', 'none');

		$(".searchbar input[type=text]").on('mouseout', function() {
			$(".searchbar input[type=text] ").css("opacity", "0.2");
		})



	} else {

		navBar.classList.add("loginnav-fixed");
		$('.userprofilename').css('color','#ead1ae');
		$('nav ul a').css('color','#ead1ae');
		$('nav a h2').css('color','#ead1ae');
		$('.searchbar input[type=text]').css('opacity','0.8');
		$('.loginnav').css('border-bottom', '1px solid #ead1ae');


	}


	
	} else {

		if (window.scrollY == 0) {

		navBar.classList.remove("loginnav-fixed");
		$('nav ul a').css('color','white');
		$('nav a h2').css('color','white');
		$('.searchbar input[type=text]').css('opacity','0.2');
		$('.userprofilename').css('color','white');
		$('.loginnav').css('position', 'fixed')
		$('.loginnav').css('border-bottom', 'none');


		} else {

		navBar.classList.add("loginnav-fixed");
		$('.userprofilename').css('color','#ead1ae');
		$('nav ul a').css('color','#ead1ae');
		$('nav a h2').css('color','#ead1ae');
		$('.searchbar input[type=text]').css('opacity','0.8');
		$('.loginnav').css('border-bottom', '1px solid #ead1ae');


		}
	}


})





//HAMBURGER MENU ANIMATION
$('.hamburgerContainer').on('click', function() {
	$('nav ul').toggleClass('hamburgerToggler');
	
})



//SHOWCASE FONT ANIMATION (INDEX.HTML)
window.addEventListener('scroll', function() {
	if (window.scrollY > 190) {
		$('#showcase h1').css('opacity', '0')
	} else {
		$('#showcase h1').css('opacity', '1')
	}
})





// ANIMATION ON ARTICLE PAGE ON LOAD


$( document ).ready(function() {
    $('.dishnamesummarygroup').css('opacity', '1');
    $('.dishnamesummarygroup').css('transform', 'translateY(0px)');
    $('#showcase h1').css('opacity', '1');
});






if ((window.location.href).includes('article')) {

	// EASE IN AND OUT ANIMATION IN THE RECIPE SHOWCASE BOX	(ARTICLE.HTML)

	function scrollAnimation2 () {

	var animateIngredientsBox = document.querySelector('.ingredientsshowcase');
	var animateDirectionsBox = document.querySelector('.directionsshowcase');
	var animateCommentsBox = document.querySelector('.commentsArea');
	var animateLinksBox = document.querySelector('.links');



	var articleIngredientsPosition = animateIngredientsBox.getBoundingClientRect().top;
	var articleDirectionsPosition = animateDirectionsBox.getBoundingClientRect().top;
	var articleCommentsPosition = animateCommentsBox.getBoundingClientRect().top;
	var articleLinksPosition = animateLinksBox.getBoundingClientRect().top;


	if (articleIngredientsPosition <  window.innerHeight) {
		animateIngredientsBox.classList.add("recipeshowcase-appear");
	}

	if (articleDirectionsPosition <  window.innerHeight) {
		animateDirectionsBox.classList.add("recipeshowcase-appear");
	}

	if (articleCommentsPosition <  window.innerHeight) {
		animateCommentsBox.classList.add("recipeshowcase-appear");
	}

	if (articleLinksPosition <  window.innerHeight) {
		animateLinksBox.classList.add("recipeshowcase-appear");
	}


}

window.addEventListener('scroll', scrollAnimation2);


} else {

	// EASE IN AND OUT ANIMATION IN THE ARTICLE BOX	(INDEX.HTML)

		function scrollAnimation() {

		var animateBannerBox = document.querySelector('.banner');
		var animateIntroDescriptionBox = document.querySelector('.introdescription');
		var animateIntroImageBox = document.querySelector('.introimage');
		var animateRowBox = document.querySelector('.row');
		var animateCollectionBox = document.querySelector('.recipecollectionheader');


		var articleBannerPosition = animateBannerBox.getBoundingClientRect().top;
		var articleIntroDescriptionPosition = animateIntroDescriptionBox.getBoundingClientRect().top;
		var articleIntroImagePosition = animateIntroImageBox.getBoundingClientRect().top;
		var articleRowPosition = animateRowBox.getBoundingClientRect().top;
		var articleCollectionPosition = animateCollectionBox.getBoundingClientRect().top;



		var screenHeight = window.innerHeight;
		

		if (articleBannerPosition < screenHeight) {
			animateBannerBox.classList.add("articlebox-appear");
		}

		if (articleIntroDescriptionPosition < screenHeight) {
			 animateIntroDescriptionBox.classList.add("articlebox-appear");
		}

		if (articleIntroImagePosition < screenHeight) {
			 animateIntroImageBox.classList.add("articlebox-appear");
		}

		if (articleRowPosition < screenHeight) {
			 animateRowBox.classList.add("articlebox-appear");
		}

		if (articleCollectionPosition < screenHeight) {
			 animateCollectionBox.classList.add("articlebox-appear");
		}


		}


		window.addEventListener('scroll', scrollAnimation);



		//GETTING THE RANDOM QUOTES FROM THE WEB API
		//APPLY AJAX TO CHANGE THE QUOTE EVERY 6 SECONDS

		randomQuoteGenerator();
		var random = setInterval(randomQuoteGenerator, 10000);

		function randomQuoteGenerator () {

		var randomQuoteRequest = new XMLHttpRequest();
		randomQuoteRequest.open('GET', 'http://quotes.stormconsultancy.co.uk/random.json', true);
		randomQuoteRequest.onload = function () {
			var quotes = JSON.parse(randomQuoteRequest.responseText);


			var quote = document.querySelector('.quote');
			var author = document.querySelector('.author');

			quote.innerHTML = quotes.quote;
			author.innerHTML = '-' + quotes.author;

			//jQuery for Fade in and Fade out of random quotes
			setTimeout(function() {

				$(".quote").ready(function() {
					setTimeout(function() {
						$(".quote").fadeOut(3050);
						$(".author").fadeOut(3050);
					})

					setTimeout(function() {
						$(".quote").fadeIn(3000);
						$(".author").fadeIn(3000);
					},3050)

				})
				
			}, 7000);

			
		};

		randomQuoteRequest.send();

		};



}





