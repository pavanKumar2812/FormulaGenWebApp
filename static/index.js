$(document).ready(function () {
    $(".latex").latex();
    
    $(".GenBtn").on("click", function (e) {
        e.preventDefault(); // Prevent form submission

        const formulaDescription = $("#formula_description").val();
        $("#latex_code_container, #latex_image_container, #error_message").empty();

        // Send AJAX POST request
        $.ajax({
            url: "/SendFormula",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ formula_description: formulaDescription }),
            success: function (response) {
                console.log(response);
                
                // Check and display the LaTeX code
                if (response.latex_code) {
                    $("#latex_code_container").text(response.latex_code);
                    $("#latex_code_container").latex(); // Render LaTeX dynamically
                }

                // Display the rendered image if available
                if (response.latex_image) {
                    $("#latex_image_container").html(`
                        <h2>Rendered Formula:</h2>
                        <img src="data:image/png;base64,${response.latex_image}" alt="Generated Formula">
                    `);
                }

                // Display any error messages if available
                if (response.error_message) {
                    $("#error_message").text(response.error_message);
                }
            },
            error: function () {
                $("#error_message").text("An error occurred while processing your request.");
            },
        });
    });
});
