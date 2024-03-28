document.addEventListener("DOMContentLoaded", function() {
    const questionsContainer = document.getElementById("questions-container");
    const nextButton = document.getElementById("next-button");
    const submitButton = document.getElementById("submit-button");

    let currentQuestionIndex = 0;
    let questions = [];

    nextButton.addEventListener("click", function() {
        displayNextQuestion();
    });

    submitButton.addEventListener("click", function(event) {
        event.preventDefault(); // Prevent default form submission behavior

        // Collect user-selected answers
        const selectedAnswer = document.querySelector('input[name="answer"]:checked');
        if (!selectedAnswer) {
            alert("Please select an answer before submitting.");
            return;
        }
        const userAnswer = selectedAnswer.value;

        // Send answers to backend
        fetch("/api/calculate_score/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ answer: userAnswer }),
        })
        .then(response => response.json())
        .then(data => {
            // Handle response from backend (e.g., display score)
            const score = data.score;
            alert("Your score is: " + score);
        })
        .catch(error => {
            console.error("Error submitting answers:", error);
            alert("An error occurred while submitting your answers. Please try again later.");
        });
    });

    function fetchQuestions(category) {
        fetch(`/api/get_questions/?category=${category}`)
            .then(response => response.json())
            .then(data => {
                questions = data.data;
                displayQuestion(currentQuestionIndex);
            });
    }

    function displayQuestion(index) {
        const question = questions[index];
        questionsContainer.innerHTML = `
            <div>
                <p>${question.question_text}</p>
                <form id="question-form">
                    ${question.answers.map(answer => `
                        <div>
                            <input type="radio" name="answer" value="${answer.text}" id="${answer.text}">
                            <label for="${answer.text}">${answer.text}</label>
                        </div>
                    `).join('')}
                </form>
            </div>
        `;
    }

    function displayNextQuestion() {
        currentQuestionIndex++;
        if (currentQuestionIndex < questions.length) {
            displayQuestion(currentQuestionIndex);
        } else {
            questionsContainer.innerHTML = "<p>No more questions.</p>";
            nextButton.style.display = "none";
            submitButton.style.display = "inline-block";
        }
    }

    // You need to trigger the category selection and fetch questions based on the selected category
});