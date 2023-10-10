$(document).ready(function() {
    $('#automationForm').submit(function(event) {
        event.preventDefault();

        // Gather form data
        var taskName = $('#taskName').val();
        var taskURL = $('#taskURL').val();

        // AJAX request to Flask backend
        $.ajax({
            type: 'POST',
            url: '/submit-task', // API endpoint in Flask
            data: JSON.stringify({ taskName: taskName, taskURL: taskURL }),
            contentType: 'application/json',
            success: function(response) {
                $('#result').html('Task submitted successfully!');
                // You can handle more logic here, such as updating the UI with the response.
            },
            error: function(error) {
                console.error('Error:', error);
                $('#result').html('Error occurred while submitting the task. Please try again.');
            }
        });
    });
});
