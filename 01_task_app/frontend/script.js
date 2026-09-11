const API_URL = "";


// =========================
// REGISTER
// =========================

const registerForm = document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const username =
            document.getElementById("registerUsername").value;

        const password =
            document.getElementById("registerPassword").value;


        try {

            const response = await fetch(`${API_URL}/register`, {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username: username,
                    password: password
                })

            });


            const data = await response.json();


            if (!response.ok) {

                alert(data.detail || "Registration failed");

                return;
            }


            alert("Registration successful!");

            window.location.href = "/login";


        } catch (error) {

            console.error(error);

            alert("Something went wrong. Check the server.");

        }

    });

}



// =========================
// LOGIN
// =========================

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const username =
            document.getElementById("loginUsername").value;

        const password =
            document.getElementById("loginPassword").value;


        try {

            const response = await fetch(`${API_URL}/login`, {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username: username,
                    password: password
                })

            });


            const data = await response.json();


            if (!response.ok) {

                alert(data.detail || "Login failed");

                return;
            }


            localStorage.setItem(
                "access_token",
                data.access_token
            );


            window.location.href = "/dashboard";


        } catch (error) {

            console.error(error);

            alert("Something went wrong. Check the server.");

        }

    });

}