$(document).ready(function () {
    var currentIndex = 0;
    var flashcards = $('.flashcard-card');
    var totalCards = flashcards.length;

    // Set the first card to be active
    flashcards.eq(currentIndex).addClass('active');

    // Update active card display
    function updateActiveCard() {
        flashcards.removeClass('active');
        flashcards.eq(currentIndex).addClass('active');
    }

    // Next Button Logic
    $('#next-btn').click(function () {
        if (currentIndex < totalCards - 1) {
            currentIndex++;
            updateActiveCard();
        }
    });

    // Previous Button Logic
    $('#prev-btn').click(function () {
        if (currentIndex > 0) {
            currentIndex--;
            updateActiveCard();
        }
    });
});
