// Global variable to store video watch duration
var watchDuration = 0;

// YouTube video player setup
var player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        videoId: '_xQNeOTRyig', // Replace with your YouTube video ID
        events: {
            'onStateChange': onPlayerStateChange
        }
    });
}

// Function to track video playback progress
function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING) {
        // Start tracking watch duration
        setInterval(function() {
            if (player.getPlayerState() == YT.PlayerState.PLAYING) {
                watchDuration += 1; // Increase duration in seconds
            }
        }, 1000); // Update duration every second
    } else if (event.data == YT.PlayerState.PAUSED) {
        // Pause tracking when video is paused
        clearInterval(watchDuration);
    }
}

// Function to send watch duration data to Django backend
function sendWatchDuration() {
    // Make an AJAX POST request to your Django view
    // Replace 'YOUR_DJANGO_VIEW_URL' with the actual URL of your Django view
    $.ajax({
        url: 'watch-course',
        type: 'POST',
        data: { 'watch_duration': watchDuration },
        success: function(data) {
            // Handle success response if needed
        },
        error: function(error) {
            // Handle error if needed
        }
    });
}

// Call the sendWatchDuration function when the video ends
player.addEventListener('onStateChange', function(event) {
    if (event.data == YT.PlayerState.ENDED) {
        sendWatchDuration();
    }
});
