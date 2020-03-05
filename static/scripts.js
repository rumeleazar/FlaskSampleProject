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




