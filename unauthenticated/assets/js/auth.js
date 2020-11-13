const signUpForm = document.querySelector("#sign_up_form");
signUpForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const email = signUpForm["email"].value;
    const password = signUpForm["password"].value;

    auth.createUserWithEmailAndPassword(email, password).then((cred) => {
        console.log(cred);
    });
});

// const signInForm = document.querySelector("#sign_in_form");

// signInForm.addEventListener("submit", (e) => {
//     e.preventDefault();

//     const email = signInForm["email"].value;
//     const password = signInForm["password"].value;

//     console.log(email, password);
// });
